import os
import json

from handler import CleanupTimerHandler
from shared_utils import DataRepo, FileRepo

metadata_repo = DataRepo(os.environ.get("FILE_METADATA_CONTAINER_ID"))
storage_repo = FileRepo()

handler = CleanupTimerHandler(metadata_repo, storage_repo)

def lambda_handler(event, context):
    print('Cleanup Timer - start')

    result = handler.handle()

    print('Cleanup Results:')
    print(f'\t- Files deleted: {result["filesDeleted"]}')
    errors_formatted = "\n".join(f"\t\t* {error}" for error in result["errors"])
    print(f'\t- Errors:\n{errors_formatted}')

    return json.dumps(result)