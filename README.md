# Gmail Interac Transfer Automation

This Python script automates the extraction of Interac e-Transfer details from Gmail and stores the information in a MariaDB (MySQL) database.

## Features

- Connects to Gmail using IMAP to fetch unseen emails.
- Extracts Interac e-Transfer details from the email bodies.
- Stores the extracted information in a MariaDB database.
- Marks processed emails as "seen" in Gmail to avoid duplication.

## Prerequisites

Before using the script, make sure you have:

- Python installed on your system.
- Required Python libraries installed: `imaplib`, `email`, `re`, `mysql.connector`.
- A MariaDB (MySQL) database set up with the provided table schema.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/gmail-interac-automation.git
   ```

2. Install the required Python library

   pip install imaplib email mysql-connector-python

3. Fill in your Gmail credentials and MariaDB connection details in the script (your@gmail.com, yourAppPassword, database host, user, password, database name).

4. Run the script
   python gmail_interac_automation.py

   The script will run in an infinite loop, checking for new emails every 60 seconds. Adjust the sleep duration in the script according to your preference.

## Database Schema

   ```bash
CREATE TABLE emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_name VARCHAR(255),
    receiver_name VARCHAR (255),  
    from_address VARCHAR(255),
    to_address VARCHAR(255),
    interac_amount VARCHAR(20),
    bank_name VARCHAR(255),
    reference_number VARCHAR(255),
    subject VARCHAR(255),
    date DATETIME,
);
   ```
Remember to replace placeholder details like `your-username`, `your@gmail.com`, `yourAppPassword`, and adjust any other information to match your specific setup. Additionally, include any other relevant information or instructions that users might find helpful.
