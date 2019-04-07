import json
import random
import string

import requests
from urllib3.connectionpool import xrange

from backend.settings import GOOGLE_PROJECT
from page import models

url_template = "https://www.googleapis.com/deploymentmanager/v2/projects/" + GOOGLE_PROJECT + "/global/deployments"
url_template_get = "https://www.googleapis.com/deploymentmanager/v2/projects/" + GOOGLE_PROJECT + "/global/deployments/"
url_operation_get = "https://www.googleapis.com/deploymentmanager/v2/projects/" + GOOGLE_PROJECT + "/global/operation/"


def _deploy(data: dict, token: str):
    payload = str(data)
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    # response = requests.request("POST", url_deploy, data=payload, headers=headers)
    # return response.text
    return {"state": 0}


def _get_list(token: str):
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("GET", url_template, headers=headers)
    if response:
        return json.loads(response.text)
    return dict()


def _create_content(data: dict, token: str):
    name = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(26)]).lower()
    payload = {
        "name": name,
        "target": {
            "config": {
                "content": data
            }
        }
    }
    payload = str(payload)
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("POST", url_template, data=payload, headers=headers)
    return_data = json.loads(response.text)
    return_data["targetName"] = name
    return_data["targetTarget"] = data
    return return_data


def _get_status(token: str, operation_name: str):
    url_tmp = url_operation_get + operation_name
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("GET", url_tmp, headers=headers)
    if response:
        return json.loads(response.text)
    return dict()
