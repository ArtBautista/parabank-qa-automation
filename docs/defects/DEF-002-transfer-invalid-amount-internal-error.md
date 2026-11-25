# DEF-002: Transfer with an empty or non-numeric amount shows "An internal error has occurred"

| Field | Value |
|---|---|
| Severity | Medium |
| Priority | P2 |
| Environment | ParaBank local Docker (parasoft/parabank:latest), Chrome headless, user john |
| Component | Transfer Funds (UI + server validation) |
| Found by | Automated tests PB-UI-031, PB-UI-032 (`test_transfer_amount_validation`) |
| Status | New |

## Steps to reproduce
1. Log in as john / demo.
2. Open **Transfer Funds**.
3. Leave **Amount** empty (or type `abc`), keep the default From and To accounts.
4. Click **Transfer**.

## Expected result
The form stays open and shows the field message "The amount cannot be empty."
(or "Please enter a valid amount." for `abc`). No request reaches the server.

## Actual result
The form disappears and the page shows:
"Error! An internal error has occurred and has been logged."

## Evidence
- Test output: `AssertionError: ParaBank showed an error page: Error! An internal error has occurred and has been logged.`
- Both validation messages exist in the page's HTML (`p#amount.errors`) but are never displayed.
- Screenshots: `reports/screenshots/tests_ui_test_transfer.py__test_transfer_amount_validation*.png`

## Impact
Users get a generic error with no hint about what to fix, and invalid input reaches the
server, where it is only caught as an unhandled exception. Reproducible every time.

## Notes
Suspected cause: client-side validation not wired to the submit handler, and no server-side
validation returning a 400 with a clear message.

## API evidence (Day 3)

The defect also reproduces through the REST API, so it is in the service layer, not just the UI form.

| Field | Value |
|---|---|
| Request | `POST {{baseUrl}}/transfer?fromAccountId=12345&toAccountId=12456` (no `amount`) |
| Expected | HTTP 400 with a validation message such as "amount is required" |
| Actual | HTTP 500 Internal Server Error |
| Test case | PB-API-051 (`postman/ParaBank.postman_collection.json`, folder 06 Negative) |
| Reproducibility | 4/4 Newman iterations (`-d postman/transfer-data.csv`) |
| Handling | Expected-behaviour test kept with `pm.test.skip`; a guard test asserts the 500 still occurs and fails once the bug is fixed |