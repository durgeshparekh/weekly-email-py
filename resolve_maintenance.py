import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


load_dotenv()

# Email content
subject = "Voice Control Service Now Available"
body = """
Dear Smart Node Users,

We're delighted to inform you that our Voice Control Service is back up and running after a brief maintenance period of approximately 30 minutes.

You can now enjoy seamless voice control for your smart devices. If you need any assistance, please reach out to our customer support team at support@smartnode.in or +919327958743.

Thank you for your patience and for choosing Smart Node Automations.

Best Regards,
Smart Node Automations
"""

# Load recipient email addresses from a file
recipient_emails_file = "recipient_emails.txt"
with open(recipient_emails_file) as f:
    recipient_emails = f.read().splitlines()

# Sender's email and credentials
sender_email = os.getenv('SMTP_USERNAME')
smtp_server = os.getenv('SMTP_HOST')
smtp_port = 587
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')


# Function to send email to a recipient
def send_email(recipient_email, index):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

    print(f"Email sent to {index} :{recipient_email}")
    # Add a 5-second delay after sending each email
    time.sleep(1)


# Send the email to each recipient
for index, value in enumerate(recipient_emails):
    send_email(value, index)

