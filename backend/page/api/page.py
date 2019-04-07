import uuid
from collections import OrderedDict
from difflib import SequenceMatcher

import yaml
import requests, json, os
import base64
import io

import cv2
import imutils
import numpy as np
from PIL import Image
from imutils.perspective import four_point_transform
from skimage.filters import threshold_local

from backend.settings import AZURE_KEY, GOOGLE_PROJECT
from page import models
from page.api.providers.google import _deploy, _create_content, _get_list, _get_status
from page.enums import google_resource_type, resource_names, google_property_type
import uuid

from .machine import Square
import operator
import math

def find_closest_google_center(center: str):
    keys = ["asia-east1", "asia-east2", "asia-northeast1", "asia-south1", "asia-southeast1", "australia-southeast1", "europe-north1", "europe-west1", "europe-west2", "europe-west3", "europe-west4", "europe-west6", "northamerica-northeast1", "southamerica-east1", "us-central1", "us-east1", "us-east4", "us-west1", "us-west2", "eu-central", "eu-west2", "eu-west3",
    "eu-west4", "eu-west6", "northamerica-northeast", "southameerica-east", "us-central"]
    center = center.lower()
    keys = sorted(keys, key = lambda x : SequenceMatcher(None, x, center).ratio(), reverse = True)
    return keys[0], SequenceMatcher(None, keys[0], center).ratio()


def find_type(label: str):
    values = {
        "vm": 0,
        "net": 2,
        "dk": 1,
        "db": 3,
    }

    label = label.lower()

    keys = list(values.keys())
    keys = sorted(keys, key = lambda x : SequenceMatcher(None, x, label).ratio(), reverse = True)
    best_one = keys[0]
    result = values[best_one]
    return result


def compute_centre(bounding):
    x = bounding[0] + (bounding[0] - bounding[3])/2
    y = bounding[1] + (bounding[1] - bounding[7])/2
    return x, y

def compute_distance(obj1, obj2):
    return math.sqrt(pow(obj2[0]-obj1[0], 2) + pow(obj2[1]-obj1[1], 2))

def get_text(image: str):
    headers = {
        'Content-Type': "application/octet-stream",
        'Ocp-Apim-Subscription-Key': "928d25e00c4b453e8db0b334d8bfc6fc",
    }
    url = "https://australiaeast.api.cognitive.microsoft.com/vision/v2.0/recognizeText?mode=Handwritten"

    res = requests.post(url=url,
                        headers=headers,
                        data=base64.decodebytes(image.encode("ascii")))
    if res.status_code == 202:
        d = {'status': 'Running'}
        while(d['status'] == 'Running'):
            r = requests.get(res.headers['Operation-Location'], headers=headers)
            d = json.loads(r.content)
            print(d)
        network = {}
        squares = []
        foundCenter = None

        elements = {
            0: [],
            1: [],
            2: [],
            3: []
        }
        elements_copy = {}
        for l in d['recognitionResult']['lines']:
            for w in l['words']:
                closest, probability = find_closest_google_center(l['text'])
                if probability > 0.8:
                    foundCenter = closest
                    continue
                t = find_type(w['text'])
                uid = str(uuid.uuid4())
                w['id'] = uid
                elements[t].append(w)
                elements_copy[uid] = {
                    'type': t,
                    'linked': []
                }
        for key,element in elements.items():
            for item in element:
                cntr1 = compute_centre(item['boundingBox'])
                if( key == 0 ):
                    for key2 in [1,2,3]:
                        for element3 in elements[key2]:
                            cntr2 = compute_centre(element3['boundingBox'])
                            dis = compute_distance(cntr1, cntr2)
                            if( dis < 450 and key2 == 2):
                                elements_copy[item['id']]['linked'].append(element3['id'])
                            if( dis < 600 and key2 == 3):
                                elements_copy[item['id']]['linked'].append(element3['id'])
                if(key == 1):
                    for key2 in [0]:
                        prop = None
                        prop2 = None
                        dist = 10000
                        dist2 = 10000
                        for element3 in elements[key2]:
                            cntr2 = compute_centre(element3['boundingBox'])
                            dis = compute_distance(cntr1, cntr2)
                            if( dis < 750 and key2 == 0 and (dis < dist or dis < dist2)):
                                disk = False
                                for d in elements_copy[element3['id']]['linked']:
                                    disk = (elements_copy[d]['type'] == 1 or disk)
                                if(not disk and dis<dist):
                                    prop = element3['id']
                                    dist = dis
                                elif(dis < dist2):
                                    prop2 = element3['id']
                                    dist2 = dis
            
                        if(prop):
                            elements_copy[prop]['linked'].append(item['id'])
                        elif(prop2):
                            elements_copy[prop2]['linked'].append(item['id'])

                
        return elements_copy, foundCenter
    #VERY BAD
    return dict(), None

