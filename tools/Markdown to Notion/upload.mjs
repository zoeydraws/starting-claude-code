import { Client } from "@notionhq/client";
import { markdownToBlocks } from "@tryfabric/martian";
import { readFileSync } from "fs";
import { basename } from "path";
import { execSync } from "child_process";

// ─── Keychain & Setup ────────────────────────────────────────────────

function getKeychainValue(service) {
  return execSync(
    `security find-generic-password -a "notion" -s "${service}" -w`
  )
    .toString()
    .trim();
}

const notion = new Client({ auth: getKeychainValue("notion-api-key") });
const databaseId = getKeychainValue("notion-database-id");

// ─── Concurrency ────────────────────────────────────────────────────

const READ_CONCURRENCY = 5; // Block/comment fetches (lighter on rate limit)
const WRITE_CONCURRENCY = 3; // Deletes, updates, appends (conservative)

// ─── Concurrency Pool ───────────────────────────────────────────────

// Runs async tasks with a max concurrency limit to respect Notion's rate limit.
async function pooled(tasks, concurrency = 3) {
  const results = new Array(tasks.length);
  let idx = 0;

  async function worker() {
    while (idx < tasks.length) {
      const i = idx++;
      results[i] = await tasks[i]();
    }
  }

  await Promise.all(Array.from({ length: concurrency }, () => worker()));
  return results;
}

// Cache for user name lookups (userId → name)
const userNameCache = new Map();

// ─── CLI Arguments ──────────────────────────────────────────────────

const flags = { dryRun: false, refresh: false };
let filePath = null;

for (const arg of process.argv.slice(2)) {
  if (arg === "--dry-run") flags.dryRun = true;
  else if (arg === "--refresh") flags.refresh = true;
  else if (!arg.startsWith("--")) filePath = arg;
}

if (!filePath) {
  console.error(
    "Usage: node upload.mjs [--dry-run] [--refresh] <path-to-md-file>"
  );
  process.exit(1);
}

const markdown = readFileSync(filePath, "utf-8");
const title = basename(filePath, ".md");

// ─── Database & Page Lookup ──────────────────────────────────────────

async function getDataSourceId() {
  const db = await notion.databases.retrieve({ database_id: databaseId });
  return db.data_sources[0].id;
}

async function findExistingPage(dataSourceId, pageTitle) {
  const response = await notion.dataSources.query({
    data_source_id: dataSourceId,
    filter: {
      property: "Name",
      title: { equals: pageTitle },
    },
  });
  return response.results[0] || null;
}

// ─── Recursive Block Fetching ────────────────────────────────────────

// Fetches all blocks under a parent, paginating through all results.
// Sets a `_children` property on blocks that have nested children.
async function fetchBlocksRecursive(parentId) {
  const blocks = [];
  let cursor = undefined;

  do {
    const response = await notion.blocks.children.list({
      block_id: parentId,
      start_cursor: cursor,
      page_size: 100,
    });
    blocks.push(...response.results);
    cursor = response.has_more ? response.next_cursor : undefined;
  } while (cursor);

  // Recursively fetch children in parallel
  const withChildren = blocks.filter((b) => b.has_children);
  if (withChildren.length > 0) {
    await pooled(
      withChildren.map((block) => async () => {
        block._children = await fetchBlocksRecursive(block.id);
      }),
      READ_CONCURRENCY
    );
  }

  return blocks;
}

// ─── Comment Fetching ────────────────────────────────────────────────

// Fetches comments for every block in the tree, returns a Map of blockId → comments[].
// Also fetches page-level comments (keyed by pageId).
async function fetchCommentsForBlocks(blocks, pageId) {
  const commentsMap = new Map();

  // Collect all block IDs (including nested) + page ID into a flat list
  const allIds = [pageId];
  function collectIds(blockList) {
    for (const block of blockList) {
      allIds.push(block.id);
      if (block._children) collectIds(block._children);
    }
  }
  collectIds(blocks);

  // Fetch all comments in parallel with concurrency limit
  await pooled(
    allIds.map((id) => async () => {
      const comments = await fetchAllComments(id);
      if (comments.length > 0) {
        commentsMap.set(id, comments);
      }
    }),
    READ_CONCURRENCY
  );

  return commentsMap;
}

// Paginate through all comments on a single block/page.
async function fetchAllComments(blockId) {
  const comments = [];
  let cursor = undefined;

  do {
    const response = await notion.comments.list({
      block_id: blockId,
      start_cursor: cursor,
      page_size: 100,
    });
    comments.push(...response.results);
    cursor = response.has_more ? response.next_cursor : undefined;
  } while (cursor);

  return comments;
}

