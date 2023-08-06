import requests
from base64 import b64encode

class Jira():
    def __init__(self, url, usr, pwd):
        self.url = url
        self.user = usr
        self.pwd = pwd
    
    def load_key(self):
        url = self.url + '/rest/api/2/user/search'

        querystring = {"username":self.user}

        headers = {
            "Authorization": "Basic " + b64encode(f"{self.user}:{self.pwd}".encode('utf-8')).decode("ascii")
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            return response.json()[0]["key"]
        else:
            return None
