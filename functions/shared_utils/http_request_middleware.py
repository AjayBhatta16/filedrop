import json

from .activity_log_builder import ActivityLogBuilder
from .activity_logging_service import ActivityLoggingService

class HttpRequestMiddleware:
    def __init__(self, action):
        self.activity_logger = ActivityLoggingService()
        self.action = action

    def handle_lambda_event(self, event):
        self.log_activity(event)

    def log_activity(self, event, overrride_ip=False):
        log_entry_builder = ActivityLogBuilder().with_lambda_event(event).with_action(self.action)

        req_body = json.loads(event.get("body", "{}"))

        if overrride_ip == True:
            log_entry_builder = log_entry_builder.with_override_ip(req_body["overrideIP"])

        if "displayName" in req_body:
            log_entry_builder = log_entry_builder.with_display_name(req_body["displayName"])

        if "fileID" in req_body:
            log_entry_builder = log_entry_builder.with_file_id(req_body["fileID"])

        if "displayID" in req_body:
            log_entry_builder = log_entry_builder.with_file_id(req_body["displayID"])

        if "name" in req_body:
            log_entry_builder = log_entry_builder.with_display_name(req_body["name"])

        if "username" in req_body:
            log_entry_builder = log_entry_builder.with_username(req_body["username"])

        if "ownerID" in req_body:
            log_entry_builder = log_entry_builder.with_username(req_body["ownerID"])

        log_entry = log_entry_builder.build()

        self.ip_address = log_entry["ipAddress"]

        self.activity_logger.log_activity(log_entry)
        
    def get_ip_address(self):
        return self.ip_address