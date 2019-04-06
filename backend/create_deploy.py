import requests

url = "https://www.googleapis.com/deploymentmanager/v2/projects/testing-copen/global/deployments"

payload = "{\n \"name\": \"example-config-with-templates\",\n \"target\": {\n  \"config\": {\n   \"content\": \"resources:\\n- name: vm-created-by-cloud-config\\n  type: compute.v1.instance\\n  properties:\\n    zone: us-central1-a\\n    machineType: https://www.googleapis.com/compute/v1/projects/myproject/zones/us-central1-a/machineTypes/n1-standard-1\\n    disks:\\n    - deviceName: boot\\n      type: PERSISTENT\\n      boot: true\\n      autoDelete: true\\n      initializeParams:\\n        diskName: disk-created-by-cloud-config\\n        sourceImage: https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/debian-7-wheezy-v20151104\\n    networkInterfaces:\\n    - network: https://www.googleapis.com/compute/v1/projects/myproject/global/networks/default\\n\"\n  }\n }\n}"
headers = {
    'Authorization': "Bearer ya29.GlvjBp4axgmnZ8eXqRgILovURnbiyKo7WlictjX0Q29NV5lMXkyKsamfoik7RK8DqHPm1lsjJtwPoGfB9q3z9-YWLcA55oLh73c4S1q6SNwcsWGucrxojuAFvDs8",
    'Content-Type': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)