// Fetches comments only for affected blocks (deleted + changed) and their children.
// Returns the same Map<blockId, comments[]> format as fetchCommentsForBlocks.
async function fetchCommentsForAffectedBlocks(affectedItems, pageId) {
  const commentsMap = new Map();
  const ids = new Set();

  // Collect block IDs from affected items and their children (recursive)
  function collectIds(block) {
    ids.add(block.id);
    if (block._children) {
      for (const child of block._children) collectIds(child);
    }
  }

  for (const item of affectedItems) {
    collectIds(item.old);
  }

  // Also fetch page-level comments
  ids.add(pageId);

  await pooled(
    [...ids].map((id) => async () => {
      const comments = await fetchAllComments(id);
      if (comments.length > 0) {
        commentsMap.set(id, comments);
      }
    }),
    READ_CONCURRENCY
  );

  return commentsMap;
}

// ─── Block Text Extraction ──────────────────────────────────────────

// Extracts plain text from a block's rich_text array (works for both
// Notion API response blocks and martian-generated blocks).
function extractBlockText(block) {
  const type = block.type;
  if (!type) return "";

  const content = block[type];
  if (!content) return "";

  // Most block types store text in `rich_text`
  const richText = content.rich_text;
  if (!richText || !Array.isArray(richText)) return "";

  return richText.map((rt) => rt.plain_text || rt.text?.content || "").join("");
}

// ─── Block Content Key ──────────────────────────────────────────────

// Extracts text from all children of a block (for tables, quotes with children, etc.)
function extractChildrenText(block) {
  // Notion API blocks use `_children`, martian blocks use `children`
  const children = block._children || block[block.type]?.children;
  if (!children || !Array.isArray(children)) return "";

  return children
    .map((child) => {
      // Table rows store text in `cells` (array of arrays of rich_text)
      if (child.type === "table_row" && child.table_row?.cells) {
        return child.table_row.cells
          .map((cell) =>
            cell
              .map((rt) => rt.plain_text || rt.text?.content || "")
              .join("")
          )
          .join("|");
      }
      // Other child blocks – extract their rich_text
      return extractBlockText(child) + extractChildrenText(child);
    })
    .join("\n");
}

// Produces a comparable string from a block: "type:plaintext+childrentext"
function blockContentKey(block) {
  const text = extractBlockText(block);
  const childText = extractChildrenText(block);
  return `${block.type}:${text}${childText ? "\n" + childText : ""}`;
}

// ─── LCS-Based Diff ─────────────────────────────────────────────────

