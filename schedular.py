import os
import schedule
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from time import sleep
from pymysql import connect
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pytz import timezone


# variables
execution_time = '11:01'
time_zone = 'Asia/Kolkata'
time_format = "%H:%M"


def send_email(csv_file_path):
    try:
        # List of recipient email addresses
        recipient_emails = ['durgeshparekh381@gmail.com']

        # Set up email parameters
        sender_name = "Durgesh Parekh"
        sender_email = "no-reply@smartnode.in"
        subject = "Weekly User Data Details"
        body = "Hi,\n\n"
        body += "Please find attached the weekly user data details.\n\n"
        body += "Best regards,\n" + sender_name

        message = MIMEMultipart()
        message["From"] = sender_email
        message["Subject"] = subject

        message.attach(MIMEText(body, 'plain'))

        # Attach the CSV file
        attachment = open(csv_file_path, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=csv_file_path.split("/")[-1])
        message.attach(part)

        # Send the email
        smtp_server = os.getenv('SMTP_HOST')
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            message["To"] = ", ".join(recipient_emails)
            server.sendmail(sender_email, recipient_emails, message.as_string())

        print("Weekly email sent successfully!")

    except Exception as e:
        print("Error sending email: ",str(e))


def generate_user_data():
    # Connect to MySQL database
    db_port = 3306

    db = connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=db_port
    )

    # Retrieve user data from MySQL
    cursor = db.cursor()
    # cursor.execute("SELECT firstName, lastName, mobile, email FROM AppUser")
    cursor.execute("SELECT DISTINCT firstName, lastName, mobile, email FROM AppUser "
                   "INNER JOIN AppDevice ON AppDevice.userId = AppUser.userId "
                   "AND AppUser.isActive = 1 AND AppDevice.isActive = 1;")

    users = cursor.fetchall()
    # Close the database connection
    db.close()

    # Prepare CSV file
    csv_file_path = "user_data.csv"

    with open(csv_file_path, "w") as file:
        file.write("First Name, Last Name, Phone, Email\n")
        for user in users:
            file.write(f"{user[0]}, {user[1]}, {user[2]}, {user[3]}\n")

    send_email(csv_file_path)


def run_script():
    # load environment variables from the .env file
    load_dotenv()
    # Check if today is Monday (0 corresponds to Monday)
    generate_user_data()
    if datetime.now().weekday() == 0:
        # Convert to the IST time zone
        ist = timezone(time_zone)
        now_ist = datetime.now(ist)
        current_time = now_ist.strftime(time_format)

        # Send the email only if it's 11:00 AM IST
        if current_time == execution_time:
            # ... (rest of your email sending code)
            generate_user_data()


# Schedule the script to run every week on Wednesday
# schedule.every().monday.at(execution_time).do(run_script)
schedule.every(5).seconds.do(run_script)
# schedule.every().hour.do(run_script).at_time_zone(time_zone)

# Run the script continuously
while True:
    schedule.run_pending()
    sleep(1)



