from db import get_db
import os
import datetime

filedrop_db = get_db()
files = filedrop_db['files']

UPLOAD_FOLDER = 'userfiles'

def delete_old_files():
    filesDeleted = 0
    fileQuery = files.find({})
    for file in fileQuery:
        print(file['id'])
        expDateStr = file['expDate'].split('T')[0].split('-')
        expDate = datetime.datetime(int(expDateStr[0]), int(expDateStr[1]), int(expDateStr[2]))
        now = datetime.datetime.now()
        diff = now - expDate
        if diff.total_seconds() / 60 > 1440:
            fileCode = file['id'] + "." + file['type']
            os.remove(UPLOAD_FOLDER+"/"+fileCode)
            files.delete_one({"id": file['id']})
            print("Deleted expired file: "+file['name'] + " (" + file['id'] + ")")
            filesDeleted = filesDeleted + 1
    return filesDeleted 

print(str(delete_old_files()) + " files deleted")