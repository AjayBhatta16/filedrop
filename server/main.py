from flask import Flask, request, render_template
from db import get_db
import json

app = Flask(__name__)

filedrop_db = get_db()
users = filedrop_db['users']
files = filedrop_db['files']

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
        if user['password'] == data['password']:
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
        "password": data['password'],
    }
    users.insert_one(newUser)
    return json.dumps({
        "status": "200",
        "username": newUser['username']
    })

@app.route('/file/upload', methods = ['POST'])
def file_upload():
    return 'file_upload'

@app.route('/<fileID>', methods = ['GET', 'DELETE'])
def get_file(fileID):
    return 'get_file %s' % fileID

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run()
