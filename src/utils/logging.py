import datetime

class Timestamping:
    def log_timestamps():
        timestamp = datetime.datetime.now().strftime("%m/%d/%y - %I:%M:%S -- ")
        return timestamp