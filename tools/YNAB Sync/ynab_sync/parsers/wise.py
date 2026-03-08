from __future__ import annotations

"""Wise (TransferWise) CSV parser.

Wise CSV format (based on actual exports):
- First row, first column contains "ID" (used for detection)
- Standard CSV with header row
- Columns: ID, Status, Direction, Created on, Finished on, Source fee amount,
           Source fee currency, Target fee amount, Target fee currency,
           Source name, Source amount (after fees), Source currency,
           Target name, Target amount (after fees), Target currency,
           Exchange rate, Reference, Batch
"""

import csv
from pathlib import Path

from dateutil.parser import parse as parse_date

from ..models import Transaction
from .base import BaseParser


class WiseParser(BaseParser):
    """Parser for Wise (TransferWise) CSV exports."""

    bank_name = "Wise"
    detection_columns = []

    def detect(self, file_path: str | Path) -> bool:
        """Detect Wise CSV by checking for 'ID' in first cell."""
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                first_row = next(reader, None)

                if first_row and len(first_row) > 0:
                    return first_row[0].strip() == "ID"
        except Exception:
            pass
        return False

    def parse(self, file_path: str | Path) -> list[Transaction]:
        """Parse Wise CSV file."""
        transactions = []

        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if len(rows) < 2:
            return transactions

        # First row is header
        header = rows[0]
        header_lower = [h.lower().strip() for h in header]

        # Find column indices
        date_idx = self._find_column(header_lower, ["finished on", "created on", "date"])
        amount_idx = self._find_column(header_lower, ["source amount (after fees)", "amount"])
        currency_idx = self._find_column(header_lower, ["source currency", "currency"])
        target_name_idx = self._find_column(header_lower, ["target name", "recipient"])
        source_name_idx = self._find_column(header_lower, ["source name", "sender"])
        reference_idx = self._find_column(header_lower, ["reference", "description"])
        direction_idx = self._find_column(header_lower, ["direction"])
        status_idx = self._find_column(header_lower, ["status"])

        # Process transaction rows (skip header)
        for row in rows[1:]:
            if not row:
                continue

            # Skip incomplete/cancelled transactions
            if status_idx is not None and status_idx < len(row):
                status = row[status_idx].strip().upper()
                if status not in ["COMPLETED", "FINISHED", ""]:
                    continue

            # Parse date
            date_str = ""
            if date_idx is not None and date_idx < len(row):
                date_str = row[date_idx].strip()

            if not date_str:
                continue

            try:
                # Wise uses ISO format dates typically
                txn_date = parse_date(date_str).date()
            except (ValueError, TypeError):
                continue

            # Parse amount
            amount = 0.0
            if amount_idx is not None and amount_idx < len(row):
                amount_str = row[amount_idx].replace(",", "").strip()
                if amount_str:
                    try:
                        amount = float(amount_str)
                    except ValueError:
                        continue

            if amount == 0:
                continue

            # Determine direction (IN = positive, OUT = negative)
            if direction_idx is not None and direction_idx < len(row):
                direction = row[direction_idx].strip().upper()
                if direction == "OUT":
                    amount = -abs(amount)
                elif direction == "IN":
                    amount = abs(amount)

            # Build payee name
            payee_parts = []

            # For outgoing, use target name; for incoming, use source name
            if amount < 0 and target_name_idx is not None and target_name_idx < len(row):
                target = row[target_name_idx].strip()
                if target:
                    payee_parts.append(target)
            elif amount > 0 and source_name_idx is not None and source_name_idx < len(row):
                source = row[source_name_idx].strip()
                if source:
                    payee_parts.append(source)

            payee = " - ".join(payee_parts) if payee_parts else "Wise Transfer"

            # Get reference/memo
            memo = None
            if reference_idx is not None and reference_idx < len(row):
                ref = row[reference_idx].strip()
                if ref:
                    memo = ref[:200]

            payee = payee[:100]

            transactions.append(Transaction.from_amount(
                date=txn_date,
                amount=amount,
                payee_name=payee,
                memo=memo,
            ))

        return transactions

    def _find_column(self, headers: list[str], names: list[str]) -> int | None:
        """Find column index matching any of the given names."""
        for i, header in enumerate(headers):
            for name in names:
                if name in header:
                    return i
        return None
