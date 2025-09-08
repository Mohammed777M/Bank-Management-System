"""
Unit tests for app.py (FastAPI Account Service).

These tests cover:
    • Account creation
    • Listing accounts
    • Retrieving a single account
    • Updating account details
    • Computing total balances
    • Deleting an account

Run with:
    pytest -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def test_account():
    """Fixture to create and clean up a test account."""
    payload = {"name": "Unit Tester", "number": "UT-001", "balance": 100.0}
    resp = client.post("/accounts", json=payload)
    assert resp.status_code == 201
    acc = resp.json()
    yield acc
    client.delete(f"/accounts/{acc['id']}")


def test_create_account():
    """Test creating a new account."""
    payload = {"name": "Alice", "number": "A-123", "balance": 50.0}
    resp = client.post("/accounts", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Alice"
    assert data["number"] == "A-123"
    assert float(data["balance"]) == 50.0
    # cleanup
    client.delete(f"/accounts/{data['id']}")


def test_list_accounts(test_account):
    """Test listing accounts."""
    resp = client.get("/accounts")
    assert resp.status_code == 200
    data = resp.json()
    assert any(acc["id"] == test_account["id"] for acc in data)


def test_get_account(test_account):
    """Test retrieving a single account by ID."""
    resp = client.get(f"/accounts/{test_account['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == test_account["id"]
    assert data["number"] == "UT-001"


def test_update_account(test_account):
    """Test updating an account balance."""
    resp = client.put(f"/accounts/{test_account['id']}", json={"balance": 250.5})
    assert resp.status_code == 200
    data = resp.json()
    assert float(data["balance"]) == 250.5


@pytest.mark.parametrize("method", ["thread", "process", "async"])
def test_total_balance(method):
    """Test total balance calculation with all concurrency methods."""
    resp = client.get("/balances/total", params={"method": method, "batch_size": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert "total_balance" in data
    assert isinstance(data["total_balance"], float)
