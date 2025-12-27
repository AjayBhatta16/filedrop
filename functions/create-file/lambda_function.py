import os
import json

from handler import CreateFileHandler
from shared_utils import DataRepo, FileRepo, HttpException, HttpRequestMiddleware, RequestSchema, validate_request

file_metadata_repo = DataRepo(os.environ.get("FILE_METADATA_CONTAINER_ID"))
file_storage_repo = FileRepo()

req_handler = CreateFileHandler(file_metadata_repo, file_storage_repo)

middleware = HttpRequestMiddleware("CREATE_FILE")
req_schema = RequestSchema("POST", ["type", "expDate", "ownerID", "displayName", "storageURL"])

def lambda_handler(event, context):
    try:
        middleware.handle_lambda_event(event)

        req_body = validate_request(event, req_schema)

        result = req_handler.handle(req_body)

        print(f'Handler result -', result)

        if "_id" in result:
            del result["_id"]

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "isBase64Encoded": False,
            "body": json.dumps(result),
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