def detectDraw(base64request: str):

    def base64toImage(base64_string):
        imgdata = base64.b64decode(str(base64_string))
        image = Image.open(io.BytesIO(imgdata))
        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

    def cleanImage(image):
        # image = cv2.imread(image)
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)
        height, width, _ = image.shape



        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 250)

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]


        if cv2.contourArea(cnts[0]) < 0.4 * width * height:
            print("Adiosita")
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        screenCnt = -1
        defined = False

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                defined = True
                break

        if not defined:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # show the contour (outline) of the piece of paper
        print("STEP 2: Find contours of paper")
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        # cv2.imshow("Outline", image)

        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = threshold_local(warped, 11, offset=10, method="gaussian")
        warped = (warped > T).astype("uint8") * 255

        print("STEP 3: Apply perspective transform")

        cv2.imshow("Scanned", imutils.resize(warped, height=650))
        cv2.waitKey(0)
        return warped

    def detectContours(neta):
        blurred = cv2.GaussianBlur(neta, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        _, cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

        cnts = imutils.grab_contours(cnts)
        detected = []

        i = 0
        for c in cnts:
            area = cv2.contourArea(c)

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            vertex = len(approx)

            print("Trobat contorn", area, vertex)
            x, y, w, h = cv2.boundingRect(c)

            detected.append([x, y, x + w, y, x + w, y + h, x, y + h])

            cv2.drawContours(final, [c], 0, (0, 255 - i , 255 - i), 3)

            i += 60

        cv2.imshow("Scanned", imutils.resize(final, height=650))
        cv2.waitKey(0)

        cv2.destroyAllWindows()

        return detected

    imatge = base64toImage(base64request)
    neta = cleanImage(imatge)
    detectados = detectContours(neta)

    result = dict()
    for i, d in enumerate(detectados):
        result[str(uuid.uuid4())] = {
            "type": 0,
            "linked" : []
        }

    return result


def create(image: str, token: str, email: str):
    infrastructure, foundCenter = get_text(image)
    foundCenter = foundCenter if foundCenter is not None else "us-central1-f"
    # infrastructure = detectDraw(image)
    infrastructure_2 = {
        "81b98e47-6eea-43f8-a34c-70354464d160": {
            "type": 0,
            "linked": ["c9f83a36-b35e-4808-8479-ff6876fc8df2", "37315dae-34af-4877-8344-a759c34e68b3"]
        },
        "c9f83a36-b35e-4808-8479-ff6876fc8df2": {
            "type": 1,
            "linked": []
        },
        "37315dae-34af-4877-8344-a759c34e68b3": {
            "type": 2,
            "linked": []
        }
    }
    infrastructure_json = infrastructure_to_json(infrastructure, google_resource_type, google_property_type, foundCenter)
    infrastructure_yaml = infrastructure_to_yaml(infrastructure_json)
    result = _create_content(infrastructure_yaml, token)
    result["code"] = infrastructure_json
    if result["status"] == "RUNNING":
        deployment = models.Deployment(id=result["targetId"], name=result["targetName"], email=email, target=json.dumps(infrastructure_json))
        deployment.save()
    return {"content": result}


def retrieve(token: str, email=None, pk=None):
    deployment = models.Deployment.objects.filter(id=int(pk), email=email).first()
    if not deployment:
        return {"content": dict()}
    result = dict()
    result["code"] = json.loads(deployment.target)
    result["id"] = pk
    return {"content": result}


def update(content: str, token: str, email: str, pk=id):
    return {"status": 0}


def _list(token: str, email: str):
    result = _get_list(token)
    if "deployments" in result:
        return {"content": result["deployments"]}
    return {"content": []}


def status(token: str, operation_name: str, email: str, pk: str):
    result = _get_status(token, operation_name)
    return {"content": result}


def infrastructure_to_json(infrastructure: dict, translate_resource: list, translate_type: list, zone: str):
    infrastructure_aux = OrderedDict()
    infrastructure_aux["resources"] = []
    i = 0
    for element_id, element in infrastructure.items():
        if element["type"] == 0:
            element_translated = OrderedDict()
            element_translated["type"] = translate_resource[element["type"]]
            element_translated["name"] = resource_names[element["type"]] + "-" + str(i)
            element_translated["properties"] = OrderedDict()
            element_translated["properties"]["zone"] = zone
            element_translated["properties"]["machineType"] = "https://www.googleapis.com/compute/v1/projects/" + GOOGLE_PROJECT + "/zones/us-central1-f/machineTypes/f1-micro"
            for element_nested in element["linked"]:
                if element["type"] == 0 and (infrastructure[element_nested]["type"] == 1 or infrastructure[element_nested]["type"] == 2):
                    if translate_type[infrastructure[element_nested]["type"]] not in element_translated["properties"]:
                        element_translated["properties"][translate_type[infrastructure[element_nested]["type"]]] = []
                    element_current = OrderedDict()
                    if infrastructure[element_nested]["type"] == 1:
                        element_current["deviceName"] = "name"
                        element_current["type"] = "PERSISTENT"
                        element_current["boot"] = True
                        element_current["autoDelete"] = True
                        element_current["initializeParams"] = {"sourceImage": "https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/family/debian-9"}
                        list.append(element_translated["properties"][translate_type[infrastructure[element_nested]["type"]]], element_current)
                    elif infrastructure[element_nested]["type"] == 2:
                        element_current["network"] = "https://www.googleapis.com/compute/v1/projects/" + GOOGLE_PROJECT + "/global/networks/default"
                        element_current["accessConfigs"] = [{"name": "External NAT", "type": "ONE_TO_ONE_NAT"}]
                        list.append(element_translated["properties"][translate_type[infrastructure[element_nested]["type"]]], element_current)
            list.append(infrastructure_aux["resources"], element_translated)
            i += 1
    yaml.add_representer(OrderedDict, represent_ordereddict)
    return infrastructure_aux


def infrastructure_to_yaml(infrastructure: dict):
    return yaml.dump(infrastructure, allow_unicode=True)


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)
