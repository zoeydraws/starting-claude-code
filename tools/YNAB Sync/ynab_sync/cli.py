"""CLI interface for ynab-sync."""

from pathlib import Path

import click

from .config import load_config
from .parsers import detect_bank, detect_account_type, get_parser
from .ynab_api import YNABClient, YNABError


@click.group()
@click.option("--config", "-c", "config_path", type=click.Path(exists=True), help="Path to config file")
@click.pass_context
def cli(ctx, config_path):
    """YNAB Sync - Import bank transactions to YNAB."""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path


@cli.command("import")
@click.argument("csv_file", type=click.Path(exists=True))
@click.option("--account", "-a", required=True, help="Account name (from config)")
@click.option("--bank", "-b", help="Bank type (dbs, citibank, uob, wise). Auto-detected if not specified.")
@click.option("--dry-run", is_flag=True, help="Show what would be imported without making changes")
@click.pass_context
def import_cmd(ctx, csv_file, account, bank, dry_run):
    """Import transactions from a bank CSV/Excel file."""
    try:
        config = load_config(ctx.obj.get("config_path"))
    except FileNotFoundError as e:
        raise click.ClickException(str(e))

    # Find account config
    account_config = config.get_account(account)
    if not account_config:
        available = [acc.name for acc in config.accounts]
        raise click.ClickException(
            f"Account '{account}' not found in config. Available: {available}"
        )

    # Determine bank type
    if bank:
        bank_type = bank.lower()
    else:
        bank_type = detect_bank(csv_file)
        if not bank_type:
            # Fall back to account's configured bank
            bank_type = account_config.bank.lower()
        click.echo(f"Detected bank: {bank_type}")

    # Parse CSV
    try:
        parser = get_parser(bank_type)
    except ValueError as e:
        raise click.ClickException(str(e))

    transactions = parser.parse(csv_file)

    if not transactions:
        click.echo("No transactions found in file.")
        return

    click.echo(f"Found {len(transactions)} transactions")

    if dry_run:
        click.echo("\nDry run - transactions that would be imported:")
        for txn in transactions[:10]:
            amount_display = txn.amount / 1000
            click.echo(f"  {txn.date} | {amount_display:>10.2f} | {txn.payee_name[:40]}")
        if len(transactions) > 10:
            click.echo(f"  ... and {len(transactions) - 10} more")
        return

    # Import to YNAB
    click.echo(f"Importing to YNAB account: {account_config.name}")

    try:
        with YNABClient(config.ynab.api_token) as client:
            result = client.create_transactions(
                budget_id=config.ynab.budget_id,
                account_id=account_config.ynab_account_id,
                transactions=transactions,
            )

            # Report results
            created = result.get("transaction_ids", [])
            duplicates = result.get("duplicate_import_ids", [])

            click.echo(f"Created: {len(created)} transactions")
            if duplicates:
                click.echo(f"Skipped: {len(duplicates)} duplicates")

    except YNABError as e:
        raise click.ClickException(f"YNAB API error: {e}")


@cli.command("accounts")
@click.pass_context
def accounts_cmd(ctx):
    """List configured accounts."""
    try:
        config = load_config(ctx.obj.get("config_path"))
    except FileNotFoundError as e:
        raise click.ClickException(str(e))

    click.echo("Configured accounts:")
    for acc in config.accounts:
        click.echo(f"  {acc.name}")
        click.echo(f"    Bank: {acc.bank}")
        click.echo(f"    YNAB ID: {acc.ynab_account_id}")


@cli.command("ynab-accounts")
@click.pass_context
def ynab_accounts_cmd(ctx):
    """List YNAB accounts (for setup)."""
    try:
        config = load_config(ctx.obj.get("config_path"))
    except FileNotFoundError as e:
        raise click.ClickException(str(e))

    try:
        with YNABClient(config.ynab.api_token) as client:
            # Get budgets
            budgets = client.get_budgets()
            if not budgets:
                click.echo("No budgets found.")
                return

            click.echo("YNAB Budgets and Accounts:")
            for budget in budgets:
                click.echo(f"\nBudget: {budget['name']}")
                click.echo(f"  ID: {budget['id']}")

                accounts = client.get_accounts(budget['id'])
                for acc in accounts:
                    if acc.get("deleted"):
                        continue
                    balance = acc.get("balance", 0) / 1000
                    click.echo(f"\n  Account: {acc['name']}")
                    click.echo(f"    ID: {acc['id']}")
                    click.echo(f"    Type: {acc['type']}")
                    click.echo(f"    Balance: {balance:.2f}")

    except YNABError as e:
        raise click.ClickException(f"YNAB API error: {e}")


