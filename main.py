from row_creator import RowCreator
from email_helper import send_email
from file_handler import FileHandler
from example_db import ExampleDb
from seller_cloud_api import SellerCloudAPI
import traceback
from ftp import FTPManager
from tqdm import tqdm


def batches_creator(objects, batch_size):
    """Creates batches of objects to be processed."""
    counter = 1
    container = []
    try:
        # It makes batches of 50 skus to send to SellerCloud
        while True:
            if len(objects) > batch_size:
                batch = [objects.pop() for _ in range(batch_size)]
            else:
                batch = objects
                objects = []

            container.append(batch)

            if not objects:
                print(f"Done creating batches of {batch_size}.")
                return container

            counter += 1

    except Exception as e:
        print(f"Error creating batches: {e}")
        raise Exception(f"Error creating batches: {e}")


def map_order_status(order_status):
    if order_status == -1:
        order_status = "Cancelled"
    elif order_status == 200:
        order_status = "OnHold"
    elif order_status == 100:
        order_status = "ProblemOrder"
    else:
        order_status = None

    return order_status


def get_sellercloud_order(sellercloud_orders_ids):
    """Checks to see if a batch of skus are in SellerCloud."""
    # NOTE: This only returns the skus that are in SellerCloud
    sc_api = SellerCloudAPI()
    sellercloud_orders = {}
    try:
        # It makes batches of 50 sellercloud_orders_ids to send to SellerCloud
        batches = batches_creator(sellercloud_orders_ids, 50)
        for batch in batches:
            # Using the previously extracted sellercloud_orders_ids to get the orders from SellerCloud
            check_sku_data = {"url_args": {"order_ids": ", ".join(batch)}}
            response = sc_api.execute(check_sku_data, "GET_ORDERS")

            # Getting the orders status and tracking number
            if response.status_code == 200:
                for order in response.json()["Items"]:
                    sellercloud_orders[order["ID"]] = {
                        "order_status": map_order_status(order["StatusCode"]),
                        "tracking_number": order["TrackingNumber"],
                        "tracking_date": order["ShipDate"],
                    }

        return sellercloud_orders

    except Exception as e:
        print(f"Error getting skus from SellerCloud: {e}")
        raise Exception("Error getting orders from SellerCloud")


def main():
    try:
        # Instantiating the classes
        d_db = ExampleDb()
        handler = FileHandler()
        row_creator = RowCreator()
        ftp = FTPManager()

        # Getting the untracked orders from the database
        untracked_orders, sellercloud_orders_ids = d_db.get_untracked_orders()

        sellercloud_orders = get_sellercloud_order(sellercloud_orders_ids)

        if not sellercloud_orders:
            print("There are no untracked orders")
            return

        # Placeholder for all the paths of the files created in the tmp folder
        all_paths = []

        dropshipper_codes = list(untracked_orders.keys())

        for dropshipper_code in dropshipper_codes:
            # Getting the orders for the current dropshipper
            orders = untracked_orders[dropshipper_code]

            # Placeholder for all the rows created for the current dropshipper data
            all_rows = []

            for order in tqdm(
                orders[:], desc=f"Getting tracking for {dropshipper_code}"
            ):
                # Getting the tracking number and status for the current order
                order_status_and_shipping = sellercloud_orders[
                    order["sellercloud_order_id"]
                ]

                # Turning on the is_cancelled or is_backorder status if needed
                # and sending an email if the order has a problem status
                if order_status_and_shipping["order_status"] == "Cancelled":
                    d_db.turning_on_is_cancelled_status(order["purchase_order_number"])
                elif order_status_and_shipping["order_status"] == "OnHold":
                    d_db.turning_on_is_backorder_status(order["purchase_order_number"])
                elif order_status_and_shipping["order_status"] == "ProblemOrder":
                    send_email(
                        "There is an order with a problem in SellerCloud",
                        f"Order {order['sellercloud_order_id']} has a problem order status",
                    )

                # Getting the tracking number
                if order_status_and_shipping["tracking_number"]:
                    tracking_number = order_status_and_shipping["tracking_number"]
                    tracking_date = order_status_and_shipping["tracking_date"]
                else:
                    orders.remove(order)
                    print(
                        f"Order {order['purchase_order_number']} has no tracking number."
                    )
                    continue

                # Storing the tracking number in the order
                order["tracking_number"] = tracking_number
                order["tracking_date"] = tracking_date

                # Creating the tracking objects and rows
                if tracking_number:
                    rows = row_creator.create_tracking_objects(
                        order["purchase_order_number"],
                        order["ship_method"],
                        tracking_number,
                        order["items"],
                    )

                    # Store the rows in the placeholder
                    all_rows.extend(rows)

            if all_rows:
                # Saving the tracking data to a file
                file_path = handler.save_tracking_data_to_file(
                    all_rows, order["ftp_folder_name"]
                )

                # Store the path in the placeholder
                all_paths.append(file_path)

            if not orders:
                del untracked_orders[dropshipper_code]
                print(f"No orders from {dropshipper_code} were tracked.")

        orders_processed = []
        if untracked_orders:
            # Saving the tracking information to the database
            d_db.save_tracking_data(untracked_orders)

            if all_paths:
                # Uploading the files to the ftp server
                ftp.upload_files(all_paths)
                pass

            for orders in tqdm(
                untracked_orders.values(), desc="Getting data to send email."
            ):
                for order in orders:
                    orders_processed.append(order["sellercloud_order_id"])

        send_email(
            "Sellercloud tracking report ran successfully",
            f"Orders processed {orders_processed}",
        )

    except Exception as e:
        print(f"There was an error: {e}")
        send_email("An Error Occurred", f"Error: {e}\n\n{traceback.format_exc()}")
        raise e


if __name__ == "__main__":
    main()
