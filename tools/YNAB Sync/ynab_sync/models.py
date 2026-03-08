from __future__ import annotations

"""Data models for YNAB transactions."""

from datetime import date
from hashlib import md5
from pydantic import BaseModel, Field, computed_field


class Transaction(BaseModel):
    """A transaction in YNAB format."""

    date: date
    amount: int = Field(description="Amount in milliunits (amount * 1000)")
    payee_name: str = Field(max_length=100)
    memo: str | None = Field(default=None, max_length=200)

    @computed_field
    @property
    def import_id(self) -> str:
        """Generate unique import ID for deduplication.

        YNAB uses import_id to prevent duplicate imports.
        Format: YNAB:{amount}:{date}:{hash}
        """
        unique_str = f"{self.date.isoformat()}:{self.amount}:{self.payee_name}"
        hash_suffix = md5(unique_str.encode()).hexdigest()[:8]
        return f"YNAB:{self.amount}:{self.date.isoformat()}:{hash_suffix}"

    def to_ynab_dict(self, account_id: str) -> dict:
        """Convert to YNAB API format."""
        result = {
            "account_id": account_id,
            "date": self.date.isoformat(),
            "amount": self.amount,
            "payee_name": self.payee_name,
            "import_id": self.import_id,
        }
        if self.memo:
            result["memo"] = self.memo
        return result

    @classmethod
    def from_amount(
        cls,
        date: date,
        amount: float,
        payee_name: str,
        memo: str | None = None,
    ) -> "Transaction":
        """Create transaction from regular amount (converts to milliunits)."""
        return cls(
            date=date,
            amount=int(amount * 1000),
            payee_name=payee_name,
            memo=memo,
        )
