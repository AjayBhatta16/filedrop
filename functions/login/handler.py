from shared_utils import encrypt_password, DataRepo, HttpException

class LoginHandler():
    def __init__(self, user_repo: DataRepo, file_metadata_repo: DataRepo):
        self.user_repo = user_repo
        self.file_metadata_repo = file_metadata_repo

    def get_user(self, username: str):
        username_query = self.user_repo.search({"username": username})

        if len(list(username_query)) > 0:
            return list(username_query)[0]
        
        email_query = self.user_repo.search({"email": username})

        if len(list(email_query)) > 0:
            return list(email_query)[0]
        
        raise HttpException(404, "User not found")
    
    def check_password(req_password: str, db_password: str):
        if req_password == db_password or req_password == encrypt_password(db_password):
            return True
        
        raise HttpException(401, "Incorrect password")
    
    def get_user_files(self, username):
        file_query = self.file_metadata_repo.search({"ownerID": username})

        user_files = []
        for file in file_query:
            user_files.append({
                "id": file['id'],
                "name": file['name'],
                "type": file['type'],
                "expDate": file['expDate']
            })
        
        return user_files

    def handle(self, req):
        user = self.get_user(req.username)

        self.check_password(req.password, user.password)

        user.files = self.get_user_files(user.username)

        return user