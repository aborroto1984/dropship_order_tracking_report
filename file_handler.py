from datetime import datetime
import os
import pandas as pd


class FileHandler:
    DATE_FORMAT = "%m%d%Y"
    TIME_FORMAT = "%H%M%S"
    BASE_DIRECTORY = "tmp"

    @staticmethod
    def save_tracking_data_to_file(all_rows, ftp_folder_name):
        """Saves the tracking data to a file."""
        tracking_data_df = pd.DataFrame(all_rows)
        directory_path = FileHandler._create_directory_structure(ftp_folder_name)
        date_str = datetime.today().strftime(FileHandler.DATE_FORMAT)
        time_str = datetime.today().strftime(FileHandler.TIME_FORMAT)
        file_path = f"{directory_path}\ASN_{date_str}_{time_str}.csv"

        try:
            tracking_data_df.to_csv(file_path, index=False)
            return file_path, tracking_data_df
        except Exception as e:
            print(f"Error while saving tracking data to file: {e}")
            raise

    @staticmethod
    def _create_directory_structure(ftp_folder_name):
        """Creates the directory structure for the tracking files."""
        datetime_str = datetime.today().strftime(
            f"{FileHandler.DATE_FORMAT}_{FileHandler.TIME_FORMAT}"
        )
        dir_path = os.path.join(
            FileHandler.BASE_DIRECTORY, ftp_folder_name, datetime_str
        )

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return dir_path
