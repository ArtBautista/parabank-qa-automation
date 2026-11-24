"""ParaBank REST API client (JSON). Used for test setup and for checking UI results."""
from decimal import Decimal
import requests

from config import API_URL

class ParaBankApi:

    def __init__(self, base_url=API_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _get(self, path):
        response = self.session.get(f"{self.base_url}{path}", timeout=15)
        response.raise_for_status()
        return response.json()

    def _post(self, path, **params):
        response = self.session.post(f"{self.base_url}{path}", params=params, timeout=15)
        response.raise_for_status()
        return response

    def login(self, username, password):
        """Returns the customer record, including its id."""
        return self._get(f"/login/{username}/{password}")

    def customer(self, customer_id):
            return self._get(f"/customers/{customer_id}")

    def accounts(self, customer_id):
        return self._get(f"/customers/{customer_id}/accounts")

    def account(self, account_id):
        return self._get(f"/accounts/{account_id}")

    def balance(self, account_id):
        return Decimal(str(self.account(account_id)["balance"])).quantize(Decimal("0.01"))

    def transactions(self, account_id):
        return self._get(f"/accounts/{account_id}/transactions")

    def transfer(self, from_account_id, to_account_id, amount):
        return self._post(
            "/transfer", fromAccountId=from_account_id, toAccountId=to_account_id, amount=amount
        )

    def create_account(self, customer_id, account_type, from_account_id):
        """account_type: 0 = CHECKING, 1 = SAVINGS."""
        return self._post(
            "/createAccount",
            customerId=customer_id,
            newAccountType=account_type,
            fromAccountId=from_account_id,
        ).json()

    def initialize_db(self):
        """Reset the database to ParaBank's default data (local container only)."""
        return self._post("/initializeDB")
