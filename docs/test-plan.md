# Test Plan - ParaBank

## 1. Scope
In scope: registration, login/logout, Accounts Overview, Open New Account, Transfer Funds,
Bill Pay, Find Transactions, Request Loan, Update Contact Info, and the REST (JSON) API under
`/parabank/services/bank`.
Out of scope: SOAP/XML services, stock positions, the Admin page, JMS and LoanProcessor settings.

## 2. Environments
| Environment | URL | Use |
|---|---|---|
| Local (Docker) | http://localhost:8080/parabank | All automation and CI. Data reset before each run. |
| Public demo | https://parabank.parasoft.com/parabank | Exploratory testing only. Shared data, never reset it. |

## 3. Risks and priorities
| Risk | Likelihood | Impact | Priority | Covered by |
|---|---|---|---|---|
| Transfer moves the wrong amount or the wrong accounts | Medium | High | P1 | PB-UI-030, PB-API-031..033, PB-RF-010 |
| Balances on screen differ from the ledger | Medium | High | P1 | PB-UI-020, PB-HY-002 |
| Anyone can log in or reach account pages | Low | High | P1 | PB-UI-002..005, PB-API-002 |
| Invalid amounts accepted | Medium | Medium | P2 | PB-UI-031..032, PB-API-050..051 |
| Loans approved without funds | Medium | High | P1 | PB-UI-051, PB-API-041 |
| Registration accepts bad or duplicate data | Medium | Medium | P2 | PB-UI-011..014 |
| Cross-browser rendering issues | Low | Low | P3 | UI suite on Chrome + Firefox |

## 4. Test levels and tools
| Level | Tool | When |
|---|---|---|
| API | Postman collection, run with Newman | Every push |
| UI | pytest + Selenium (Page Object Model) | Every push, Chrome + Firefox |
| UI + API, keyword-driven | Robot Framework (SeleniumLibrary, RequestsLibrary) | Every push |
| Hybrid | API for setup, UI for checks | Every push |
| Exploratory | Manual, public demo | Each new feature |

## 5. Entry and exit criteria
Entry: container starts, `GET /customers/12212` returns 200. Exit: all P1 tests pass,
no open Critical/High defects, every pipeline job green.

## 6. Estimate
| Activity | Hours |
|---|---|
| Exploration and test design | 5 |
| Selenium page objects and tests | 7 |
| Postman collection | 4 |
| Robot Framework suites | 3 |
| CI/CD pipeline | 3 |