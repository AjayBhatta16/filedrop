import random
import string

class FileRepo():
    def __init__(self):
        pass

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

    def deleteFile(self):
        pass