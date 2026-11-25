"""Currency helpers for the sandbox ledger."""


def is_foreign(account_currency: str, home_currency: str) -> bool:
    """Return True when the account currency differs from the home currency, ignoring case."""
    if home_currency is None:
        raise ValueError("home_currency is required")
    return account_currency.casefold() != home_currency.casefold()
