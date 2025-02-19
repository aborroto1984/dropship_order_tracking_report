from datetime import datetime

# This is a dictionary of the shipping methods that Jolt uses.
# The keys can be found by using the Get All Shipping Methods Postman request.
# Custom shipping methods can be added here.
shipping_methods = {
    "UPS Ground": {"name": "UPS", "code": "UPS"},
    "FEDEX Ground HD": {"name": "FedEx", "code": "FEDHD"},
}


class RowCreator:
    @staticmethod
    def create_tracking_objects(po, ship_method, tracking_number, items):
        """Creates the tracking_obj and rows for the tracking file."""
        rows = []

        carrier_name = shipping_methods[ship_method]["name"]
        ship_method_code = shipping_methods[ship_method]["code"]
        ship_date = RowCreator._format_ship_date()

        for item in items:
            tracking_obj = {
                "po_number": po,
                "sku": item["sku"],
                "quantity": item["quantity"],
                "carrier_name": carrier_name,
                "ship_method": "Ground",
                "ship_method_code": ship_method_code,
                "ship_date": ship_date,
                "tracking_number": tracking_number,
            }
            rows.append(tracking_obj)

        return rows

    @staticmethod
    def _format_ship_date():
        """Formats the ship date as YYYY-MM-DD."""
        return datetime.today().strftime("%Y-%m-%d")
