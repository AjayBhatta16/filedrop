from shared_utils import FileRepo, DataRepo, HttpException

class DeleteFileHandler():
    def __init__(self, metadata_repo: DataRepo, storage_repo: FileRepo):
        self.metadata_repo = metadata_repo
        self.storage_repo = storage_repo

    def delete_metadata(self, file_id):
        metadata = self.metadata_repo.search_one({"displayID": file_id})

        if metadata == None:
            raise HttpException(404, f"File with display ID {file_id} not found.")

        self.metadata_repo.delete_item({"displayID": file_id})

        return metadata
    
    def delete_file_s3(self, storage_url):
        self.storage_repo.deleteFile(storage_url)

    def handle(self, req):
        delete_meta_result = self.delete_file(req["displayID"])

        self.delete_file_s3(delete_meta_result["storageURL"])

        return delete_meta_result