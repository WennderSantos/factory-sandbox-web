# factory-sandbox-web

A tiny Python package used to try out a software factory on a second repository. It reads the statement export of
the ledger in `WennderSantos/factory-sandbox` and turns it into Python values a web page could show.

Nothing here is real. There are no customers, no money and no secrets.

This sandbox is owned by Wennder Santos.

## Layout

- `ledger_client/`: the package. `statement.py` parses one exported statement.
- `tests/`: pytest tests.
- `REVIEW.md`: the rules a pull request is reviewed against.

## Run the tests

```bash
python -m pip install pytest
python -m pytest -q
```

## CI and deploy

`ci` runs the tests on every pull request (job `test`). `deploy` is a stand-in for a real deploy: it runs on every
merge to `main` and fails when the merge commit message contains `DEPLOY_FAILS`.
