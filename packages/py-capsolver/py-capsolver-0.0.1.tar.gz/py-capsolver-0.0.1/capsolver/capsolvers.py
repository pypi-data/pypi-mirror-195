import requests

class CAPSOLVER:
    def __init__(self, client_key: str):
        self.client_key = client_key
        self.session = requests.Session()

    def checkbalance(self):
        headers = {"Content-Type": "application/json"}
        json = {"clientKey": self.client_key}
      
        response = self.session.post("https://api.capsolver.com/getBalance", headers=headers, json=json).json()
        return response
