import os
import json

from handler import GetFileHandler
from shared_utils import DataRepo, HttpException, RequestSchema, validate_request

file_metadata_repo = DataRepo(os.environ.get("FILE_METADATA_CONTAINER_ID"))

req_handler = GetFileHandler(file_metadata_repo)

req_schema = RequestSchema("POST", ["fileID"])

def lambda_handler(event, context):
    try:
        req_body = validate_request(event, req_schema)

        result = req_handler.handle(req_body)

        print(f'Handler result -', result)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
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