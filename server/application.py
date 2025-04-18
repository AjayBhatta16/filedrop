from flask import Flask, request, render_template, send_file, abort
from werkzeug.utils import secure_filename

import json
import os
import boto3
import uuid
import requests

application = Flask(__name__)

s3_client = boto3.client('s3')

print(os.environ.get("API_GATEWAY_URL"))
js_env = {
    "baseURL": os.environ.get("API_GATEWAY_URL")
}

"""
def log_IP(req, action, fileID):
    ip = ""
    if req.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = req.environ['REMOTE_ADDR']
    else: 
        ip = req.environ['HTTP_X_FORWARDED_FOR']
    log = {
        "action": action,
        "fileID": fileID,
        "IPAddress": ip,
        "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
    iplogs.insert_one(log) 
"""

@application.route('/')
def send_index():
    return render_template('index.html', js_env=js_env)

@application.route('/login')
def send_login_page():
    return render_template('login.html', js_env=js_env)

@application.route('/signup')
def send_signup_page():
    return render_template('signup.html', js_env=js_env)

@application.route('/dashboard')
def send_dashboard():
    return render_template('dashboard.html', js_env=js_env)

@application.route('/newfile')
def send_create_page():
    return render_template('newfile.html', js_env=js_env)

@application.route('/file/upload', methods = ['POST'])
def file_upload():
    if 'file' not in request.files:
        print('No file part')
        return json.dumps({
            "status": "400",
            "message": "no file part"
        })
    
    f = request.files['file']
    if f.filename == '':
        print('No selected file')
    else:
        print('File received: ', f.filename)
    
    uuid_prefix = uuid.uuid4()
    file_name = secure_filename(f'{uuid_prefix}_{f.filename}')

    # save file to s3
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

    upload_headers = {
        "ContentType": f.content_type
    }

    try:
        s3_client.upload_fileobj(f, S3_BUCKET_NAME, file_name, ExtraArgs=upload_headers)
    except Exception as e:
        print('S3 Upload Failed:', e)
        return json.dumps({
            "status": "500",
            "message": "Failed to upload file to S3"
        })

    print("file data: ", request.form['model'])
    data = json.loads(request.form['model'])

    create_file_request = {
        "type": data['type'],
        "expDate": data['expDate'],
        "ownerID": data['ownerID'],
        "displayName": data['displayName'],
        "storageURL": file_name
    }

    # forward request to Lambda
    API_GATEWAY_URL = os.environ.get("API_GATEWAY_URL")
    response = requests.post(
        f"{API_GATEWAY_URL}/filedrop-file-create", 
        json.dumps(create_file_request), 
        headers={
            'Content-Type': 'application/json'
        }
    )

    if int(response.status_code) >= 400:
        return json.dumps({
            "status": 500,
            "message": f"Failed to create metadata with error code {response.status_code}"
        })
    
    file_id = response.json()["displayID"]
    
    return json.dumps({
        "status": 200,
        "displayID": file_id
    })

@application.route('/<fileID>', methods = ['GET'])
def get_file(fileID):
    get_metadata_request = {
        "displayID": fileID
    }

    # call lambda function to get metadata
    API_GATEWAY_URL = os.environ.get("API_GATEWAY_URL")
    response = requests.post(
        f"{API_GATEWAY_URL}/filedrop-file-get-metadata", 
        json.dumps(get_metadata_request), 
        headers={
            'Content-Type': 'application/json'
        }
    )

    if int(response.status_code) >= 400:
        return json.dumps({
            "status": 500,
            "message": f"Failed to create metadata with error code {response.status_code}"
        })
    
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    
    metadata = response.json()
    s3_file_name = metadata["storageURL"]
    s3_response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_file_name)

    f = s3_response['Body']
    
    return send_file(f, as_attachment = True, download_name=metadata["displayName"])
    

if __name__ == '__main__':
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    application.run()
