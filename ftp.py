import os
import ftplib
from config import ftp_server
from tqdm import tqdm
from email_helper import send_email


class FTPManager:
    def __init__(self):
        self.host = ftp_server["server"]
        self.username = ftp_server["username"]
        self.password = ftp_server["password"]

    def upload_files(self, all_paths):
        """Uploads files to both the dropshipper's and the log's folders in the FTP server."""
        try:
            # Starting connection to FTP
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.username, self.password)

            for path_tupple in tqdm(all_paths, desc="Uploading files to FTP server"):
                path = path_tupple[0]
                ftp_folder_name, file_name = self._path_decomposer(path)

                if ftp_folder_name != "absolute_trade":
                    # List of directories to upload the file
                    ftp_directories = [
                        f"dropshipper_logs/tracking_logs/{ftp_folder_name}",
                        f"dropshipper/{ftp_folder_name}/tracking",
                    ]

                    # ftp_directories = [
                    #     f"test_dropshipper_logs/tracking_logs/{ftp_folder_name}",
                    #     f"test_dropshipper/{ftp_folder_name}/tracking",
                    # ]

                    for ftp_directory in ftp_directories:
                        # Reset to the root directory
                        self.ftp.cwd("/")

                        # Change to the remote directory
                        self.ftp.cwd(ftp_directory)

                        # Uploading file
                        with open(path, "rb") as local_file:
                            self.ftp.storbinary(
                                "STOR " + os.path.basename(path), local_file
                            )

            self.ftp.quit()

        except ftplib.all_errors as e:
            # Closing
            self.ftp.quit()

            print(
                f"There was an error uploading the tracking files to the FTP server: {e}"
            )
            send_email(
                f"There was an error uploading the following tracking files to FTP server: \n\t{all_paths}"
            )

    def _path_decomposer(self, path):
        """Decomposes the path into the FTP folder name and the file name.""" ""
        path_parts = path.split("\\")
        ftp_folder_name = path_parts[1]
        file_name = path_parts[-1]
        return ftp_folder_name, file_name
