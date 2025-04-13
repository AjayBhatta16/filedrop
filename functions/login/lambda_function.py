import os
import json

from handler import LoginHandler
from shared_utils import DataRepo, HttpException, RequestSchema, validate_request

user_repo = DataRepo(os.environ.get("USER_CONTAINER_ID"))
file_metadata_repo = DataRepo(os.environ.get("FILE_CONTAINER_ID"))
req_handler = LoginHandler(user_repo, file_metadata_repo)

req_schema = RequestSchema("POST", ["username", "password"])

def lambda_handler(event, context):
    try:
        req_body = validate_request(event, req_schema)

        result = req_handler.handle(req_body)

        return json.dumps({
            "status": 200,
            "data": result
        })

    except HttpException as ex:
        return json.dumps({
            "status": ex.status_code,
            "message": ex.message
        })
    
    except Exception as ex:
        return json.dumps({
            "status": 500,
            "message": "An unknown error has occurred."
        })