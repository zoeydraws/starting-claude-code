from __future__ import annotations

"""YNAB API client."""

import httpx

from .models import Transaction


class YNABError(Exception):
    """YNAB API error."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class YNABClient:
    """Client for YNAB API."""

    BASE_URL = "https://api.ynab.com/v1"

    def __init__(self, api_token: str):
        """Initialize client with API token."""
        self.api_token = api_token
        self._client = httpx.Client(
            base_url=self.BASE_URL,
            headers={"Authorization": f"Bearer {api_token}"},
            timeout=30.0,
        )

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """Make API request."""
        response = self._client.request(method, path, **kwargs)

        if response.status_code >= 400:
            try:
                error_data = response.json()
                message = error_data.get("error", {}).get("detail", response.text)
            except Exception:
                message = response.text
            raise YNABError(message, response.status_code)

        return response.json()

    def get_budgets(self) -> list[dict]:
        """Get list of budgets.

        Returns:
            List of budget objects with id, name, etc.
        """
        data = self._request("GET", "/budgets")
        return data.get("data", {}).get("budgets", [])

    def get_accounts(self, budget_id: str) -> list[dict]:
        """Get list of accounts for a budget.

        Args:
            budget_id: Budget ID (use 'default' for default budget)

        Returns:
            List of account objects with id, name, type, balance, etc.
        """
        data = self._request("GET", f"/budgets/{budget_id}/accounts")
        return data.get("data", {}).get("accounts", [])

    def create_transactions(
        self,
        budget_id: str,
        account_id: str,
        transactions: list[Transaction],
    ) -> dict:
        """Create transactions in YNAB.

        Args:
            budget_id: Budget ID
            account_id: Account ID to add transactions to
            transactions: List of Transaction objects

        Returns:
            API response with created/duplicate transaction info
        """
        payload = {
            "transactions": [
                txn.to_ynab_dict(account_id) for txn in transactions
            ]
        }

        data = self._request(
            "POST",
            f"/budgets/{budget_id}/transactions",
            json=payload,
        )

        return data.get("data", {})

    def get_transaction_count(self, budget_id: str, account_id: str) -> int:
        """Get count of transactions for an account."""
        data = self._request(
            "GET",
            f"/budgets/{budget_id}/accounts/{account_id}/transactions",
        )
        return len(data.get("data", {}).get("transactions", []))

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
