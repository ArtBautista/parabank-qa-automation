# ParaBank QA Automation

[![QA Pipeline](https://github.com/ArtBautista/parabank-qa-automation/actions/workflows/qa-pipeline.yml/badge.svg?branch=main)](https://github.com/ArtBautista/parabank-qa-automation/actions/workflows/qa-pipeline.yml)

End-to-end test automation for **[ParaBank](https://parabank.parasoft.com)**, Parasoft's demo online bank:
UI tests with Selenium and the Page Object Model, API tests with Postman and Newman, keyword-driven tests
with Robot Framework, and a CI pipeline that runs every suite against a fresh ParaBank Docker container
on each push.

## Results at a glance

| Suite | Tools | Scope | Latest local result |
|---|---|---|---|
| UI (page objects) | Python 3.11, Selenium 4, pytest, pytest-html | 23 tests · login, registration, accounts, transfers, bill pay, loans, transactions | **21 passed, 2 xfailed** (DEF-002) |
| Hybrid | API setup + UI verification | 2 tests | run with `pytest -m hybrid` |
| API | Postman, Newman, htmlextra | 17 requests · 50 assertions per pass · CSV data-driven (4 amounts) | **4 iterations, 0 failed** (DEF-002 skipped) |
| Keyword-driven | Robot Framework, SeleniumLibrary, RequestsLibrary | 10 tests · tagged `smoke`, `ui`, `api`, `negative` | **9 passed, 1 skipped** (DEF-002) |
| CI/CD | GitHub Actions, Jenkinsfile, GitLab CI | lint → API → UI (Chrome + Firefox) + Robot | runs on push, PR, nightly 02:00 PHT |

**46 documented test cases** (31 UI, 13 API, 2 hybrid) are traced to automated tests in
[docs/test-cases.md](docs/test-cases.md).

## Defect found

**[DEF-002](docs/defects/DEF-002-transfer-invalid-amount-internal-error.md) · Medium / P2:**
Transfer Funds with an empty or invalid amount shows *"An internal error has occurred"* in the UI,
and the REST API returns **HTTP 500** instead of a 400 validation error. Reproduced 4/4 in Newman.
The tests that expect the correct behaviour are kept and marked as known defects
(`xfail(strict=True)` in pytest, `pm.test.skip` plus a guard test in Postman, `robot:skip-on-failure`
in Robot), so the pipeline stays green and flags the moment the bug is fixed.

## Architecture

```text
                    ┌──────────────────────── GitHub Actions ────────────────────────┐
  git push ───────► │  lint ──► api-tests ──┬──► ui-tests (chrome)                   │
                    │  (ruff)   (Newman)    ├──► ui-tests (firefox)                  │
                    │                       └──► robot-tests                         │
                    └───────────────┬────────────────────────────────────────────────┘
                                    │ service container
                                    ▼
                    ParaBank (parasoft/parabank) :8080
                    ├── UI   /parabank/index.htm        ◄── Selenium page objects, SeleniumLibrary
                    └── API  /parabank/services/bank    ◄── Newman, requests, RequestsLibrary
```

## Project structure

```text
parabank-qa-automation/
├── config.py                     URLs, credentials and timeouts from environment variables
├── framework/api_client.py       requests wrapper used for setup and hybrid tests
├── pages/                        Page Object Model: one class per ParaBank screen
├── tests/
│   ├── conftest.py               driver, api and login fixtures; screenshot on failure
│   ├── ui/                       Selenium tests
│   └── hybrid/                   API setup + UI verification
├── postman/                      collection, local/public environments, transfer-data.csv
├── robot/
│   ├── resources/parabank.resource   shared keywords and variables
│   └── tests/                    login, transfer and API suites
├── scripts/wait_for_parabank.py  waits for ParaBank, then resets the local database
├── docs/                         test plan, test cases, strategy, defect reports
├── ci/                           Jenkinsfile and .gitlab-ci.yml (reference pipelines)
├── .github/workflows/qa-pipeline.yml
└── docker-compose.yml
```

## Run locally (Windows PowerShell)

Prerequisites: Docker Desktop, Python 3.11, Node.js 20, Google Chrome.

```powershell
# 1. Start ParaBank and set up Python
docker compose up -d
py -3.11 -m venv .venv --prompt parabank
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
npm install -g newman newman-reporter-htmlextra

# 2. Wait for ParaBank and reset to default data (john / demo)
python scripts/wait_for_parabank.py

# 3. Selenium + pytest (HTML report)
python -m pytest --headless --html=reports/pytest-report.html --self-contained-html

# 4. Postman via Newman, data-driven
newman run postman/ParaBank.postman_collection.json -e postman/local.postman_environment.json -d postman/transfer-data.csv -r "cli,htmlextra" --reporter-htmlextra-export reports/newman-data-driven.html

# 5. Robot Framework
robot --outputdir reports/robot --variable BROWSER:headlesschrome robot/tests
```

Useful options: `python -m pytest --browser firefox`, `python -m pytest -m hybrid`,
`robot --include smoke robot/tests`. Reports are written to `reports/` (git-ignored); in CI they
are uploaded as build artifacts.

> The database reset only runs against `localhost`. It is never called on the public ParaBank site.

## Documentation

- [Test plan](docs/test-plan.md): scope, environments, entry and exit criteria, risks
- [Test cases](docs/test-cases.md): 46 cases with IDs, steps, expected results and automation status
- [Test strategy](docs/test-strategy.md): test pyramid, tool choices, data, flakiness and CI rules
- [Defect report template](docs/defect-report-template.md) and [defects](docs/defects/)

## Author

**Art Bautista** · QA Engineer · [LinkedIn](https://www.linkedin.com/in/art-bautista-39b3b1299/)