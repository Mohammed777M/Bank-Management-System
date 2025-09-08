"""
Flask-based Account API with CRUD operations.

This module provides a simple RESTful API using the Flask framework.
It demonstrates how to manage accounts in memory with logging and
exception handling applied at both local and global levels.

Features:
    • Create, read, update, and delete accounts.
    • Each account stores:
        - number (str): Unique account number.
        - name (str): Account holder's name.
        - balance (float): Current balance (default: 0).
    • Logging for create, update, and delete operations.
    • Local exception handling inside each route.
    • Global error handler for unexpected errors.

How to Run:
    1. Install Flask if not installed:
        pip install flask
    2. Run the application:
        python app.py
    3. Access the API at:
        http://127.0.0.1:5000/

API Endpoints:
    - GET    /                → Welcome message
    - POST   /create          → Create a new account
    - GET    /read/<number>   → Retrieve account by number
    - PUT    /update/<number> → Update account details
    - DELETE /delete/<number> → Delete an account
"""

import logging
from flask import Flask, request, jsonify

# ---------------- Logging Setup ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------- Flask App ----------------
app = Flask(__name__)

# In-memory "database"
accounts = {}


# ---------------- Routes ----------------
@app.route("/")
def home():
    """
    Welcome route.

    Returns:
        Response: A JSON response with a welcome message.
    """
    return jsonify({"message": "Welcome to Account API"}), 200


@app.route("/create", methods=["POST"])
def create_account():
    """
    Create a new account with logging and error handling.

    Request JSON:
        {
            "name": "Alice",
            "number": "ACC123",
            "balance": 500.0
        }

    Returns:
        Response: JSON message indicating success or error.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        account_number = data.get("number")
        if not account_number:
            return jsonify({"error": "Account number is required"}), 400

        if account_number in accounts:
            return jsonify({"error": "Account already exists"}), 400

        accounts[account_number] = {
            "name": data.get("name"),
            "balance": data.get("balance", 0),
        }

        logger.info("Created account %s for %s", account_number, data.get("name"))
        return jsonify({"message": "Account created successfully"}), 201
    except Exception as exc:  # Catch unexpected errors
        logger.exception("Error in create_account: %s", exc)
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/read/<string:number>", methods=["GET"])
def read_account(number):
    """
    Read account details by account number.

    Args:
        number (str): The account number to look up.

    Returns:
        Response: JSON with account details or error message.
    """
    try:
        account = accounts.get(number)
        if not account:
            return jsonify({"error": "Account not found"}), 404
        return jsonify({"account": account}), 200
    except Exception as exc:
        logger.exception("Error in read_account: %s", exc)
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/update/<string:number>", methods=["PUT"])
def update_account(number):
    """
    Update account details.

    Args:
        number (str): The account number to update.

    Request JSON (any field optional):
        {
            "name": "New Name",
            "balance": 1000.0
        }

    Returns:
        Response: JSON message indicating success or error.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        account = accounts.get(number)
        if not account:
            return jsonify({"error": "Account not found"}), 404

        # Update fields
        account["name"] = data.get("name", account["name"])
        account["balance"] = data.get("balance", account["balance"])

        accounts[number] = account
        logger.info("Updated account %s", number)
        return jsonify({"message": "Account updated successfully"}), 200
    except Exception as exc:
        logger.exception("Error in update_account: %s", exc)
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/delete/<string:number>", methods=["DELETE"])
def delete_account(number):
    """
    Delete an account by account number.

    Args:
        number (str): The account number to delete.

    Returns:
        Response: JSON message indicating success or error.
    """
    try:
        if number not in accounts:
            return jsonify({"error": "Account not found"}), 404

        del accounts[number]
        logger.info("Deleted account %s", number)
        return jsonify({"message": "Account deleted successfully"}), 200
    except Exception as exc:
        logger.exception("Error in delete_account: %s", exc)
        return jsonify({"error": "Internal Server Error"}), 500


# ---------------- Global Error Handler ----------------
@app.errorhandler(Exception)
def handle_exception(error):
    """
    Global exception handler for unhandled errors.

    Args:
        error (Exception): The exception object.

    Returns:
        Response: JSON error message with HTTP 500 status.
    """
    logger.exception("Unhandled exception: %s", error)
    return jsonify({"error": "Something went wrong. Please try again later."}), 500


# ---------------- Main Entry ----------------
if __name__ == "__main__":
    app.run(debug=True)

