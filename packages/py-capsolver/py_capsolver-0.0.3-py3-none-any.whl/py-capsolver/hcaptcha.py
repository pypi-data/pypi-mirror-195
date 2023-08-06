import requests, time
from .exceptions import *


class HCaptcha:  # check dc
    # kk

    def __init__(self, client_key: str, beta: bool = False) -> None:

        self.client_key = client_key
        self.session = requests.Session()
        self.basesite = "https://api.capsolver.com/createTask"
        self.retrys = 0

    def create_task(self, url: str, sitekey: str, isInvisble: bool = False):
        headers = {"Content-Type": "application/json"}

        json = {
            "clientKey": self.client_key,
            "task": {
                "type": "HCaptchaTaskProxyLess",
                "websiteURL": url,
                "websiteKey": sitekey,
                "isInvisible": isInvisble,
                "enterprisePayload": {"rqdata": ""},
                "proxy": "",
                "userAgent": "",
            },
        }

        self.response = self.session.post(self.basesite, headers=headers, json=json)

        if self.response.status_code == 400:
            raise HCaptchaError(self.response.text, self.response.status_code)

        return self.response.json()["taskId"]

    def join_task_together(self, taskId: str):

        self.task_id = taskId

        headers = {"Content-Type": "application/json"}
        json = {"clientKey": self.client_key, "taskId": self.task_id}
        while True:
            response = self.session.post("https://api.capsolver.com/getTaskResult", json=json, headers=headers).json()

            if response["status"] == "processing":
                time.sleep(1)
                self.retrys += 1
                continue
            elif response["status"] == "ready":
                return response["solution"]["gRecaptchaResponse"]
                break
            elif self.retrys == 90:  # go to discord
                raise HCaptchaError("MAX RETRYS", 400)
