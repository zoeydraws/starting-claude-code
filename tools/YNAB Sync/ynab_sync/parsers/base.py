from __future__ import annotations

"""Base parser interface for bank CSV files."""

import csv
from abc import ABC, abstractmethod
from pathlib import Path

from ..models import Transaction


class BaseParser(ABC):
    """Abstract base class for bank CSV parsers."""

    # Subclasses should define these
    bank_name: str = "Unknown"
    # Column names or patterns to detect this bank's format
    detection_columns: list[str] = []

    @abstractmethod
    def parse(self, file_path: str | Path) -> list[Transaction]:
        """Parse a CSV file and return list of transactions.

        Args:
            file_path: Path to the CSV file

        Returns:
            List of Transaction objects
        """
        pass

    def detect(self, file_path: str | Path) -> bool:
        """Detect if this parser can handle the given CSV file.

        Default implementation checks if detection_columns are present.

        Args:
            file_path: Path to the CSV file

        Returns:
            True if this parser can handle the file
        """
        if not self.detection_columns:
            return False

        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                # Try to detect delimiter
                sample = f.read(4096)
                f.seek(0)

                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
                reader = csv.DictReader(f, dialect=dialect)

                if reader.fieldnames is None:
                    return False

                # Check if all detection columns are present
                fieldnames_lower = [name.lower().strip() for name in reader.fieldnames]
                for col in self.detection_columns:
                    if col.lower() not in fieldnames_lower:
                        return False
                return True
        except Exception:
            return False

    def _read_csv(self, file_path: str | Path) -> list[dict]:
        """Read CSV file and return list of row dicts."""
        rows = []
        with open(file_path, "r", encoding="utf-8-sig") as f:
            # Try to detect delimiter
            sample = f.read(4096)
            f.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                # Default to comma if detection fails
                dialect = csv.excel

            reader = csv.DictReader(f, dialect=dialect)
            for row in reader:
                # Strip whitespace from keys and values
                cleaned = {
                    k.strip(): v.strip() if isinstance(v, str) else v
                    for k, v in row.items()
                    if k is not None
                }
                rows.append(cleaned)
        return rows
