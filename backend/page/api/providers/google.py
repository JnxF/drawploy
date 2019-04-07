import datetime
import json
import random
import string

import requests
from urllib3.connectionpool import xrange

from backend.settings import GOOGLE_PROJECT
from page import models

url_template = "https://www.googleapis.com/deploymentmanager/v2/projects/" + GOOGLE_PROJECT + "/global/deployments"
url_template_get = "https://www.googleapis.com/deploymentmanager/v2/projects/" + GOOGLE_PROJECT + "/global/deployments/"
url_operation_get = "https://www.googleapis.com/deploymentmanager/v2/projects/" + GOOGLE_PROJECT + "/global/operations/"
url_metrics_get = "https://monitoring.googleapis.com/v3/projects/" + GOOGLE_PROJECT + "/timeSeries/"


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


def _get_metrics(token: str, metric_name: str, machine_name: str):
    url_tmp = url_metrics_get
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': "application/json",
    }
    time_current = datetime.datetime.now()
    time_previous = time_current - datetime.timedelta(minutes=30)
    time_current = datetime.datetime.strftime(time_current, "%Y-%m-%dT%G:%i:00Z")
    time_previous = datetime.datetime.strftime(time_previous, "%Y-%m-%dT%G:%i:00Z")
    url_tmp += "?name=" + GOOGLE_PROJECT + "&filter==" + metric_name + "&interval.startTime=" + time_current + "&interval.endTime=" + time_previous
    response = requests.request("GET", url_tmp, headers=headers)
    if response:
        return json.loads(response.text)
    return {"url": url_tmp}
