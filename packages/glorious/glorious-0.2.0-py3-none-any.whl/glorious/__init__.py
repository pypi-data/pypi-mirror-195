from typing import Type

from .devices import *
from .protocol import *


def device(device_dict):
    """Returns a device class depending on the device_dict passed in"""

    if device_dict["vendor_id"] != 9610:
        raise ValueError("Invalid device_dict!")

    product_id = device_dict["product_id"]
    product = SUPPORTED_DEVICES[product_id] # raises KeyError if no device was found

    # product references a class, so create an instance of it 
    device = product(device_dict)
    
    return device


def supported(kind: Type[Device] = None, device_dicts: list[dict] = hid.enumerate().copy()) -> list[Device]:
    """
    Return a list of device classes with all the supported devices connected.
    If device_dicts is not specified, hid.enumerate() is used.
    """

    # check for glorious vendor id
    glorious_devices = [d for d in device_dicts if d["vendor_id"] == 0x258a]

    # remove duplicates
    supported_devices = []

    for device_dict in glorious_devices:
        if device_dict["product_string"] not in [
            device.product_string for device in supported_devices
        ]:
            supported_devices.append(device(device_dict))

    if kind:
        return [d for d in supported_devices if type(d) is kind]
    else:
        return supported_devices
