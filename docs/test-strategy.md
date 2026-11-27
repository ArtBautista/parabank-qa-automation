# Test Strategy · ParaBank QA Automation

## 1. Purpose

This strategy explains **what** is automated for ParaBank, **with which tool**, and **why**, so that
anyone joining the project can add tests the same way and trust what the pipeline reports.

## 2. Application under test

| Item | Detail |
|---|---|
| Application | ParaBank, Parasoft's demo online bank |
| UI | `http://localhost:8080/parabank/index.htm` |
| REST API | `http://localhost:8080/parabank/services/bank` (JSON with `Accept: application/json`) |
| Environment | Docker image `parasoft/parabank:latest`, one fresh container per CI job |
| Test data | Default customer **john / demo** (customer 12212), restored by `POST /initializeDB` |

## 3. Test pyramid and tool choices

| Layer | Tool | Share | Tests | Why this tool |
|---|---|---|---|---|
| API | Postman + Newman | ~40% | 17 requests, 50 assertions per pass | Fastest feedback on business rules and response contracts; Newman runs the same collection in CI |
| UI, page objects | Python, Selenium 4, pytest | ~35% | 23 | Critical customer journeys, run on Chrome and Firefox |
| UI + API, keywords | Robot Framework | ~15% | 10 | Plain-language tests that non-developers can read and review |
| Hybrid | `requests` setup + Selenium check | ~10% | 2 | Creates data through the API in milliseconds, then verifies it in the UI |

Most checks sit at the API layer because API tests are faster and less fragile. The UI layer covers
the journeys a customer actually clicks through.

## 4. Scope

**In scope:** login, registration, accounts overview, open account, transfer funds, bill pay,
request loan, find transactions, and the matching REST endpoints, including negative and boundary
cases (wrong password, unknown customer or account, missing or invalid amounts, oversized loans).

**Out of scope:** performance and load testing, security scanning, visual regression, mobile
browsers, and the admin and JMS pages. These are possible next steps, not part of this project.

## 5. Test design techniques

- **Equivalence partitioning and boundary values:** transfer amounts 0.01, 1, 10.50 and 250, plus
  empty and invalid input.
- **Positive and negative paths** for every feature.
- **Data-driven testing:** `postman/transfer-data.csv` runs the transfer flow once per amount.
- **State-based checks:** the balance before and after a transfer must differ by exactly the amount,
  and the transaction must appear in the history.
- **Traceability:** every case in `docs/test-cases.md` has an ID (PB-UI-xxx, PB-API-xxx, PB-HY-xxx,
  PB-RF-xxx) that appears in the test name or tags.

## 6. Framework rules

1. **Explicit waits only.** No `time.sleep`. ParaBank fills dropdowns with AJAX, so page objects wait
   for options (`wait_for_options`) and for the first *visible* element.
2. **Locators live in one place:** page-object classes for pytest, and the resource file for Robot.
3. **Every test owns its data.** Usernames are generated per test. Transfers and loans pick their
   source account at runtime, for example the account with the highest balance.
4. **Known state at the start of each run.** `scripts/wait_for_parabank.py` resets the local
   database. The reset is guarded so it never runs against the public site.
5. **Evidence on failure.** pytest saves a screenshot. Robot's log keeps every step. All reports are
   uploaded as pipeline artifacts, even when a job fails.
6. **No secrets in the repository.** Only the public demo account is committed. The public Postman
   environment keeps blank credentials.

## 7. Defect handling

- Defects are logged in `docs/defects/` with the [template](defect-report-template.md): severity,
  priority, steps, expected and actual result, and evidence.
- A test that fails because of a confirmed product defect is **kept, not deleted**, and marked as a
  known defect, so the pipeline stays green but the expected behaviour stays documented:

  | Framework | Mechanism |
  |---|---|
  | pytest | `@pytest.mark.xfail(reason="DEF-002 ...", strict=True)` |
  | Postman | `pm.test.skip` for the expected behaviour, plus a guard test that the defect still reproduces |
  | Robot Framework | tags `known-defect` and `robot:skip-on-failure` |

- When the product is fixed, the strict xfail or the guard test fails, which signals that the marker
  should be removed.
- **Current open defect:** DEF-002 (Medium / P2). An empty or invalid transfer amount gives an
  internal error in the UI and HTTP 500 from the API.

## 8. Flaky tests

A test that passes and fails on the same code is treated as a bug in the test. It is investigated
within one working day: it is either fixed (usually a missing wait or shared data) or quarantined
with a tag and a ticket. Retries are not used to hide flakiness.

## 9. CI/CD

| Trigger | What runs |
|---|---|
| Push or pull request to `main` | lint → API (Newman) → UI on Chrome and Firefox + Robot, in parallel |
| Nightly, 02:00 Manila time | full regression |
| Manual (`workflow_dispatch`) | full regression on demand |

- GitHub Actions is the live pipeline. `ci/Jenkinsfile` and `ci/.gitlab-ci.yml` are equivalent
  reference pipelines.
- Each job starts its own ParaBank service container, so jobs never share data.
- **Quality gate:** a pull request can merge only when lint and every test job pass. Known defects
  are reported as xfail or skipped, not as failures.

## 10. Entry and exit criteria

| | Criteria |
|---|---|
| **Entry** | ParaBank answers on `/services/bank/customers/12212`; the database has been reset; dependencies are installed |
| **Exit** | 100% of non-defect tests pass on Chrome and Firefox; every failure is either fixed or logged as a defect with evidence; reports are archived |

## 11. Reporting

| Suite | Report |
|---|---|
| pytest | `reports/pytest-report.html` plus JUnit XML and failure screenshots |
| Newman | `reports/newman-data-driven.html` (htmlextra) plus JUnit XML |
| Robot Framework | `reports/robot/report.html` and `log.html` |