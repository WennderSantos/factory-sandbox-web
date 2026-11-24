"""Writes one statement line in the form the ledger export uses."""

import re
from decimal import Decimal

from ledger_client.statement import KINDS, StatementLine

_CENTS = Decimal("0.01")
# ; and every character str.splitlines() breaks on, so a written line always parses back.
_SEPARATORS = re.compile("[;\n\r\x0b\x0c\x1c-\x1e\x85  ]")


def _field(name: str, value: str) -> str:
    if _SEPARATORS.search(value):
        raise ValueError(f"{name} must not contain ';' or a line break")
    return value


def format_line(line: StatementLine) -> str:
    """Return the line as `organization_id;account_id;kind;amount;description`, as ExportAccountStatementService writes it.

    The amount has two decimal places, a blank description is empty, and each `;` or line break in the
    description becomes one space. Like the Java ledger entry, it refuses an amount that is not above zero or
    has more than two decimal places, an unknown kind, and an id or kind holding `;` or a line break.
    """
    if line.kind not in KINDS:
        raise ValueError(f"unknown kind {line.kind!r}")
    if not line.amount.is_finite() or line.amount <= 0:
        raise ValueError("amount must be above zero")
    amount = line.amount.quantize(_CENTS)
    if amount != line.amount:
        raise ValueError("amount must have at most two decimal places")
    organization_id = _field("organization_id", line.organization_id)
    account_id = _field("account_id", line.account_id)
    description = "" if not line.description.strip() else _SEPARATORS.sub(" ", line.description)
    return f"{organization_id};{account_id};{line.kind};{amount};{description}"
