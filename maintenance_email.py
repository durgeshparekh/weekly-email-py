import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from pymysql import connect


load_dotenv()

# Email content
subject = "Voice Control Service Upgrade Notification"
body = """
Dear Smart Home Users,

We're excited to inform you that we're upgrading our Voice Control Service to provide you with an even better smart home experience.

Maintenance Schedule:
- Date: 3rd Oct 2023
- Time: 3:00 PM to 3:30 PM (approximately 30 minutes)

During this time, the Voice Control Service will be temporarily offline. We apologize for any inconvenience and suggest using the Smart Node mobile app to control your devices during this brief upgrade.

We appreciate your cooperation and thank you for choosing Smart Node Automations.

Best Regards,
Smart Node Automations
"""

# Load recipient email addresses from a file
recipient_emails_file = "recipient_emails.csv"
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


# Retrieve user data from MySQL and store in user_data.txt
def retrieve_user_data():
    db_port = 3306
    db = connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=db_port
    )

    cursor = db.cursor()
    cursor.execute(
        ""
        "SELECT DISTINCT vw_userDetail.email,vw_userDetail.firstName,vw_userDetail.lastName "
        "FROM vw_userDetail "
        "INNER JOIN vw_deviceDetail "
        "ON vw_deviceDetail.userId = vw_userDetail.userId"
        ""
    )

    users = cursor.fetchall()

    with open(recipient_emails_file, "w") as file:
        file.write("Email, First Name, Last Name\n")
        for user in users:
            file.write(f"{user[0]}, {user[1]}, {user[2]}\n")

    db.close()


# Retrieve user data and send emails
retrieve_user_data()

# Send the email to each recipient
# for index, value in enumerate(recipient_emails):
#     send_email(value, index)
