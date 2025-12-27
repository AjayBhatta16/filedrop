import os
import json

from handler import SignupHandler
from shared_utils import DataRepo, HttpException, HttpRequestMiddleware, RequestSchema, validate_request

user_repo = DataRepo(os.environ.get("USER_CONTAINER_ID"))
req_handler = SignupHandler(user_repo)

middleware = HttpRequestMiddleware("USER_SIGNUP")
req_schema = RequestSchema("POST", ["username", "email", "password"])

def lambda_handler(event, context):
    try:
        middleware.handle_lambda_event(event)

        req_body = validate_request(event, req_schema)

        req_body["ipAddress"] = middleware.get_ip_address()

        result = req_handler.handle(req_body)

        print(f'Handler result -', result)

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "username": result["username"],
                "email": result["email"]
            }),
            "isBase64Encoded": False
        }

    except HttpException as ex:
        return {
            "statusCode": ex.status_code,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": ex.message
            }),
            "isBase64Encoded": False
        }
    
    except Exception as ex:
        print(str(ex))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "An unknown error has occurred."
            }),
            "isBase64Encoded": False
        }