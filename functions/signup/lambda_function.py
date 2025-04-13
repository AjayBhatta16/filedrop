import os
import json

from handler import SignupHandler
from shared_utils import DataRepo, HttpException, RequestSchema, validate_request

user_repo = DataRepo(os.environ.get("USER_CONTAINER_ID"))
req_handler = SignupHandler(user_repo)

req_schema = RequestSchema("POST", ["username", "email", "password"])

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
        print(str(ex))

        return json.dumps({
            "status": 500,
            "message": "An unknown error has occurred."
        })