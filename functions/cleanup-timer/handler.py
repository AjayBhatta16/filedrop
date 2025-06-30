from shared_utils import DataRepo, FileRepo
import datetime

class CleanupTimerHandler():
    def __init__(self, metadata_repo: DataRepo, storage_repo: FileRepo):
        self.metadata_repo = metadata_repo
        self.storage_repo = storage_repo

    def get_expired_files(self):
        all_files = self.metadata_repo.search({})
        expired_files = []

        for file in all_files:
            now = datetime.datetime.now()

            print(f"expDate type: {type(file['expDate'])}")
            print(f"now type: {type(now)}")
            
            exp_date = datetime.datetime.fromtimestamp(file['expDate'] / 1000)
            diff = now - exp_date
            
            if diff.total_seconds() / 60 > 1440:
                expired_files.append(file)

    def delete_file_metadata(self, file_id: str):
        self.metadata_repo.delete_item({"displayID": file_id})

    def delete_file_from_storage(self, storage_url: str):
        self.storage_repo.deleteFile(storage_url)

    def handle(self):
        expired_files = self.get_expired_files()

        file_count = 0
        error_list = []

        for file in expired_files:
            file_count += 1

            try:
                file_id = file["displayID"]
                storage_url = file["storageURL"]
                
                self.delete_file_from_storage(storage_url)

                self.delete_file_metadata(file_id)
            except Exception as ex:
                error_list.append(str(ex))

        return {
            "filesDeleted": file_count,
            "errors": error_list
        }