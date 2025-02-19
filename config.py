db_config = {
    "ExampleDb": {
        "server": "example.database.windows.net",
        "database": "ExampleDb",
        "username": "example",
        "password": "example",
        "driver": "{ODBC Driver 17 for SQL Server}",
        "port": 1433,  # Default port for SQL Server
    },
}


def create_connection_string(server_config):
    return (
        f"DRIVER={server_config['driver']};"
        f"SERVER={server_config['server']};"
        f"PORT={server_config["port"]};DATABASE={server_config['database']};"
        f"UID={server_config['username']};"
        f"PWD={server_config['password']}"
    )


sellercloud_credentials = {
    "Username": "username",
    "Password": "password",
}

sellercloud_base_url = "https://example_company.api.sellercloud.us/rest/api/"


sellercloud_endpoints = {
    "GET_TOKEN": {
        "type": "post",
        "url": "https://example_company.api.sellercloud.us/rest/api/token",
        "endpoint_error_message": "while getting SellerCoud API access token: ",
        "success_message": "Got SellerCloud API access token successfully!",
    },
    "GET_ORDERS": {
        "type": "get",
        "url": "https://example_company.api.sellercloud.us/rest/api/Orders?model.orderIDs={order_ids}&model.pageSize=50",
        "endpoint_error_message": "while getting orders from SellerCloud: ",
        "success_message": "Got orders successfully!",
    },
}

ftp_server = {
    "server": "ftp.example.com",
    "username": "example",
    "password": "password",
}

zip_tax_api_key = "zip_tax_api_key"
zip_tax_api_url = (
    "https://api.zip-tax.com/request/v40?key={api_key}&postalcode={postalcode}"
)

SENDER_EMAIL = "sender_email@domain.com"
SENDER_PASSWORD = "sender_password"
RECIPIENT_EMAILS = [
    "recipient_email_1@domain.com",
    "recipient_email_2@domain.com",
]  # List of emails to send the report
