import requests

url = "https://www.googleapis.com/deploymentmanager/v2/projects/testing-copen/global/deployments"


def _deploy(data: dict, token: str):
    payload = str(data)
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text


def _get_content(id: str, token:str):
    return {}
