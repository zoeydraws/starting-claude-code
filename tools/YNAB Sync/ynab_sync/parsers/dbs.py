from __future__ import annotations

"""DBS Bank (Singapore) CSV parser.

DBS CSV format (based on actual exports):
- One of the first few rows contains "Account Details For:" in column 1 (used for detection)
- Header row contains "Transaction Date" and is found dynamically
- Columns typically: Transaction Date, Description, Debit Amount, Credit Amount
"""

import csv
from pathlib import Path

from dateutil.parser import parse as parse_date

from ..models import Transaction
from .base import BaseParser


class DBSParser(BaseParser):
    """Parser for DBS Bank Singapore CSV exports."""

    bank_name = "DBS"
    # Don't use detection_columns - we have custom detection
    detection_columns = []

    def detect(self, file_path: str | Path) -> bool:
        """Detect DBS CSV by checking for 'Account Details For:' marker."""
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                rows = list(reader)

                # DBS has "Account Details For:" in the first few rows, column 1 (index 0)
                # Older exports had it in row 2 (index 1), newer exports in row 1 (index 0)
                for row in rows[:3]:
                    if row and row[0] == "Account Details For:":
                        return True
        except Exception:
            pass
        return False

    def parse(self, file_path: str | Path) -> list[Transaction]:
        """Parse DBS CSV file."""
        transactions = []

        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Find header row dynamically (contains "Transaction Date" or "Date")
        header_idx = None
        for i, row in enumerate(rows):
            if row and any("transaction date" in c.lower() or c.lower().strip() == "date" for c in row):
                header_idx = i
                break

        if header_idx is None:
            return transactions

        header_row = rows[header_idx]
        header_lower = [h.lower().strip() for h in header_row]

        # Find column indices
        date_idx = self._find_column(header_lower, ["transaction date", "date"])
        ref_idx = self._find_column(header_lower, ["reference", "description", "ref"])
        debit_idx = self._find_column(header_lower, ["debit", "withdrawal"])
        credit_idx = self._find_column(header_lower, ["credit", "deposit"])

        # Process transaction rows (starting after header)
        for row in rows[header_idx + 1:]:
            if not row or len(row) <= max(date_idx or 0, ref_idx or 0):
                continue

            # Parse date
            date_str = row[date_idx].strip() if date_idx is not None and date_idx < len(row) else ""
            if not date_str:
                continue

            try:
                txn_date = parse_date(date_str, dayfirst=True).date()
            except (ValueError, TypeError):
                continue

            # Parse amount
            amount = 0.0
            if debit_idx is not None and debit_idx < len(row):
                debit_str = row[debit_idx].replace(",", "").replace("$", "").strip()
                if debit_str:
                    try:
                        amount = -abs(float(debit_str))
                    except ValueError:
                        pass

            if amount == 0 and credit_idx is not None and credit_idx < len(row):
                credit_str = row[credit_idx].replace(",", "").replace("$", "").strip()
                if credit_str:
                    try:
                        amount = abs(float(credit_str))
                    except ValueError:
                        pass

            if amount == 0:
                continue

            # Get reference/description
            payee = ""
            if ref_idx is not None and ref_idx < len(row):
                payee = row[ref_idx].strip()
            if not payee:
                payee = "DBS Transaction"
            payee = payee[:100]

            transactions.append(Transaction.from_amount(
                date=txn_date,
                amount=amount,
                payee_name=payee,
            ))

        return transactions

    def _find_column(self, headers: list[str], names: list[str]) -> int | None:
        """Find column index matching any of the given names."""
        for i, header in enumerate(headers):
            for name in names:
                if name in header:
                    return i
        return None
