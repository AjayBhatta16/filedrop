from shared_utils import encrypt_password, DataRepo, HttpException

class LoginHandler():
    def __init__(self, user_repo: DataRepo, file_metadata_repo: DataRepo):
        self.user_repo = user_repo
        self.file_metadata_repo = file_metadata_repo

    def get_user(self, username: str):
        LOG_CONTEXT = 'LoginHandler - get_user'

        print(f'{LOG_CONTEXT} - search by username')
        username_query = self.user_repo.search({"username": username})

        if len(list(username_query)) > 0:
            return list(username_query)[0]
        
        print(f'{LOG_CONTEXT} - search by email')
        email_query = self.user_repo.search({"email": username})

        if len(list(email_query)) > 0:
            return list(email_query)[0]
        
        print(f'{LOG_CONTEXT} - user not found')
        raise HttpException(404, "User not found")
    
    def check_password(req_password: str, db_password: str):
        LOG_CONTEXT = 'LoginHandler - check_password'

        print(f'{LOG_CONTEXT} - encrypting password')
        encrypt_result = encrypt_password(db_password)

        if req_password == db_password or req_password == encrypt_result:
            return True
        
        print(f'{LOG_CONTEXT} - Incorrect password')
        raise HttpException(401, "Incorrect password")
    
    def get_user_files(self, user):
        LOG_CONTEXT = 'LoginHandler - get_user_files'

        print(f'{LOG_CONTEXT} - searching for files for owner {user["username"]}')

        user_files = []

        if "file_list" in user:
            for file_id in user["file_list"]:
                file = self.file_metadata_repo.search_one({"displayID": file_id})

                user_files.append({
                    "id": file['id'],
                    "name": file['name'],
                    "type": file['type'],
                    "expDate": file['expDate']
                })

        print(f'{LOG_CONTEXT} - {len(user_files)} files found')
        
        return user_files

    def handle(self, req):
        user = self.get_user(req["username"])

        self.check_password(req["password"], user["password"])

        user.files = self.get_user_files(user)

        return user