@cli.command("import-dir")
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--dry-run", is_flag=True, help="Show what would be imported without making changes")
@click.pass_context
def import_dir_cmd(ctx, directory, dry_run):
    """Import all CSV/Excel files from a directory.

    Files are matched to accounts based on detected bank and card type.
    Supports: .csv, .xls, .xlsx files
    """
    try:
        config = load_config(ctx.obj.get("config_path"))
    except FileNotFoundError as e:
        raise click.ClickException(str(e))

    # Find all supported files
    dir_path = Path(directory)
    files = []
    for pattern in ["*.csv", "*.xls", "*.xlsx"]:
        files.extend(dir_path.glob(pattern))

    if not files:
        click.echo("No CSV/Excel files found in directory.")
        return

    click.echo(f"Found {len(files)} files")

    for file_path in files:
        click.echo(f"\nProcessing: {file_path.name}")

        # Detect specific account type (e.g., uob-one-cc, citi-premier-cc)
        account_type = detect_account_type(str(file_path))
        if not account_type:
            click.echo("  Could not detect bank/account type, skipping.")
            continue

        click.echo(f"  Detected account type: {account_type}")

        # Find matching account by bank type
        matching_accounts = config.get_account_by_bank(account_type)
        if not matching_accounts:
            # Fall back to base bank type (e.g., "uob" instead of "uob-one-cc")
            base_bank = account_type.split("-")[0]
            matching_accounts = config.get_account_by_bank(base_bank)

        if not matching_accounts:
            click.echo(f"  No account configured for '{account_type}', skipping.")
            continue

        if len(matching_accounts) > 1:
            click.echo(f"  Multiple accounts for '{account_type}':")
            for acc in matching_accounts:
                click.echo(f"    - {acc.name}")
            click.echo("  Use 'ynab-sync import' with --account to specify.")
            continue

        account_config = matching_accounts[0]
        click.echo(f"  Using account: {account_config.name}")

        # Parse
        parser = get_parser(account_type)
        transactions = parser.parse(str(file_path))

        if not transactions:
            click.echo("  No transactions found.")
            continue

        click.echo(f"  Found {len(transactions)} transactions")

        if dry_run:
            for txn in transactions[:3]:
                amount_display = txn.amount / 1000
                click.echo(f"    {txn.date} | {amount_display:>10.2f} | {txn.payee_name[:30]}")
            if len(transactions) > 3:
                click.echo(f"    ... and {len(transactions) - 3} more")
            continue

        # Import
        try:
            with YNABClient(config.ynab.api_token) as client:
                result = client.create_transactions(
                    budget_id=config.ynab.budget_id,
                    account_id=account_config.ynab_account_id,
                    transactions=transactions,
                )
                created = len(result.get("transaction_ids", []))
                duplicates = len(result.get("duplicate_import_ids", []))
                click.echo(f"  Imported: {created} new, {duplicates} duplicates")
        except YNABError as e:
            click.echo(f"  Error: {e}")


@cli.command("detect")
@click.argument("file", type=click.Path(exists=True))
def detect_cmd(file):
    """Detect bank and account type from a file."""
    account_type = detect_account_type(file)
    bank_type = detect_bank(file)

    if not bank_type:
        click.echo("Could not detect bank type.")
        return

    click.echo(f"Bank: {bank_type}")
    if account_type and account_type != bank_type:
        click.echo(f"Account type: {account_type}")


@cli.command("run")
@click.option("--dry-run", is_flag=True, help="Preview only, don't upload")
@click.pass_context
def run_cmd(ctx, dry_run):
    """Process all files in the inbox folder and upload to YNAB.

    This is the main command. Just drop your bank files in the 'inbox' folder
    and run this command.
    """
    # Find inbox folder (relative to config or current directory)
    config_path = ctx.obj.get("config_path")
    if config_path:
        inbox_dir = Path(config_path).parent / "inbox"
    else:
        # Try current directory, then package directory
        inbox_dir = Path.cwd() / "inbox"
        if not inbox_dir.exists():
            # Try relative to this file's location
            inbox_dir = Path(__file__).parent.parent / "inbox"

    if not inbox_dir.exists():
        click.echo(f"Inbox folder not found: {inbox_dir}")
        click.echo("Create an 'inbox' folder and drop your bank files there.")
        return

    # Call import-dir with the inbox folder
    ctx.invoke(import_dir_cmd, directory=str(inbox_dir), dry_run=dry_run)

    # If not dry run, offer to clear processed files
    if not dry_run:
        click.echo("\nDone! You can now delete the files from the inbox folder.")


if __name__ == "__main__":
    cli()
