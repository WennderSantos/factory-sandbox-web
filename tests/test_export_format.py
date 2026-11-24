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


@pytest.mark.parametrize("amount", ["1.005", "0.001", "0", "-1", "NaN"])
def test_a_refused_amount_raises(amount):
    line = StatementLine(ORG, "acc-1", "CREDIT", Decimal(amount), "x")
    with pytest.raises(ValueError):
        format_line(line)


@pytest.mark.parametrize("field", ["organization_id", "account_id", "kind"])
@pytest.mark.parametrize("bad", ["a;b", "a\nb", "CREDIT\nother"])
def test_ids_and_kind_cannot_forge_fields_or_lines(field, bad):
    values = {"organization_id": ORG, "account_id": "acc-1", "kind": "CREDIT"}
    values[field] = bad
    with pytest.raises(ValueError):
        format_line(StatementLine(amount=Decimal("1"), description="x", **values))


@pytest.mark.parametrize("sep", ["\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", " ", " "])
def test_unicode_line_breaks_in_description_round_trip(sep):
    line = StatementLine(ORG, "acc-1", "CREDIT", Decimal("1.00"), "a b")
    text = format_line(StatementLine(ORG, "acc-1", "CREDIT", Decimal("1.00"), f"a{sep}b"))
    assert parse_statement(text, ORG) == [line]
