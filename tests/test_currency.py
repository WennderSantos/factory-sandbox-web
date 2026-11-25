import pytest

from ledger_client import is_foreign


def test_different_currencies_are_foreign():
    assert is_foreign("USD", "EUR") is True


@pytest.mark.parametrize("account,home", [("USD", "USD"), ("usd", "USD"), ("USD", "usd")])
def test_same_currency_ignoring_case_is_not_foreign(account, home):
    assert is_foreign(account, home) is False


def test_none_home_currency_is_refused():
    with pytest.raises(ValueError):
        is_foreign("USD", None)
