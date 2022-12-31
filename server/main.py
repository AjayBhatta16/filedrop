from flask import Flask
app = Flask(__name__)

@app.route('/user/login', methods = ['POST'])
def login():
    return 'login'

@app.route('/user/create', methods = ['POST'])
def user_create():
    return 'user_create'

@app.route('/file/upload', methods = ['POST'])
def file_upload():
    return 'file_upload'

@app.route('/<fileID>', methods = ['GET', 'DELETE'])
def get_file(fileID):
    return 'get_file %s' % fileID

if __name__ == '__main__':
    app.run()
