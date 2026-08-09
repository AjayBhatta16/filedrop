import json
import os

from .activity_log_builder import ActivityLogBuilder
from .activity_logging_service import ActivityLoggingService
from .http_exception import HttpException

class HttpRequestMiddleware:
    def __init__(self, action):
        self.activity_logger = ActivityLoggingService()
        self.action = action

    def handle_lambda_event(self, event, override_ip=False):
        print(f"Lambda headers - {event.get('headers')}")
        self.validate_origin_secret(event)
        self.log_activity(event, override_ip=override_ip)

    def log_activity(self, event, override_ip=False):
        log_entry_builder = ActivityLogBuilder().with_lambda_event(event).with_action(self.action)

        req_body = json.loads(event.get("body", "{}"))

        if override_ip == True:
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

    def validate_origin_secret(self, event):
        req_origin_secret = event.get("headers", {}).get("x-origin-verify")
        expected_secret = os.getenv("ORIGIN_SECRET")

        if req_origin_secret != expected_secret:
            raise HttpException(401, "Missing or invalid origin secret")
        
    def get_ip_address(self):
        return self.ip_address