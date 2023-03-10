from flask import Flask, request, render_template, send_file, abort
from werkzeug.utils import secure_filename
from db import get_db
from cleanup import delete_old_files

import json
import string
import random
import os
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'userfiles'
CLEANUP_INTERVAL = 100
newFiles = 0
salt = 'dr0p'

filedrop_db = get_db()
users = filedrop_db['users']
files = filedrop_db['files']
iplogs = filedrop_db['iplogs']

def encrypt_password(password):
    global salt
    db_password = password + salt 
    return hashlib.md5(db_password.encode()).hexdigest()

def userData(username):
    fileQuery = files.find({"ownerID": username})
    userFiles = []
    for file in fileQuery:
        userFiles.append(json.dumps({
            "id": file['id'],
            "name": file['name'],
            "type": file['type'],
            "expDate": file['expDate']
        }))
    return json.dumps({
        "status": "200",
        "username": username,
        "files": userFiles
    })

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

def generateID():
    return ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(8)])

def newFileID():
    id = generateID()
    fileQuery = files.find({"id": id})
    if len(list(fileQuery)) > 0:
        return newFileID()
    return id 

def get_ext(filename):
    parts = filename.split(".")
    return parts[len(parts) - 1]

@app.route('/')
def send_index():
    return render_template('index.html')

@app.route('/login')
def send_login_page():
    return render_template('login.html')

@app.route('/signup')
def send_signup_page():
    return render_template('signup.html')

@app.route('/dashboard')
def send_dashboard():
    return render_template('dashboard.html')

@app.route('/newfile')
def send_create_page():
    return render_template('newfile.html')

@app.route('/user/login', methods = ['POST'])
def login():
    dataStr = request.data.decode()
    data = json.loads(dataStr)
    username = ""
    userQuery = users.find({"username": data['username']})
    for user in userQuery:
        if user['password'] == data['password'] or user['password'] == encrypt_password(data['password']):
            username = user['username']
    emailQuery = users.find({"email": data['username']})
    for user in emailQuery:
        if user['password'] == data['password']:
            username = user['username']
    if len(username) > 0:
        return userData(username)
    return json.dumps({
        "status": "404",
        "message": "Incorrect username or password"
    })

@app.route('/user/create', methods = ['POST'])
def user_create():
    # TODO: Implement password encryption
    dataStr = request.data.decode()
    data = json.loads(dataStr)
    usernameQuery = users.find({"username": data['username']})
    if len(list(usernameQuery)) > 0:
        return json.dumps({
            "status": 400,
            "message": "An account with this username already exists"
        })
    emailQuery = users.find({"email": data['email']})
    if len(list(emailQuery)) > 0:
        return json.dumps({
            "status": 400,
            "message": "An account with this email already exists"
        })
    newUser = {
        "username": data['username'],
        "email": data['email'],
        "password": encrypt_password(data['password']),
    }
    users.insert_one(newUser)
    return json.dumps({
        "status": "200",
        "username": newUser['username']
    })

@app.route('/file/upload', methods = ['POST'])
def file_upload():
    global newFiles 
    global CLEANUP_INTERVAL
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
    id = newFileID()
    log_IP(request, "upload", id)
    f.save(app.config['UPLOAD_FOLDER']+"/"+secure_filename(id+"."+get_ext(f.filename)))
    print("file data: ", request.form['model'])
    data = json.loads(request.form['model'])
    newFile = {
        "id": id,
        "type": data['type'],
        "expDate": data['expDate'],
        "ownerID": data['ownerID'],
        "name": data['name']
    }
    files.insert_one(newFile)
    newFiles = newFiles + 1
    if newFiles == CLEANUP_INTERVAL:
        files_deleted = delete_old_files()
        print(str(files_deleted) + " files deleted")
        newFiles = 0
    return json.dumps({
        "status": 200,
        "fileID": id
    })

@app.route('/<fileID>', methods = ['GET', 'DELETE'])
def get_file(fileID):
    if request.method == 'GET':
        log_IP(request, "download", fileID)
        fileCode = ""
        fileQuery = files.find({"id": fileID})
        for file in fileQuery:
            fileCode = file['id'] + "." + file['type']
        if len(fileCode) == 0:
            abort(404)
        return send_file(app.config['UPLOAD_FOLDER']+"/"+fileCode, as_attachment = True)
    if request.method == 'DELETE':
        fileCode = ""
        fileQuery = files.find({"id": fileID})
        for file in fileQuery:
            fileCode = file['id'] + "." + file['type']
            fileName = file['name']
        if len(fileCode) == 0:
            abort(404)
        os.remove(app.config['UPLOAD_FOLDER']+"/"+fileCode)
        files.delete_one({"id": fileID})
        return json.dumps({
            "status": 200,
            "message": "File "+fileName+" has been deleted."
        })

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run()
