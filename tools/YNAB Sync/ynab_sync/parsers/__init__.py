from __future__ import annotations

"""Bank CSV parsers."""

from .base import BaseParser
from .dbs import DBSParser
from .citibank import CitibankParser
from .uob import UOBParser
from .wise import WiseParser

PARSERS = {
    "dbs": DBSParser,
    "citibank": CitibankParser,
    "uob": UOBParser,
    "wise": WiseParser,
    # Specific UOB account types
    "uob-bank": UOBParser,
    "uob-one-cc": UOBParser,
    "uob-ppv-cc": UOBParser,
    "uob-ladies-cc": UOBParser,
    # Specific Citibank account types
    "citi-premier-cc": CitibankParser,
    "citi-shared-cc": CitibankParser,
}


def get_parser(bank: str) -> BaseParser:
    """Get parser instance for a bank."""
    parser_cls = PARSERS.get(bank.lower())
    if not parser_cls:
        raise ValueError(f"Unknown bank: {bank}. Available: {list(PARSERS.keys())}")
    return parser_cls()


def detect_bank(file_path: str) -> str | None:
    """Auto-detect bank from CSV file.

    Returns the base bank type (dbs, citibank, uob, wise).
    For specific account types within a bank, use detect_account_type().
    """
    for bank, parser_cls in [("dbs", DBSParser), ("citibank", CitibankParser),
                              ("uob", UOBParser), ("wise", WiseParser)]:
        parser = parser_cls()
        if parser.detect(file_path):
            return bank
    return None


def detect_account_type(file_path: str) -> str | None:
    """Auto-detect specific account type from file.

    Returns specific account type identifiers like:
    - 'uob-bank', 'uob-one-cc', 'uob-ppv-cc', 'uob-ladies-cc'
    - 'citi-premier-cc', 'citi-shared-cc'
    - 'dbs' (no subtypes)
    - 'wise' (no subtypes)

    Returns None if bank cannot be detected.
    """
    # Check DBS
    dbs_parser = DBSParser()
    if dbs_parser.detect(file_path):
        return "dbs"

    # Check Citibank (with card type)
    citi_parser = CitibankParser()
    if citi_parser.detect(file_path):
        account_type = citi_parser.get_account_type(file_path)
        return account_type if account_type else "citibank"

    # Check UOB (with card type)
    uob_parser = UOBParser()
    if uob_parser.detect(file_path):
        account_type = uob_parser.get_account_type(file_path)
        return account_type if account_type else "uob"

    # Check Wise
    wise_parser = WiseParser()
    if wise_parser.detect(file_path):
        return "wise"

    return None


__all__ = [
    "BaseParser",
    "DBSParser",
    "CitibankParser",
    "UOBParser",
    "WiseParser",
    "get_parser",
    "detect_bank",
    "detect_account_type",
]
