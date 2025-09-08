import requests

BASE_URL = "http://localhost:5000/api/accounts"

def create_account():
    name = input("Enter name: ")
    number = input("Enter number: ")
    balance = float(input("Enter balance: "))
    
    response = requests.post(BASE_URL, json={
        "name": name,
        "number": number,
        "balance": balance
    })
    print("✅ Response:", response.json())

def get_all_accounts():
    response = requests.get(BASE_URL)
    print("📋 Accounts List:")
    print(response.json())

def update_account():
    account_id = input("Enter account ID to update: ")
    name = input("Enter new name: ")
    number = input("Enter new number: ")
    balance = float(input("Enter new balance: "))

    response = requests.put(f"{BASE_URL}/{account_id}", json={
        "name": name,
        "number": number,
        "balance": balance
    })
    print("🛠️ Response:", response.json())

def delete_account():
    account_id = input("Enter account ID to delete: ")
    response = requests.delete(f"{BASE_URL}/{account_id}")
    print("❌ Response:", response.json())

def main():
    while True:
        print("\n📌 Menu:")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. Update Account")
        print("4. Delete Account")
        print("5. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            get_all_accounts()
        elif choice == "3":
            update_account()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            print("👋 Exiting.")
            break
        else:
            print("❗ Invalid choice.")

if __name__ == "__main__":
    main()
