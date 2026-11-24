"""Test settings. Every value can be overridden with an environment variable."""
import os
from urllib.parse import urlparse

BASE_URL = os.environ.get("PARABANK_URL", "http://localhost:8080/parabank").rstrip("/")
API_URL = f"{BASE_URL}/services/bank"
USERNAME = os.environ.get("PARABANK_USER", "john")
PASSWORD = os.environ.get("PARABANK_PASS", "demo")
TIMEOUT = float(os.environ.get("TIMEOUT", "15"))

# Resetting the database is only safe on your own local container, never on the public site.
IS_LOCAL = urlparse(BASE_URL).hostname in ("localhost", "127.0.0.1")
