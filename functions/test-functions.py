import json
import os

with open('./env.json') as file:
    env_vars = json.load(file)
    for k, v in env_vars.items():
        os.environ[k] = str(v)
        print(f"{k}: {os.environ[k]}")

from login.lambda_function import lambda_handler as login_lambda_handler

test_signup_event = {
    "requestContext": {
        "http": {
            "method": "POST",
        },
    },
    "body": json.dumps({
        "username": "test2",
        "email": "test2@email.com",
        "password": "abcd1234"
    })
}

test_login_event = {
    "requestContext": {
        "http": {
            "method": "POST",
        },
    },
    "body": json.dumps({
        "username": "test2",
        "password": "abcd1234"
    })
}

login_result = login_lambda_handler(test_login_event, None)

print(f'Login Result: {login_result}')