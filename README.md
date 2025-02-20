# Order Tracking and Processing System

This project automates order tracking, status updates, and integration with SellerCloud.

## Features
- Retrieves untracked orders from the database.
- Fetches tracking numbers and updates order statuses.
- Uploads tracking data to an FTP server.
- Sends email notifications for errors and tracking updates.

## Project Structure
```
project_root/
├── config.py              # Configuration file for database, API, and email credentials
├── email_helper.py        # Sends email notifications
├── example_db.py          # Manages database interactions
├── file_handler.py        # Handles tracking file creation and storage
├── ftp.py                 # Uploads tracking files to an FTP server
├── main.py                # Main script orchestrating order tracking
├── row_creator.py         # Creates tracking file rows
├── seller_cloud_api.py    # Interfaces with SellerCloud API
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/order-tracking.git
cd order-tracking
```

### 2. Install Dependencies
Ensure you have Python 3 installed, then install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure the System
Modify `config.py` with your database, FTP, and API credentials.

Example database configuration:
```python
db_config = {
    "ExampleDb": {
        "server": "your.database.windows.net",
        "database": "YourDB",
        "username": "your_user",
        "password": "your_password",
        "driver": "{ODBC Driver 17 for SQL Server}",
    },
}
```
Example email configuration:
```python
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_email_password"
```

## Usage
Run the main script to start the tracking process:
```bash
python main.py
```

## How It Works
1. Fetches untracked orders from the database.
2. Retrieves tracking numbers from SellerCloud.
3. Updates order statuses (e.g., shipped, backordered).
4. Saves tracking data to a CSV file.
5. Uploads tracking files to an FTP server.
6. Sends email notifications for errors or missing tracking data.

## Tech Stack
- Python 3
- Azure SQL Database (`pyodbc`)
- SellerCloud API Integration
- FTP File Handling (`ftplib`)
- Email Notifications (`smtplib`)

## Troubleshooting
- If you encounter database connection issues, ensure `ODBC Driver 17` is installed.
- If emails fail to send, ensure your SMTP settings allow external authentication.
