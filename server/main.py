from flask import Flask, request
from db import get_db
import json

app = Flask(__name__)
filedrop_db = get_db()
users = filedrop_db['users']
files = filedrop_db['files']


@app.route('/user/login', methods = ['POST'])
def login():
    return 'login'

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
