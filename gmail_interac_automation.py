import imaplib
import email
import re
import mysql.connector
from datetime import datetime
import time

# Function to extract Interac e-Transfer details from email body
def extract_interac_details(body):
    sender_name = None
    receiver_name = None
    interac_amount = None
    bank_name = None
    reference_number = None

    # Extract sender's name
    sender_match = re.search(r'([^,]+) has sent you', body)
    if sender_match:
        sender_name = sender_match.group(1).strip()

    # Extract receiver's name
    receiver_match = re.search(r'Hi ([^,]+),', body)
    if receiver_match:
        receiver_name = receiver_match.group(1).strip()

    # Split the email body into lines and iterate through them
    for line in body.split('\n'):
        if "Reference Number:" in line:
            reference_number = line.split("Reference Number:")[1].strip()
            break

    # Use regular expressions to extract the amount and bank name as before
    match_amount = re.search(r'has sent you (\$[\d,]+\.\d{2} \(\w+\))', body)
    if match_amount:
        interac_amount = match_amount.group(1)
    match_bank = re.search(r'your bank account at (\w+(?: \w+)*)', body)
    if match_bank:
        bank_name = match_bank.group(1)

    return sender_name, receiver_name, interac_amount, bank_name, reference_number

# Gmail credentials and login details
username = "your@gmail.com"
app_password = "yourAppPassword"

while True:
    # Connect to Gmail using IMAP
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, app_password)

    # Select the mailbox (Inbox)
    mail.select("inbox")

    # Connect to MariaDB
    db = mysql.connector.connect(
        host="127.0.0.1", #your database hosting, in my case my databse hosting is 127.0.0.1
        user="root", #your database username, in my case my databse username is root
        password="root", #your database password, in my case my databse password is root
        database="emailpy" #database name, in my case my database name is emailpy
    )

    cursor = db.cursor()

    # Search for unseen emails
    status, email_ids = mail.search(None, "UNSEEN")

    if status == "OK":
        email_id_list = email_ids[0].split()
        for email_id in email_id_list:
            # Fetch the email
            status, email_data = mail.fetch(email_id, "(RFC822)")

            if status == "OK":
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Extract headers
                from_address = msg["from"]
                date = msg["date"]
                subject = msg["subject"]
                to_address = msg["to"]

                # Initialize variables for Interac e-Transfer details
                sender_name = None
                receiver_name = None
                interac_amount = None
                bank_name = None
                reference_number = None

                # Extract Interac e-Transfer details from the email body
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()

                        # Check if the email contains Interac details
                        if "INTERAC" in body:
                            sender_name, receiver_name, interac_amount, bank_name, reference_number = extract_interac_details(body)
                            print("Sender Name:", sender_name)
                            print("Receiver Name:", receiver_name)
                            print("Interac Amount:", interac_amount)
                            print("Bank Name:", bank_name)
                            print("Reference Number:", reference_number)

                # Convert the date to the correct MySQL datetime format
                try:
                    email_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
                    date = email_date.strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    # Handle date parsing errors
                    print("Error parsing date:", e)
                    date = None

                # Insert data into MariaDB
                sql = "INSERT INTO emails (from_address, to_address, sender_name, receiver_name, subject, date, interac_amount, bank_name, reference_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (from_address, to_address, sender_name, receiver_name, subject, date, interac_amount, bank_name, reference_number)
                cursor.execute(sql, values)
                db.commit()

                print("Email data inserted successfully.")

                # Mark the email as "seen" in Gmail
                mail.store(email_id, '+FLAGS', r'(\Seen)')

    cursor.close()
    db.close()
    mail.logout()

    time.sleep(60)  # Wait for 60 seconds before checking for new emails again

# MySql Query to create table

# CREATE TABLE emails (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     sender_name VARCHAR(255),
#     receiver_name VARCHAR (255),  
#     from_address VARCHAR(255),
#     to_address VARCHAR(255),
#     interac_amount VARCHAR(20),
#     bank_name VARCHAR(255),
#     reference_number VARCHAR(255),
#     subject VARCHAR(255),
#     date DATETIME,
# );