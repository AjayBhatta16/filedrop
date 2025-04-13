import json

from .http_exception import HttpException

class RequestSchema():
    def __init__(self, method: str, required_fields: list):
        self.method = method
        self.required_fields = required_fields

def validate_request(request_event, request_schema: RequestSchema):
    if request_event["requestContext"]["http"]["method"] != request_schema.method:
        raise HttpException(405, "method not allowed")
    
    req_body = json.loads(request_event.get("body", "{}"))

    for field in request_schema.required_fields:
        if field not in req_body:
            raise HttpException(400, f"Missing required field: {field}")
    
    return req_body