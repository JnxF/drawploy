import uuid

import requests

from backend.settings import GOOGLE_PROJECT

url_template = "https://www.googleapis.com/deploymentmanager/v2/projects/" + GOOGLE_PROJECT + "/global/deployments"


def _deploy(data: dict, token: str):
    payload = str(data)
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    # response = requests.request("POST", url_deploy, data=payload, headers=headers)
    # return response.text
    return {"state": 0}


def _get_content(id: str, token: str):
    return {}


def _create_content(data: dict, token: str):
    payload = {
        "name": "example-config-with-templates-2",
        "target": {
            "config": {
                "content": data
            }
        }
    }
    payload = str(payload)
    print(payload)
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("POST", url_template, data=payload, headers=headers)
    return response.text
