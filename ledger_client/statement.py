"""One exported statement: text lines in, typed lines out."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

KINDS = ("CREDIT", "DEBIT")


@dataclass(frozen=True)
class StatementLine:
    """One entry of an account statement."""

    organization_id: str
    account_id: str
    kind: str
    amount: Decimal
    description: str


def parse_statement(text: str, organization_id: str) -> list[StatementLine]:
    """Return the lines of one statement that belong to the organization.

    Each line is `organization_id;account_id;kind;amount;description`. Empty lines are allowed. A line of
    another organization is an error, not something to drop: a statement is exported for one organization.
    """
    lines = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip():
            continue
        parts = raw.split(";")
        if len(parts) != 5:
            raise ValueError(f"line {number}: expected 5 fields, got {len(parts)}")
        org, account, kind, amount, description = (part.strip() for part in parts)
        if org != organization_id:
            raise ValueError(f"line {number}: belongs to another organization")
        if kind not in KINDS:
            raise ValueError(f"line {number}: unknown kind {kind!r}")
        try:
            value = Decimal(amount)
        except InvalidOperation as error:
            raise ValueError(f"line {number}: amount {amount!r} is not a number") from error
        if value <= 0:
            raise ValueError(f"line {number}: amount must be above zero")
        lines.append(StatementLine(org, account, kind, value, description))
    return lines


def total(lines: list[StatementLine]) -> Decimal:
    """Return credits minus debits."""
    result = Decimal("0")
    for line in lines:
        result += line.amount if line.kind == "CREDIT" else -line.amount
    return result
