import os

from .data_repo import DataRepo

class ActivityLoggingService():
    def __init__(self):
        log_container_id = os.environ.get("LOG_CONTAINER_ID")
        self.data_repo = DataRepo(log_container_id)
    
    def log_activity(self, log_entry):
        self.data_repo.create_item(log_entry)