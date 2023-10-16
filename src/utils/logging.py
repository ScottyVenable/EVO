import datetime
import os


class Timestamping:
    def log_timestamps():
        timestamp = datetime.datetime.now().strftime("%I:%M:%S -- ")
        return timestamp

class CreateLog:
    logs_directory = "src\logs"

    def __init__(self, log_filename, logs_directory):
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file_path = os.path.join(self.logs_directory, f"{log_filename}_{self.timestamp}.txt")
        os.makedirs(self.logs_directory, exist_ok=True)

    # Create the 'logs' directory if it doesn't exist
    os.makedirs(logs_directory, exist_ok=True)



