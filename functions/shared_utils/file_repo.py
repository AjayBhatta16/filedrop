import random
import string
import boto3
import os

class FileRepo():
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def generateID(self):
        return ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(8)])

    def newFileID(self, file_queryable):
        id = self.generateID()
        fileQuery = file_queryable.find({"id": id})
        if len(list(fileQuery)) > 0:
            return self.newFileID()
        return id
    
    def saveFile(self):
        pass

    def getFile(self):
        pass

    def deleteFile(self, file_name):
        bucket_name = os.environ.get("S3_BUCKET_NAME")
        response = self.s3_client.delete_object(
            Bucket=bucket_name,
            Key=file_name
        )

        return response