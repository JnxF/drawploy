import enum


class ResourceType(enum.IntEnum):
    VM: 0
    DISK: 1
    NETWORK: 2
    DATABASE: 3


resource_names = ["vm", "disk", "network", "database"]
google_resource_type = ["compute.v1.instance", "holita1", "holita2", "gcp-types/sqladmin-v1beta4:instances"]
google_property_type = ["holita0", "disks", "networkInterfaces", "holita3"]
