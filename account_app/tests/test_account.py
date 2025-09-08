from models.account import create_account

def test_create_account():
    create_account("Test User", "12345678", 5000.00)
    # Add assert and read logic here