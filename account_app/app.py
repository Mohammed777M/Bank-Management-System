from flask import Flask, jsonify, request # type: ignore
from models.account import (
    create_account,
    get_accounts,
    get_account_by_id,
    update_account,
    delete_account
)
from services.balance_calculator import calculate_total_balance_threaded
from services.interest_scraper import fetch_interest_rates  # import scraper module
from services.mailer import send_email_notification


app = Flask(__name__)

# Create Account
@app.route('/accounts', methods=['POST'])
def create_account_route():
    try:
        data = request.get_json()
        name = data.get('name')
        number = data.get('number')
        balance = data.get('balance')


        if not all([name, number, balance is not None]):
            return jsonify({"error": "Missing required fields"}), 400

        account_id = create_account(name, number, balance)

        # Send email notification (make sure send_email_notification takes recipient email if needed)
        recipient_email = "recipient@example.com"  # Replace with actual email logic
        send_email_notification(name, number, balance, recipient_email)

        return jsonify({"message": "Account created", "id": account_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all accounts
@app.route('/accounts', methods=['GET'])
def get_accounts_route():
    try:
        accounts = get_accounts()
        return jsonify(accounts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get account by ID
@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account_route(account_id):
    account = get_account_by_id(account_id)
    if account:
        return jsonify(account), 200
    return jsonify({"error": "Account not found"}), 404

# Update account
@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account_route(account_id):
    data = request.get_json()
    name = data.get('name')
    number = data.get('number')
    balance = data.get('balance')
    if not all([name, number, balance is not None]):
        return jsonify({"error": "Missing required fields"}), 400

    updated = update_account(account_id, name, number, balance)
    if updated:
        return jsonify({"message": "Account updated"}), 200
    return jsonify({"error": "Account not found"}), 404

# Delete account
@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account_route(account_id):
    deleted = delete_account(account_id)
    if deleted:
        return jsonify({"message": "Account deleted"}), 200
    return jsonify({"error": "Account not found"}), 404

# Total balance - multi-threaded calculation
@app.route('/total-balance', methods=['GET'])
def total_balance_route():
    try:
        total = calculate_total_balance_threaded()
        return jsonify({'total_balance': total}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Scrape interest rates

@app.route('/interest-rates', methods=['GET'])
def interest_rate_route():
    rates = fetch_interest_rates()
    if rates:
        return jsonify({"interest_rates": rates}), 200
    else:
        return jsonify({"error": "Unable to fetch interest rates"}), 500
    
@app.route('/register', methods=['POST'])
def register_user():
    # Assume registration logic here...
    
    # Send welcome email
    send_email_notification(
        "user@example.com",
        "Welcome!",
        "Thank you for registering with us."
    )
    
    return jsonify({"message": "User registered and email sent"})



if __name__ == '__main__':
    app.run(debug=True)
