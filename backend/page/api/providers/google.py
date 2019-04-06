import uuid

import requests

from backend.settings import GOOGLE_PROJECT

url_deploy = "https://www.googleapis.com/deploymentmanager/v2/projects/" + GOOGLE_PROJECT + "/global/deployments"
url_template = "https://www.googleapis.com/compute/v1/projects/" + GOOGLE_PROJECT + "/global/instanceTemplates"


def _deploy(data: dict, token: str):
    payload = str(data)
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("POST", url_deploy, data=payload, headers=headers)
    return response.text


def _get_content(id: str, token:str):
    return {}


def _create_content(data: dict, token:str):
    payload = dict()
    payload["name"] = str(uuid.uuid4())

    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("POST", url_template, data=payload, headers=headers)
    return response.text