// Computes the longest common subsequence indices between oldBlocks and newBlocks,
// then classifies each block as unchanged, changed, deleted, or added.
//
// Returns:
// {
//   unchanged: [ { old, new, oldIndex, newIndex } ],
//   changed:   [ { old, new, oldIndex, newIndex } ],
//   deleted:   [ { old, oldIndex } ],
//   added:     [ { new, newIndex, afterBlockId } ],
// }
function diffBlocks(oldBlocks, newBlocks) {
  const oldKeys = oldBlocks.map(blockContentKey);
  const newKeys = newBlocks.map(blockContentKey);

  // Build LCS table
  const m = oldKeys.length;
  const n = newKeys.length;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (oldKeys[i - 1] === newKeys[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // Backtrack to find matched pairs
  const matchedOld = new Set();
  const matchedNew = new Set();
  const matchPairs = []; // { oldIndex, newIndex }

  let i = m;
  let j = n;
  while (i > 0 && j > 0) {
    if (oldKeys[i - 1] === newKeys[j - 1]) {
      matchPairs.unshift({ oldIndex: i - 1, newIndex: j - 1 });
      matchedOld.add(i - 1);
      matchedNew.add(j - 1);
      i--;
      j--;
    } else if (dp[i - 1][j] >= dp[i][j - 1]) {
      i--;
    } else {
      j--;
    }
  }

  // Classify blocks
  const unchanged = [];
  const changed = [];
  const deleted = [];
  const added = [];

  // Unchanged = blocks in the LCS (same content, same relative order)
  for (const { oldIndex, newIndex } of matchPairs) {
    unchanged.push({
      old: oldBlocks[oldIndex],
      new: newBlocks[newIndex],
      oldIndex,
      newIndex,
    });
  }

  // Deleted = old blocks not in LCS
  for (let idx = 0; idx < oldBlocks.length; idx++) {
    if (!matchedOld.has(idx)) {
      deleted.push({ old: oldBlocks[idx], oldIndex: idx });
    }
  }

  // Added = new blocks not in LCS.
  // For each added block, find which existing block it should be inserted after.
  for (let idx = 0; idx < newBlocks.length; idx++) {
    if (!matchedNew.has(idx)) {
      // Find the nearest preceding block in newBlocks that IS matched,
      // so we can insert after that block's old ID.
      let afterBlockId = null;
      for (let k = idx - 1; k >= 0; k--) {
        if (matchedNew.has(k)) {
          // This new block at k matched an old block – use that old block's ID
          const pair = matchPairs.find((p) => p.newIndex === k);
          if (pair) {
            afterBlockId = oldBlocks[pair.oldIndex].id;
          }
          break;
        }
      }
      added.push({ new: newBlocks[idx], newIndex: idx, afterBlockId });
    }
  }

  // Check for type-changed blocks: old and new at "same position" but different types.
  // We detect this by looking at deleted+added blocks that could pair up by position.
  // If an old block is deleted and a new block is added at a similar position with
  // the same type, we could update it. But if the type differs, we must delete+add.
  // For now, leave as separate delete/add – the plan says type changes = delete + add.

  return { unchanged, changed, deleted, added };
}

// ─── Comment Migration ──────────────────────────────────────────────

// For deleted blocks that have comments, creates a callout marker at page top
// and re-creates each comment on the callout.
// Collects all blocks with comments from a block and its children recursively.
// Returns an array of { block, comments } for each block/child that has comments.
function collectCommentedBlocks(block, commentsMap) {
  const result = [];

  // Check children first (table rows, quote children, toggle children, etc.)
  const childResults = [];
  if (block._children) {
    for (const child of block._children) {
      childResults.push(...collectCommentedBlocks(child, commentsMap));
    }
  }

  // Only include the parent block's own comments if no children have comments,
  // to avoid duplicating aggregated parent comments alongside per-child callouts.
  const comments = commentsMap.get(block.id);
  if (childResults.length > 0) {
    result.push(...childResults);
  } else if (comments && comments.length > 0) {
    result.push({ block, comments });
  }

  return result;
}

// Extracts a preview string for a block, handling table rows specially.
function blockPreview(block) {
  if (block.type === "table_row" && block.table_row?.cells) {
    return block.table_row.cells
      .map((cell) =>
        cell.map((rt) => rt.plain_text || rt.text?.content || "").join("")
      )
      .join(" | ");
  }
  return extractBlockText(block);
}

// Creates a callout + migrates comments for a single commented block.
async function migrateOneBlock(pageId, commentedBlock, position) {
  const { block, comments } = commentedBlock;
  const preview = blockPreview(block).slice(0, 80);

  const calloutResponse = await notion.blocks.children.append({
    block_id: pageId,
    children: [
      {
        type: "paragraph",
        paragraph: {
          color: "gray",
          rich_text: [
            {
              type: "text",
              text: {
                content: `📄 "${preview}${preview.length >= 80 ? "…" : ""}"`,
              },
              annotations: {
                italic: true,
                color: "gray",
              },
            },
          ],
        },
      },
    ],
    position,
  });

  const calloutBlockId = calloutResponse.results[0].id;

  // Group comments by discussion_id to preserve reply threads
  const discussions = new Map();
  for (const comment of comments) {
    const did = comment.discussion_id;
    if (!discussions.has(did)) discussions.set(did, []);
    discussions.get(did).push(comment);
  }

  // Re-create each discussion thread on the callout block
  for (const [, thread] of discussions) {
    let newDiscussionId = null;

    for (const comment of thread) {
      // Resolve real author name with caching
      const userId = comment.created_by?.id;
      let authorName = comment.created_by?.name;
      if (!authorName && userId) {
        if (userNameCache.has(userId)) {
          authorName = userNameCache.get(userId);
        } else {
          try {
            const user = await notion.users.retrieve({ user_id: userId });
            authorName = user.name;
            userNameCache.set(userId, authorName);
          } catch {
            // Fall back if we can't retrieve user
          }
        }
      }

      const createArgs = {
        rich_text: comment.rich_text,
        display_name: {
          type: "custom",
          custom: { name: authorName || "Unknown Author" },
        },
      };

      if (newDiscussionId) {
        createArgs.discussion_id = newDiscussionId;
      } else {
        createArgs.parent = {
          type: "block_id",
          block_id: calloutBlockId,
        };
      }

      const created = await notion.comments.create(createArgs);
      if (!newDiscussionId) {
        newDiscussionId = created.discussion_id;
      }
    }
  }

  return comments.length;
}

async function migrateComments(pageId, affectedBlocks, commentsMap, oldBlocks) {
  // Build set of affected block IDs for quick lookup
  const affectedIds = new Set(affectedBlocks.map((d) => d.old.id));

  // Process in ascending oldIndex order so callouts stack correctly
  const sorted = [...affectedBlocks].sort((a, b) => a.oldIndex - b.oldIndex);

  for (const { old: block, oldIndex } of sorted) {
    // Skip callout blocks that are themselves previous migration markers
    if (
      block.type === "paragraph" &&
      block.paragraph?.color === "gray" &&
      extractBlockText(block).startsWith('📄 "')
    ) {
      continue;
    }

    // Collect comments from this block AND all its children
    const commentedBlocks = collectCommentedBlocks(block, commentsMap);
    if (commentedBlocks.length === 0) continue;

    // Find the nearest preceding block that is NOT also being affected
    let position = { type: "start" };
    for (let k = oldIndex - 1; k >= 0; k--) {
      if (!affectedIds.has(oldBlocks[k].id)) {
        position = {
          type: "after_block",
          after_block: { id: oldBlocks[k].id },
        };
        break;
      }
    }

    // Create a separate callout for each commented block/child
    let totalMigrated = 0;
    for (const cb of commentedBlocks) {
      totalMigrated += await migrateOneBlock(pageId, cb, position);
    }

    console.log(
      `  Migrated ${totalMigrated} comment(s) from ${block.type}`
    );
  }
}

// ─── Apply Changes ──────────────────────────────────────────────────

// Takes the diff result and applies block-level updates to the Notion page.
async function applyChanges(pageId, diff, commentsMap, oldBlocks) {
  const { unchanged, changed, deleted, added } = diff;

  console.log(
    `  Diff: ${unchanged.length} unchanged, ${changed.length} changed, ${deleted.length} deleted, ${added.length} added`
  );

  // 1. Migrate comments for DELETED blocks (predecessor blocks still exist for positioning)
  await migrateComments(pageId, deleted, commentsMap, oldBlocks);

  // 2. Migrate comments for CHANGED blocks (inline comments can be lost on update)
  await migrateComments(pageId, changed, commentsMap, oldBlocks);

  // 3. Delete removed blocks in parallel (order doesn't matter for independent deletes)
  if (deleted.length > 0) {
    await pooled(
      deleted.map(({ old: block }) => () =>
        notion.blocks.delete({ block_id: block.id })
      ),
      WRITE_CONCURRENCY
    );
  }

  // 4. Update changed blocks in parallel (each targets a different block ID)
  if (changed.length > 0) {
    await pooled(
      changed.map(({ old: oldBlock, new: newBlock }) => () => {
        const type = newBlock.type;
        const content = newBlock[type];
        if (!content) return Promise.resolve();
        return notion.blocks.update({
          block_id: oldBlock.id,
          type,
          [type]: content,
        });
      }),
      WRITE_CONCURRENCY
    );
  }

  // 5. Append new blocks at correct positions
  // Group consecutive added blocks by their afterBlockId for batch appending
  const addGroups = groupConsecutiveAdds(added);
  for (const group of addGroups) {
    const position = group.afterBlockId
      ? { type: "after_block", after_block: { id: group.afterBlockId } }
      : { type: "start" };

    await notion.blocks.children.append({
      block_id: pageId,
      children: group.blocks.map((item) => item.new),
      position,
    });
  }

}

// Groups consecutive added blocks that share the same insertion point,
// so we can batch them into a single append call.
function groupConsecutiveAdds(addedItems) {
  if (addedItems.length === 0) return [];

  const groups = [];
  let currentGroup = {
    afterBlockId: addedItems[0].afterBlockId,
    blocks: [addedItems[0]],
  };

  for (let i = 1; i < addedItems.length; i++) {
    const item = addedItems[i];
    // If this block has the same afterBlockId as the previous,
    // they're consecutive additions at the same insertion point.
    if (item.afterBlockId === currentGroup.afterBlockId) {
      currentGroup.blocks.push(item);
    } else {
      groups.push(currentGroup);
      currentGroup = { afterBlockId: item.afterBlockId, blocks: [item] };
    }
  }
  groups.push(currentGroup);

  return groups;
}

// ─── Page Creation ──────────────────────────────────────────────────

async function createNewPage(dataSourceId, pageTitle, blocks) {
  const page = await notion.pages.create({
    parent: { type: "data_source_id", data_source_id: dataSourceId },
    properties: {
      Name: {
        title: [{ text: { content: pageTitle } }],
      },
    },
  });

  if (blocks.length > 0) {
    // Notion API limits to 100 blocks per append call
    for (let i = 0; i < blocks.length; i += 100) {
      const chunk = blocks.slice(i, i + 100);
      await notion.blocks.children.append({
        block_id: page.id,
        children: chunk,
      });
    }
  }

  return page;
}

// ─── Main ────────────────────────────────────────────────────────────

async function main() {
  // Convert markdown → Notion blocks via martian
  const newBlocks = markdownToBlocks(markdown);

  const dataSourceId = await getDataSourceId();
  const existing = await findExistingPage(dataSourceId, title);

  if (!existing) {
    if (flags.dryRun) {
      console.log(`Page "${title}" does not exist yet.`);
      console.log(`  Would create with ${newBlocks.length} block(s).`);
      console.log("No changes applied (dry run).");
      return;
    }
    // New page – create with blocks directly, no diffing needed
    const page = await createNewPage(dataSourceId, title, newBlocks);
    console.log(`Created new page: "${title}"`);
    console.log(`URL: ${page.url}`);
    return;
  }

  // ── --refresh: wipe page and re-upload from scratch ──
  if (flags.refresh) {
    console.log(`Refreshing page: "${title}" (replacing all content)`);
    console.log("  Warning: all existing comments will be destroyed.");

    if (flags.dryRun) {
      console.log(`  Would delete all existing blocks and append ${newBlocks.length} new block(s).`);
      console.log("No changes applied (dry run).");
      return;
    }

    // Fetch top-level block IDs only (no recursive children needed)
    const topBlocks = [];
    let cursor = undefined;
    do {
      const response = await notion.blocks.children.list({
        block_id: existing.id,
        start_cursor: cursor,
        page_size: 100,
      });
      topBlocks.push(...response.results);
      cursor = response.has_more ? response.next_cursor : undefined;
    } while (cursor);

    // Delete all existing blocks in parallel
    if (topBlocks.length > 0) {
      await pooled(
        topBlocks.map((block) => () =>
          notion.blocks.delete({ block_id: block.id })
        ),
        WRITE_CONCURRENCY
      );
      console.log(`  Deleted ${topBlocks.length} existing block(s).`);
    }

    // Append new blocks in 100-block chunks
    for (let i = 0; i < newBlocks.length; i += 100) {
      const chunk = newBlocks.slice(i, i + 100);
      await notion.blocks.children.append({
        block_id: existing.id,
        children: chunk,
      });
    }

    console.log(`  Appended ${newBlocks.length} new block(s).`);
    console.log(`  Done.`);
    console.log(`URL: ${existing.url}`);
    return;
  }

  // ── Normal sync: fetch blocks → diff → targeted comment fetch → apply ──
  console.log(`Updating existing page: "${title}"`);

  const oldBlocks = await fetchBlocksRecursive(existing.id);
  console.log(`  Fetched ${oldBlocks.length} existing blocks`);

  // Diff top-level blocks (nested children replaced wholesale on update)
  const diff = diffBlocks(oldBlocks, newBlocks);

  if (
    diff.changed.length === 0 &&
    diff.deleted.length === 0 &&
    diff.added.length === 0
  ) {
    console.log("  No changes detected – page is up to date.");
    console.log(`URL: ${existing.url}`);
    return;
  }

  // ── --dry-run: preview changes without mutations ──
  if (flags.dryRun) {
    console.log(
      `  Diff: ${diff.unchanged.length} unchanged, ${diff.changed.length} changed, ${diff.deleted.length} deleted, ${diff.added.length} added`
    );

    const preview = (block) => {
      const text = extractBlockText(block).slice(0, 60);
      return text ? `"${text}${text.length >= 60 ? "…" : ""}"` : `(${block.type})`;
    };

    for (const { old: block } of diff.deleted) {
      console.log(`    - DELETE ${block.type}: ${preview(block)}`);
    }
    for (const { old: oldBlock, new: newBlock } of diff.changed) {
      console.log(`    ~ CHANGE ${oldBlock.type}: ${preview(oldBlock)} → ${preview(newBlock)}`);
    }
    for (const item of diff.added) {
      console.log(`    + ADD ${item.new.type}: ${preview(item.new)}`);
    }

    console.log("No changes applied (dry run).");
    return;
  }

  // Fetch comments only for blocks that need migration (deleted + changed)
  const needsComments = [...diff.deleted, ...diff.changed];
  let commentsMap;
  if (needsComments.length > 0) {
    commentsMap = await fetchCommentsForAffectedBlocks(needsComments, existing.id);
    console.log(`  Fetched comments for ${commentsMap.size} block(s) (${needsComments.length} affected)`);
  } else {
    commentsMap = new Map();
  }

  await applyChanges(existing.id, diff, commentsMap, oldBlocks);

  console.log(`  Done.`);
  console.log(`URL: ${existing.url}`);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
