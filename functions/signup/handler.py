from shared_utils import encrypt_password, DataRepo, HttpException

class SignupHandler():
    def __init__(self, user_repo: DataRepo):
        self.user_repo = user_repo

    def handle(self, req):
        uname_query = self.user_repo.search({"username": req.username})

        if len(list(uname_query)) > 0:
            raise HttpException(409, "A user with this username already exists.")
        
        email_query = self.user_repo.search({"email": req.email})

        if len(list(email_query)) > 0:
            raise HttpException(409, "A user with this email already exists.")
        
        new_user = {
            "username": req.username,
            "email": req.email,
            "password": encrypt_password(req.password)
        }

        self.user_repo.create_item(new_user)

        return new_user

    
    