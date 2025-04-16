from shared_utils import encrypt_password, DataRepo, HttpException

class LoginHandler():
    def __init__(self, user_repo: DataRepo, file_metadata_repo: DataRepo):
        self.user_repo = user_repo
        self.file_metadata_repo = file_metadata_repo

    def get_user(self, username: str):
        LOG_CONTEXT = 'LoginHandler - get_user'

        print(f'{LOG_CONTEXT} - search by username')
        username_query = self.user_repo.search_one({"username": username})

        if username_query != None:
            print(f'{LOG_CONTEXT} - user found: {username_query}')
            return username_query
        
        print(f'{LOG_CONTEXT} - search by email')
        email_query = self.user_repo.search_one({"email": username})

        if email_query != None:
            print(f'{LOG_CONTEXT} - user found: {email_query}')
            return email_query
        
        print(f'{LOG_CONTEXT} - user not found')
        raise HttpException(404, "User not found")
    
    def check_password(self, req_password: str, db_password: str):
        LOG_CONTEXT = 'LoginHandler - check_password'

        print(f'{LOG_CONTEXT} - encrypting password')
        encrypt_result = encrypt_password(req_password)

        print(f'{LOG_CONTEXT} - encrypt result: {encrypt_result}')

        if req_password == db_password or encrypt_result == db_password:
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

        user["files"] = self.get_user_files(user)

        return user