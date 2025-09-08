import smtplib
from email.message import EmailMessage

def send_account_email(to_email, account_name):
    msg = EmailMessage()
    msg.set_content(f"Account for {account_name} has been created.")
    msg["Subject"] = "New Account Created"
    msg["From"] = "from"
    msg["To"] = "to"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your_email@example.com", "your_password")
            server.send_message(msg)
    except Exception as e:
        print("Email failed:", e)