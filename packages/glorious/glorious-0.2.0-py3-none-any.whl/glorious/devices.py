import hid

from .protocol import Config, Report


class Device(hid.device):
    """Base class for all devices defined in this package"""

    def __init__(self, device_dict):
        self.device_dict = device_dict

        for key, value in self.device_dict.items():
            setattr(self, key, value)

    def open(self):
        """The same as hid.device.open(), but supports the context manager protocol"""
        super().open(
            self.vendor_id,
            self.product_id,
            self.serial_number
        )

        return self


    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

class ModelOWireless(Device):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def battery(self) -> int:
        # get battery percentage
        data = Report.get(Report.BATTERY, device=self)
        self.battery_percent = data[8]

        return self.battery_percent
    
    @property
    def wired(self) -> bool:
        all_device_dicts = hid.enumerate()

        # product ID determines if it's wired; remove it
        def new_dict(old_dict):
            new = old_dict.copy()
            new.pop('product_id')
            return new

        all_without_product_id = [
            new_dict(device_dict)
            for device_dict in all_device_dicts
        ]
        own_without_product_id = new_dict(self.device_dict)

        index = all_without_product_id.index(own_without_product_id)
        product_id = all_device_dicts[index]['product_id']
        if product_id == 8209:
            return True # mouse is wired 
        elif product_id == 8226:
            return False
    
    @property
    def firmware(self) -> str:
        if self.wired:
            data = Report.get(Report.FIRMWARE_WIRED, device=self)
        else:
            data = Report.get(Report.FIRMWARE_WIRELESS, device=self)
        
        self.firmware_version = f"{data[7]}.{data[8]}.{data[9]}.{data[10]}"

        return self.firmware_version


    @property
    def profile(self) -> int:
        raise NotImplementedError # TODO
    
    @profile.setter
    def profile(self, val: int):
        Config.send(Config.PROFILE, self, val)


# supported products, along with their respective classes
SUPPORTED_DEVICES = {
    # product ID determines if mouse is plugged in (8209 plugged in, 8226 not)
    0x2011: ModelOWireless, # 8209
    0x2022: ModelOWireless, # 8226
}
