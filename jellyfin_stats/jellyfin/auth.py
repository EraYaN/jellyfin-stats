import requests

class JellyfinAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["x-mediabrowser-token"] = self.token
        return r