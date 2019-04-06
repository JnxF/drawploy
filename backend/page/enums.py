import enum


class ResourceType(enum.IntEnum):
    VM: 0
    DISK: 1
    NETWORK: 2


resource_names = ["vm", "disk", "network"]
google_resource_type = ["compute.v1.instance", "holita1", "holita2"]
google_property_type = ["holita0", "disks", "networkInterfaces"]
