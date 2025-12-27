import datetime
from shared_utils import FileRepo, DataRepo

class CreateFileHandler():
    def __init__(self, file_metadata_repo: DataRepo, file_storage_repo: FileRepo):
        self.metadata_repo = file_metadata_repo
        self.storage_repo = file_storage_repo
    
    def handle(self, req):
        metadata_queryable = self.metadata_repo.get_queryable()

        new_file_id = self.storage_repo.newFileID(metadata_queryable)

        req["displayID"] = new_file_id
        req["createdDateTime"] = datetime.datetime.utcnow().isoformat()
        req["active"] = True

        self.metadata_repo.create_item(req)

        return req
    