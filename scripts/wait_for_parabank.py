"""Wait for ParaBank to start, initialise its database, and confirm the demo data exists.

A brand-new ParaBank container has an EMPTY database: the app answers, but the CUSTOMER
table does not exist until /initializeDB runs. So the order is:
  1. wait until the web server answers (any HTTP response from the home page)
  2. POST /initializeDB (only on your own container, never the public site)
  3. wait until the default customer 12212 (john / demo) can be read

Usage: python scripts/wait_for_parabank.py [--timeout 300] [--no-reset]
"""
import argparse
import sys
import time

import requests

sys.path.insert(0, ".")
from config import API_URL, BASE_URL, IS_LOCAL  # noqa: E402

JSON = {"Accept": "application/json"}


def poll(description, check, deadline, start):
    """Call check() every 3 s until it returns True or the deadline passes."""
    print(f"Waiting for {description}", flush=True)
    status, last_report = "no response yet", 0.0
    while time.time() < deadline:
        try:
            ok, status = check()
            if ok:
                print(f"  {description}: ready after {time.time() - start:.0f} s", flush=True)
                return True
        except requests.RequestException as error:
            status = type(error).__name__
        if time.time() - last_report >= 15:
            print(f"  {time.time() - start:4.0f} s: {status}", flush=True)
            last_report = time.time()
        time.sleep(3)
    print(f"Timed out waiting for {description} (last result: {status})", flush=True)
    return False


def server_answers():
    response = requests.get(f"{BASE_URL}/index.htm", timeout=5)
    return response.status_code == 200, f"HTTP {response.status_code}"


def initialize_db():
    response = requests.post(f"{API_URL}/initializeDB", timeout=60)
    return response.status_code in (200, 204), f"initializeDB HTTP {response.status_code}"


def demo_customer_exists():
    response = requests.get(f"{API_URL}/customers/12212", headers=JSON, timeout=5)
    return response.status_code == 200, f"customer 12212 HTTP {response.status_code}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--no-reset", action="store_true")
    args = parser.parse_args()

    start = time.time()
    deadline = start + args.timeout
    print(f"ParaBank: {BASE_URL}", flush=True)

    if not poll("the ParaBank web server", server_answers, deadline, start):
        return 1

    if IS_LOCAL and not args.no_reset:
        if not poll("database initialisation", initialize_db, deadline, start):
            return 1
        print("Database reset to default data", flush=True)

    if not poll("demo customer 12212 (john / demo)", demo_customer_exists, deadline, start):
        print("Hint: a fresh container needs /initializeDB. Run without --no-reset.")
        return 1

    print(f"ParaBank is up and ready after {time.time() - start:.0f} s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
