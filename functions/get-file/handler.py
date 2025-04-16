from shared_utils import DataRepo, HttpException

class GetFileHandler():
    def __init__(self, file_metadata_repo: DataRepo):
        self.file_metadata_repo = file_metadata_repo

    def get_file(self, id: str):
        file_query = self.file_metadata_repo.search_one({"displayID": id})

        if file_query != None:
            return file_query
        
        raise HttpException(404, 'File not found')

    def handle(self, req):
        file_id = req["fileID"]

        file_info = self.get_file(file_id)

        return file_info