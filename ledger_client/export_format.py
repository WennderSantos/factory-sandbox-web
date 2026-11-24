"""Writes one statement line in the form the ledger export uses."""

import re
from decimal import Decimal, InvalidOperation

from ledger_client.statement import KINDS, StatementLine

_CENTS = Decimal("0.01")
# ; and every character str.splitlines() breaks on, so a written line always parses back.
_SEPARATORS = re.compile("[;\n\r\x0b\x0c\x1c-\x1e\x85  ]")


def _field(name: str, value: str) -> str:
    if _SEPARATORS.search(value):
        raise ValueError(f"{name} must not contain ';' or a line break")
    if value != value.strip():
        raise ValueError(f"{name} must not start or end with whitespace")
    return value


def format_line(line: StatementLine) -> str:
    """Return the line as organizationId;accountId;kind;amount;description, as ExportAccountStatementService writes it."""
    # Refusals below (ids, kind, amount) go beyond the Java export; they only keep the line parseable.
    if line.kind not in KINDS:
        raise ValueError(f"unknown kind {line.kind!r}")
    if not line.amount.is_finite() or line.amount <= 0:
        raise ValueError("amount must be above zero")
    try:
        amount = line.amount.quantize(_CENTS)
    except InvalidOperation as error:
        raise ValueError("amount is too large") from error
    if amount != line.amount:
        raise ValueError("amount must have at most two decimal places")
    organization_id = _field("organization_id", line.organization_id)
    account_id = _field("account_id", line.account_id)
    description = "" if not line.description.strip() else _SEPARATORS.sub(" ", line.description)
    return f"{organization_id};{account_id};{line.kind};{amount};{description}"
