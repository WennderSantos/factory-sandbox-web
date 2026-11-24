# Review rules

Every pull request is checked against these rules. A violation of rules 1 to 4 blocks the merge.

1. Money is `decimal.Decimal`, built from text. Never `float`, not even for an intermediate result.
2. Every function that reads data of an organization takes `organization_id` and never returns rows of another one.
3. A parser rejects input it does not understand with `ValueError` that names the line. It never guesses and never skips a line in silence.
4. Every new behaviour has a test, including the input that must be refused.
5. Public functions have type hints and a one line docstring that says what they return.
6. No new dependency without a reason in the pull request. The package runs on the standard library.
