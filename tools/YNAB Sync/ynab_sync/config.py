from __future__ import annotations

"""Configuration loading and validation."""

import os
import re
from pathlib import Path

import yaml
from pydantic import BaseModel, field_validator


class AccountConfig(BaseModel):
    """Configuration for a bank account mapping."""

    name: str
    bank: str
    ynab_account_id: str


class YNABConfig(BaseModel):
    """YNAB API configuration."""

    api_token: str
    budget_id: str = "default"


class Config(BaseModel):
    """Root configuration."""

    ynab: YNABConfig
    accounts: list[AccountConfig]

    def get_account(self, name: str) -> AccountConfig | None:
        """Get account config by name (case-insensitive)."""
        name_lower = name.lower()
        for account in self.accounts:
            if account.name.lower() == name_lower:
                return account
        return None

    def get_account_by_bank(self, bank: str) -> list[AccountConfig]:
        """Get all accounts for a bank."""
        bank_lower = bank.lower()
        return [acc for acc in self.accounts if acc.bank.lower() == bank_lower]


def _expand_env_vars(value: str) -> str:
    """Expand environment variables in a string.

    Supports ${VAR_NAME} syntax.
    """
    pattern = re.compile(r"\$\{([^}]+)\}")

    def replacer(match):
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))

    return pattern.sub(replacer, value)


def _expand_env_recursive(obj):
    """Recursively expand environment variables in a config dict."""
    if isinstance(obj, str):
        return _expand_env_vars(obj)
    elif isinstance(obj, dict):
        return {k: _expand_env_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_expand_env_recursive(item) for item in obj]
    return obj


def load_config(path: str | Path | None = None) -> Config:
    """Load configuration from YAML file.

    Args:
        path: Path to config file. If None, searches for:
            1. ./config.yaml
            2. ~/.config/ynab-sync/config.yaml

    Returns:
        Validated Config object

    Raises:
        FileNotFoundError: If no config file found
        ValueError: If config is invalid
    """
    if path is None:
        # Search default locations
        search_paths = [
            Path.cwd() / "config.yaml",
            Path.home() / ".config" / "ynab-sync" / "config.yaml",
        ]
        for p in search_paths:
            if p.exists():
                path = p
                break
        else:
            raise FileNotFoundError(
                f"No config file found. Searched: {[str(p) for p in search_paths]}"
            )
    else:
        path = Path(path)

    with open(path) as f:
        raw_config = yaml.safe_load(f)

    # Expand environment variables
    expanded = _expand_env_recursive(raw_config)

    return Config.model_validate(expanded)
