from decimal import Decimal

import pytest

from ledger_client import parse_statement, total

ORG = "org-1"


def test_parses_a_credit_and_a_debit():
    lines = parse_statement("org-1;acc-1;CREDIT;10.50;salary\norg-1;acc-1;DEBIT;0.50;fee\n", ORG)
    assert [line.kind for line in lines] == ["CREDIT", "DEBIT"]
    assert lines[0].amount == Decimal("10.50")


def test_total_is_credits_minus_debits():
    lines = parse_statement("org-1;acc-1;CREDIT;10.50;salary\norg-1;acc-1;DEBIT;0.50;fee\n", ORG)
    assert total(lines) == Decimal("10.00")


def test_empty_lines_are_allowed():
    assert parse_statement("\n\norg-1;acc-1;CREDIT;1;x\n\n", ORG)[0].amount == Decimal("1")


def test_a_line_of_another_organization_is_refused():
    with pytest.raises(ValueError, match="line 1: belongs to another organization"):
        parse_statement("org-2;acc-9;CREDIT;1;x", ORG)


@pytest.mark.parametrize("line, message", [
    ("org-1;acc-1;CREDIT;1", "line 1: expected 5 fields, got 4"),
    ("org-1;acc-1;REFUND;1;x", "line 1: unknown kind 'REFUND'"),
    ("org-1;acc-1;CREDIT;ten;x", "line 1: amount 'ten' is not a number"),
    ("org-1;acc-1;CREDIT;0;x", "line 1: amount must be above zero"),
])
def test_bad_lines_are_refused_with_the_line_number(line, message):
    with pytest.raises(ValueError, match=message.replace("'", "'")):
        parse_statement(line, ORG)
