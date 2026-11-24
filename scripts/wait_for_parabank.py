"""Wait until ParaBank answers, then reset its data so every run starts the same way.
Usage: python scripts/wait_for_parabank.py [--timeout 180] [--no-reset]
"""
import argparse
import sys
import time
import requests
sys.path.insert(0, ".")
from config import API_URL, IS_LOCAL # noqa: E402
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--no-reset", action="store_true")
    args = parser.parse_args()

    deadline = time.time() + args.timeout
    url = f"{API_URL}/customers/12212"
    while time.time() < deadline:
        try:
            response = requests.get(url, headers={"Accept": "application/json"}, timeout=5)
            if response.status_code == 200:
                print("ParaBank is up")
                break
        except requests.RequestException:
            pass
        time.sleep(3)
    else:
        print(f"ParaBank did not answer within {args.timeout} s at {url}")
        return 1

    if IS_LOCAL and not args.no_reset:
        requests.post(f"{API_URL}/initializeDB", timeout=30).raise_for_status()
        print("Database reset to default data")
    return 0

if __name__ == "__main__":
    sys.exit(main())
