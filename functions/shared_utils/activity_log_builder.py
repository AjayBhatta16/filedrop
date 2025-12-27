import datetime

class ActivityLogBuilder:
    def __init__(self):
        self.log = {
            "timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }

    def build(self):
        return self.log
    
    def with_request(self, req):
        ip = ""
        if req.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = req.environ['REMOTE_ADDR']
        else: 
            ip = req.environ['HTTP_X_FORWARDED_FOR']
        self.log["ipAddress"] = ip
        return self
    
    def with_lambda_event(self, event):
        ip = event["requestContext"]["http"]["sourceIp"]
        self.log["ipAddress"] = ip
        return self
    
    def with_action(self, action):
        self.log["action"] = action
        return self
    
    def with_display_name(self, display_name):
        self.log["displayName"] = display_name
        return self
    
    def with_file_id(self, file_id):
        self.log["fileID"] = file_id
        return self
    
    def with_username(self, username):
        self.log["username"] = username
        return self