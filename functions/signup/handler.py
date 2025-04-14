from shared_utils import encrypt_password, DataRepo, HttpException

class SignupHandler():
    def __init__(self, user_repo: DataRepo):
        self.user_repo = user_repo

    def handle(self, req):
        print('Signup Handler - validating unique username')
        uname_result = self.user_repo.search_one({"username": req["username"]})

        if uname_result != None:
            raise HttpException(409, "A user with this username already exists.")
        
        print('Signup Handler - validating unique email')
        email_result = self.user_repo.search_one({"email": req["email"]})

        if email_result != None:
            raise HttpException(409, "A user with this email already exists.")
        
        print('Signup Handler - encrypting password')
        encrypted_passwd = encrypt_password(req["password"])

        new_user = {
            "username": req["username"],
            "email": req["email"],
            "password": encrypted_passwd
        }

        print('Signup Handler - creating new user')
        self.user_repo.create_item(new_user)

        return new_user

    
