# ParaBank Test Cases

Preconditions unless stated: local container running with reset data; signed in as `john`.
"Auto" shows where each case is automated: **Py** = pytest/Selenium, **PM** = Postman, **RF** = Robot Framework, **M** = manual.

## Login and registration
| ID | Title | Steps | Expected result | Priority | Auto |
|---|---|---|---|---|---|
| PB-UI-001 | Valid login | Enter john/demo, Log In | Accounts Overview; "Welcome John Smith" | P1 | Py, RF |
| PB-UI-002 | Wrong password | john / wrong password | "The username and password could not be verified." | P1 | Py, RF |
| PB-UI-003 | Unknown user | Unknown username | Same generic error | P1 | Py, RF |
| PB-UI-004 | Empty login | Click Log In with empty fields | "Please enter a username and password." | P2 | Py, RF |
| PB-UI-005 | Log out | Log in, click Log Out | Login form shown, no account menu | P1 | Py |
| PB-UI-006 | Back button after logout | Log out, press browser Back | Account data not usable without logging in | P2 | M |
| PB-UI-010 | Register new customer | Fill every field, Register | "Welcome username"; signed in | P1 | Py |
| PB-UI-011 | Password mismatch | Different confirm password | "Passwords did not match." | P2 | Py |
| PB-UI-012 | Duplicate username | Register same username twice | "This username already exists." | P2 | Py |
| PB-UI-013 | First name required | Leave First Name empty | "First name is required." | P2 | Py |
| PB-UI-014 | SSN required | Leave SSN empty | "Social Security Number is required." | P2 | Py |
| PB-UI-015 | Forgot login info | Use the lookup form with registered details | Username and password shown | P3 | M |

## Accounts
| ID | Title | Steps | Expected result | Priority | Auto |
|---|---|---|---|---|---|
| PB-UI-020 | Overview matches ledger | Compare table with API balances | Every id and balance matches | P1 | Py |
| PB-UI-021 | Open savings account | Type SAVINGS, Open New Account | New account number shown; API type SAVINGS | P1 | Py |
| PB-UI-022 | Open checking account | Type CHECKING | API type CHECKING | P2 | Py |
| PB-UI-023 | Account activity | Click an account number | Account details and transactions shown | P2 | M |
| PB-UI-024 | Total row | Check the Total row | Equals sum of balances | P2 | M |

## Transfers and bill pay
| ID | Title | Steps | Expected result | Priority | Auto |
|---|---|---|---|---|---|
| PB-UI-030 | Transfer between accounts | 25.50 from A to B | "Transfer Complete!"; A -25.50, B +25.50 | P1 | Py, RF |
| PB-UI-031 | Empty amount | Transfer with no amount | "The amount cannot be empty." | P2 | Py, RF |
| PB-UI-032 | Non-numeric amount | Amount "abc" | "Please enter a valid amount." | P2 | Py |
| PB-UI-033 | Same account both sides | From and To the same account | Should be rejected (check behaviour) | P2 | M |
| PB-UI-034 | Negative amount | Amount -10 | Should be rejected (check behaviour) | P1 | M |
| PB-UI-040 | Pay a bill | Valid payee and amount | "Bill Payment Complete"; payee named | P1 | Py |
| PB-UI-041 | Account mismatch | Different verify account | "The account numbers do not match." | P2 | Py |
| PB-UI-042 | Empty bill pay form | Send Payment with nothing filled | Required-field errors shown | P2 | Py |

## Loans and transactions
| ID | Title | Steps | Expected result | Priority | Auto |
|---|---|---|---|---|---|
| PB-UI-050 | Small loan approved | 100 with 10 down | Status "Approved"; new account number | P1 | Py |
| PB-UI-051 | Huge loan denied | 99,999,999 with 10 down | Status "Denied"; reason starts "We cannot grant a loan" | P1 | Py |
| PB-UI-052 | Down payment above funds | Down payment larger than balance | "You do not have sufficient funds for the given down payment." | P2 | M |
| PB-UI-060 | Find by amount | Transfer 7.77, search 7.77 | At least one result | P2 | Py |
| PB-UI-061 | Invalid transaction id | Search id "abc" | "Invalid transaction ID" | P3 | Py |
| PB-UI-062 | Find by date range | Search today to today | Today's transactions listed | P3 | M |

## REST API
| ID | Title | Request | Expected result | Priority | Auto |
|---|---|---|---|---|---|
| PB-API-001 | Login | GET /login/{user}/{pass} | 200; customer id saved | P1 | PM, RF |
| PB-API-002 | Login wrong password | GET /login/{user}/wrong | 4xx; no customer data | P1 | PM |
| PB-API-010 | Customer schema | GET /customers/{id} | 200; matches Customer schema | P1 | PM |
| PB-API-011 | Unknown customer | GET /customers/999999999 | 400 "Could not find customer #999999999" | P2 | PM, RF |
| PB-API-020 | List accounts | GET /customers/{id}/accounts | 200; array of Account; all owned by customer | P1 | PM, RF |
| PB-API-021 | Account by id | GET /accounts/{id} | 200; matches Account schema | P2 | PM |
| PB-API-022 | Create savings | POST /createAccount?newAccountType=1 | 200; type SAVINGS | P1 | PM, RF |
| PB-API-030..033 | Transfer chain | balance → transfer → balance → transactions | Balance drops by the amount; debit recorded | P1 | PM (data-driven) |
| PB-API-040 | Small loan | POST /requestLoan amount=100 | approved true | P1 | PM |
| PB-API-041 | Huge loan | POST /requestLoan amount=99999999 | approved false with message | P1 | PM |
| PB-API-050 | Transfer from unknown account | POST /transfer fromAccountId=999999999 | 4xx | P2 | PM |
| PB-API-051 | Transfer without amount | POST /transfer (no amount) | 4xx | P2 | PM |
| PB-API-052 | Unknown account | GET /accounts/999999999 | 400 | P2 | PM |

## Hybrid
| ID | Title | Steps | Expected result | Priority | Auto |
|---|---|---|---|---|---|
| PB-HY-001 | API account appears in UI | Create via API, open overview | New id listed | P2 | Py |
| PB-HY-002 | API transfer updates UI | Transfer via API, read overview | Balance reduced by the amount | P1 | Py |