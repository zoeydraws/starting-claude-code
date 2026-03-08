from __future__ import annotations

"""Citibank (Singapore) CSV parser.

Citibank CSV format (based on actual exports):
- Row 1, column 5 contains card number - used for detection
- Transaction data follows after header rows
- Columns typically: Date, Description, Debit, Credit (or single Amount)
"""

import csv
from pathlib import Path

from dateutil.parser import parse as parse_date

from ..models import Transaction
from .base import BaseParser


# Mapping from last 4 digits of card number to account type identifiers
# Update these with your own card last-4 digits
CITIBANK_CARD_MAP = {
    "0000": "citi-premier-cc",
    "1111": "citi-shared-cc",
    "2222": "citi-shared-cc",
}


class CitibankParser(BaseParser):
    """Parser for Citibank Singapore CSV exports."""

    bank_name = "Citibank"
    detection_columns = []

    def detect(self, file_path: str | Path) -> bool:
        """Detect Citibank CSV by checking for card number in row 1, col 5."""
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                first_row = next(reader, None)

                if first_row and len(first_row) > 4:
                    col5 = first_row[4].strip()
                    card_num = col5.replace("'", "")
                    # Check for a numeric card pattern (15+ digits)
                    if card_num.isdigit() and len(card_num) >= 15:
                        # Optionally check if last 4 digits match a known card
                        return True
        except Exception:
            pass
        return False

    def get_card_number(self, file_path: str | Path) -> str | None:
        """Get the card number from the CSV file."""
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                first_row = next(reader, None)

                if first_row and len(first_row) > 4:
                    col5 = first_row[4].strip()
                    # Remove surrounding quotes
                    return col5.replace("'", "")
        except Exception:
            pass
        return None

    def get_account_type(self, file_path: str | Path) -> str | None:
        """Get the account type identifier based on card number.

        Returns the normalized account type (e.g., 'citi-premier-cc', 'citi-shared-cc')
        or None if not detected.
        """
        card_number = self.get_card_number(file_path)
        if card_number:
            last4 = card_number[-4:]
            if last4 in CITIBANK_CARD_MAP:
                return CITIBANK_CARD_MAP[last4]
        return None

    def parse(self, file_path: str | Path) -> list[Transaction]:
        """Parse Citibank CSV file."""
        transactions = []

        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            return transactions

        # Find the header row - look for a row with "Date" in it
        header_idx = None
        for i, row in enumerate(rows):
            row_lower = [c.lower().strip() for c in row]
            if "date" in row_lower:
                header_idx = i
                break

        if header_idx is not None:
            header_row = rows[header_idx]
            header_lower = [h.lower().strip() for h in header_row]
            date_idx = self._find_column(header_lower, ["date", "transaction date"])
            desc_idx = self._find_column(header_lower, ["description", "details", "particulars"])
            debit_idx = self._find_column(header_lower, ["debit", "withdrawal", "dr"])
            credit_idx = self._find_column(header_lower, ["credit", "deposit", "cr"])
            amount_idx = self._find_column(header_lower, ["amount"])
            data_rows = rows[header_idx + 1:]
        else:
            # No header row — Citibank CSV format: Date, Description, Debit, Credit, CardNumber
            date_idx = 0
            desc_idx = 1
            debit_idx = 2
            credit_idx = 3
            amount_idx = None
            data_rows = rows

        # Process transaction rows
        for row in data_rows:
            if not row:
                continue

            # Parse date
            date_str = ""
            if date_idx is not None and date_idx < len(row):
                date_str = row[date_idx].strip().replace('"', '')

            if not date_str:
                continue

            try:
                txn_date = parse_date(date_str, dayfirst=True).date()
            except (ValueError, TypeError):
                continue

            # Parse amount
            amount = 0.0

            # Try debit/credit columns first
            if debit_idx is not None and debit_idx < len(row):
                debit_str = row[debit_idx].replace(",", "").replace("$", "").replace('"', '').strip()
                if debit_str:
                    try:
                        amount = -abs(float(debit_str))
                    except ValueError:
                        pass

            if amount == 0 and credit_idx is not None and credit_idx < len(row):
                credit_str = row[credit_idx].replace(",", "").replace("$", "").replace('"', '').strip()
                if credit_str:
                    try:
                        amount = abs(float(credit_str))
                    except ValueError:
                        pass

            # Fallback to single amount column
            if amount == 0 and amount_idx is not None and amount_idx < len(row):
                amount_str = row[amount_idx].replace(",", "").replace("$", "").replace('"', '').strip()
                if amount_str:
                    try:
                        # For credit cards, positive usually means expense
                        amount = -float(amount_str)
                    except ValueError:
                        pass

            if amount == 0:
                continue

            # Get description
            payee = ""
            if desc_idx is not None and desc_idx < len(row):
                payee = row[desc_idx].strip().replace('"', '')
            if not payee:
                payee = "Citibank Transaction"
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
