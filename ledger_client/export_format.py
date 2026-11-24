"""Writes one statement line in the form the ledger export uses."""

import re
from decimal import ROUND_HALF_UP, Decimal

from ledger_client.statement import StatementLine

_CENTS = Decimal("0.01")
_SEPARATORS = re.compile(r"[;\n\r]")


def format_line(line: StatementLine) -> str:
    """Return the line as `organization_id;account_id;kind;amount;description`, as ExportAccountStatementService writes it.

    The amount has two decimal places, a blank description is empty, and each `;`, newline or carriage return
    in the description becomes one space.
    """
    amount = line.amount.quantize(_CENTS, rounding=ROUND_HALF_UP)
    description = "" if not line.description.strip() else _SEPARATORS.sub(" ", line.description)
    return f"{line.organization_id};{line.account_id};{line.kind};{amount};{description}"
