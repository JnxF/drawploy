from collections import OrderedDict

import yaml
import requests, json, os 

from page.enums import google_resource_type, resource_names, google_property_type

def get_text(image: str):
    headers = {
        'Content-Type': "application/octet-stream",
        'Ocp-Apim-Subscription-Key': os.environ['AZURE_KEY'],
    }
    url = "https://australiaeast.api.cognitive.microsoft.com/vision/v2.0/recognizeText?mode=Handwritten"

    res = requests.post(url=url,
                        headers=headers,
                        data=image)

    if res.status_code == 202:
        d = {'status': 'Running'}
        while(d['status'] == 'Running'):
            r = requests.get(res.headers['Operation-Location'], headers=headers)
            d = json.loads(r.content)
        return d['recognitionResult']
    
    #VERY BAD
    return None

def detectDraw(base64request: str):
    import base64
    import io

    import cv2
    import imutils
    import numpy as np
    from PIL import Image
    from imutils.perspective import four_point_transform
    from skimage.filters import threshold_local

    def base64toImage(base64_string):
        imgdata = base64.b64decode(str(base64_string))
        image = Image.open(io.BytesIO(imgdata))
        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

    def cleanImage(image):
        # image = cv2.imread(image)
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)

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

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break

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
        edges = cv2.Canny(neta, 100, 200)
        edges = cv2.dilate(edges, None, iterations=1)
        edges = cv2.erode(edges, None, iterations=1)

        im2, cnts, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        final = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

        detected = []

        for c in cnts:
            area = cv2.contourArea(c)
            if area < 300:
                continue

            x, y, w, h = cv2.boundingRect(c)

            detected.append([x, y, x + w, y, x + w, y + h, x, y + h])

            cv2.drawContours(final, [c], 0, (0, 255, 255), 3)

        cv2.imshow("Scanned", imutils.resize(final, height=650))
        cv2.waitKey(0)

        cv2.destroyAllWindows()

        return detected

    imatge = base64toImage(base64request)
    neta = cleanImage(imatge)
    detectados = detectContours(neta)
    return detectados


def create(image: str):
    # Infrastructure format
    # - resource
    #     - id
    #     - type
    #     - properties
    #         - property 1
    #         - property 2
    #         - ...
    
    ocr_result = get_text(image)
    shapes = detectDraw(image)
    infrastructure = []

    infrastructure_example = {
        "81b98e47-6eea-43f8-a34c-70354464d160": {
            "type": 0,
            "properties": {
                "disks": ["c9f83a36-b35e-4808-8479-ff6876fc8df2"],
                "networks": ["37315dae-34af-4877-8344-a759c34e68b3"]
            }
        },
        "c9f83a36-b35e-4808-8479-ff6876fc8df2": {
            "type": 1,
            "properties": {}
        },
        "37315dae-34af-4877-8344-a759c34e68b3": {
            "type": 2,
            "properties": {}
        }
    }
    infrastructure_yaml = infrastructure_to_yaml(infrastructure_example, google_resource_type, google_property_type, "us-central1-f")
    return {"content": infrastructure_yaml}


def infrastructure_to_yaml(infrastructure: dict, translate_resource: list, translate_type: list, zone: str):
    infrastructure_aux = OrderedDict()
    infrastructure_aux["resources"] = []
    i = 0
    for element_id, element in infrastructure.items():
        element_translated = OrderedDict()
        element_translated["type"] = translate_resource[element["type"]]
        element_translated["name"] = resource_names[element["type"]] + "-" + str(i)
        element_translated["properties"] = OrderedDict()
        element_translated["properties"]["zone"] = zone
        '''for property_name, property_values in element["properties"].items():
            element_translated["properties"][translate_type[property_name]] = dict()'''
        list.append(infrastructure_aux["resources"], element_translated)
        i += 1
    yaml.add_representer(OrderedDict, represent_ordereddict)
    infrastructure_yaml = yaml.dump(infrastructure_aux, allow_unicode=True)
    print(infrastructure_yaml)
    return infrastructure_yaml


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)
