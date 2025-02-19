import pyodbc
from config import create_connection_string, db_config
from email_helper import send_email
from tqdm import tqdm


class ExampleDb:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                create_connection_string(db_config["ExampleDb"]),
            )
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e:
            print(f"Error establishing connection to the ExampleDb database: {e}")
            raise

    def get_untracked_orders(self):
        """Gets all the untracked orders from the ExampleDb database."""
        try:
            self.cursor.execute(
                """
                SELECT   
                    po.id,     
                    po.purchase_order_number,
                    po.sellercloud_order_id,
                    d.code
                FROM PurchaseOrders po
                JOIN Dropshippers d ON po.dropshipper_id = d.id
                JOIN ShipstationOrderIds s on po.id = s.purchase_order_id
                WHERE po.is_cancelled = 0 AND po.in_sellercloud = 1 AND po.tracking_number IS NULL AND d.code = 'ABS'
                """
            )
            rows = self.cursor.fetchall()

            # Placeholder
            dropshippers_untracked_orders = {}
            sellercloud_order_ids = []

            for row in tqdm(rows, desc="Getting untracked orders"):
                sellercloud_order_ids.append(str(row.sellercloud_order_id))

                order = {
                    "purchase_order_number": row.purchase_order_number,
                    "sellercloud_order_id": row.sellercloud_order_id,
                }

                if dropshippers_untracked_orders.get(row.code):
                    dropshippers_untracked_orders[row.code].append(order)

                else:
                    dropshippers_untracked_orders[row.code] = [order]

            return dropshippers_untracked_orders, sellercloud_order_ids

        except Exception as e:
            print(f"Error while getting untracked orders: {e}")
            raise

    def turning_on_is_cancelled_status(self, purchase_order_number):
        """Updates the is_cancelled status to 1 in the ExampleDb database."""
        try:
            self.cursor.execute(
                """
                UPDATE PurchaseOrders
                SET is_cancelled = '1'
                WHERE purchase_order_number = ?
                """,
                purchase_order_number,
            )
            self.conn.commit()

        except Exception as e:
            print(f"Error while updating backorder status: {e}")
            send_email(
                "There was an error while updating is_cancelled status: ",
                f"Please update the is_cancelled status in the PurchaseOrders table, to 1 for the purchase order {purchase_order_number} manually.",
            )

    def turning_on_is_backorder_status(self, purchase_order_number):
        """Updates the is_cancelled status to 1 in the ExampleDb database."""
        try:
            self.cursor.execute(
                """
                UPDATE PurchaseOrders
                SET is_backorder = '1'
                WHERE purchase_order_number = ?
                """,
                purchase_order_number,
            )
            self.conn.commit()

        except Exception as e:
            print(f"Error while updating backorder status: {e}")
            send_email(
                "There was an error while updating is_cancelled status: ",
                f"Please update the is_cancelled status in the PurchaseOrders table, to 1 for the purchase order {purchase_order_number} manually.",
            )

    def save_tracking_data(self, untracked_orders):
        """Saves the tracking data to the database."""
        po_and_tracking = []
        for orders in tqdm(untracked_orders.values(), desc="Saving tracking data"):
            for order in orders:
                if order.get("tracking_number"):
                    po_and_tracking.append(
                        (
                            order["tracking_number"],
                            order["purchase_order_number"],
                        )
                    )

        try:
            self.cursor.executemany(
                """
                UPDATE PurchaseOrders
                SET tracking_number = ?
                WHERE purchase_order_number = ?
                """,
                po_and_tracking,
            )
            self.conn.commit()

        except Exception as e:
            print(f"Error while updating tracking number: {e}")
            send_email(
                "There was an error while adding the tracking number to an order: ",
                f"Please add the tracking number in the PurchaseOrders table, for the following purchase orders manually:\n\t{po_and_tracking}.",
            )

    def close(self):
        """Closes the connection to the database."""
        self.cursor.close()
        self.conn.close()
