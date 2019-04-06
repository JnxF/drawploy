import yaml

from page.enums import google_resource_type, resource_names, google_property_type


def create(image: str):
    # Infrastructure format
    # - resource
    #     - id
    #     - type
    #     - properties
    #         - property 1
    #         - property 2
    #         - ...
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
    infrastructure_aux = dict()
    infrastructure_aux["resources"] = []
    i = 0
    for element_id, element in infrastructure.items():
        element_translated = dict()
        element_translated["type"] = translate_resource[element["type"]]
        element_translated["name"] = resource_names[element["type"]] + "-" + str(i)
        element_translated["properties"] = dict()
        element_translated["properties"]["zone"] = zone
        '''for property_name, property_values in element["properties"].items():
            element_translated["properties"][translate_type[property_name]] = dict()'''
        list.append(infrastructure_aux["resources"], element_translated)
        i += 1
    infrastructure_yaml = yaml.dump(infrastructure_aux, allow_unicode=True)
    return infrastructure_yaml
