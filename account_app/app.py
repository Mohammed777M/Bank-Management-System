"""
Flask-based Account API with CRUD operations.

This demo uses an in-memory dictionary as a database. 
Includes logging and exception handling at both local
and global levels.
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
    """Welcome route."""
    return jsonify({"message": "Welcome to Account API"}), 200


@app.route("/create", methods=["POST"])
def create_account():
    """Create a new account with logging and error handling."""
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
    """Read account details by number."""
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
    """Update account details."""
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
    """Delete an account by number."""
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
    """Global exception handler for unhandled errors."""
    logger.exception("Unhandled exception: %s", error)
    return jsonify({"error": "Something went wrong. Please try again later."}), 500


# ---------------- Main Entry ----------------
if __name__ == "__main__":
    app.run(debug=True)
