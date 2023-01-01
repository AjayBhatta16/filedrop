from flask import Flask, request
from db import get_db
import json

app = Flask(__name__)
filedrop_db = get_db()
users = filedrop_db['users']
files = filedrop_db['files']

def userData(userQuery):
    user = userQuery[0]
    fileQuery = files.find({"ownerID": user.username})
    return json.dumps({
        "status": "200",
        "user": user,
        "files": fileQuery
    })

@app.route('/user/login', methods = ['POST'])
def login():
    userQuery = users.find({"username": request.form['username']})
    if len(userQuery) > 0:
        return userData(userQuery)
    emailQuery = users.find({"email": request.form['username']})
    if len(emailQuery) > 0:
        return userData(emailQuery)
    return json.dumps({
        "status": "404",
        "message": "Incorrect username or password"
    })

@app.route('/user/create', methods = ['POST'])
def user_create():
    # TODO: Validate username and email
    # TODO: Implement password encryption
    let newUser = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password": request.form['password'],
        "files": []
    }
    users.insert_one(newUser)
    return json.dumps({
        "status": "200",
        "data": newUser
    })

@app.route('/file/upload', methods = ['POST'])
def file_upload():
    return 'file_upload'

@app.route('/<fileID>', methods = ['GET', 'DELETE'])
def get_file(fileID):
    return 'get_file %s' % fileID

if __name__ == '__main__':
    app.run()
