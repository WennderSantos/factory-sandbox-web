from decimal import Decimal

import pytest

from ledger_client import StatementLine, parse_statement
from ledger_client.export_format import format_line

ORG = "org-1"


@pytest.mark.parametrize("kind, amount", [("CREDIT", "10.50"), ("DEBIT", "5.00")])
def test_a_line_round_trips_through_parse_statement(kind, amount):
    line = StatementLine(ORG, "acc-1", kind, Decimal(amount), "salary")
    assert parse_statement(format_line(line), ORG) == [line]


def test_amount_keeps_two_places():
    line = StatementLine(ORG, "acc-1", "DEBIT", Decimal("5"), "fee")
    assert format_line(line) == "org-1;acc-1;DEBIT;5.00;fee"
    assert ";5.00;" in format_line(line)
    assert parse_statement(format_line(line), ORG)[0].amount.as_tuple().exponent == -2


@pytest.mark.parametrize("description, expected", [
    ("", ""), ("  ", ""), ("a;b", "a b"), ("a\nb", "a b"), ("a\r\nb", "a  b"),
])
def test_description_is_cleaned(description, expected):
    line = StatementLine(ORG, "acc-1", "CREDIT", Decimal("1"), description)
    assert format_line(line) == f"org-1;acc-1;CREDIT;1.00;{expected}"
