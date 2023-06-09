from utilities.utility import *


class USB:

    def __init__(self, password, usb_name):
        self.password = password
        self.usb_name = usb_name

    def usb_config(self):

        fat_file_format()
        mlabel(dev, usb_name)
        usb_eject()
        usb_reconnect()
