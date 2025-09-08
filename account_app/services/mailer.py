import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure your email credentials and SMTP server
SMTP_SERVER = "smtp.gmail.com"         # For Gmail
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your sender email
SENDER_PASSWORD = "your_app_password"  # Replace with your app-specific password

def send_email_notification(to_email, subject, body):
    # logic...

    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")
