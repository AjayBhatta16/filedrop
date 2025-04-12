import hashlib
import os

def encrypt_password(password):
    db_password = password + os.environ.get('PASSWORD_SALT')
    return hashlib.md5(db_password.encode()).hexdigest()