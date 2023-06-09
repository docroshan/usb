from utilities.usb import *


def usb_capacity():
    print(f"{'*'*20}TestCase started {blue('|usb_2.0|USB Capacity|')}{'*'*20}")
    available_usb()
    usbname = (data["current_usb_name"]).upper()
    path = dev_path(usbname)

    if path != "USB NOT FOUND":
        res = usb_df()
        try:
            assert data["total_storage"].upper() == (res[usbname]['Size'])

        except AssertionError:
            print(f"Actual Capacity of USB is {green(data['total_storage'])}")
            print(f"Expected result of of USB is {red(res[usbname]['Size'])}\n")
            print(red("FAIL"))

        else:
            print(f"Total Capacity of USB is {green(data['total_storage'])}")
            print(f"Expected result of of USB is {green(res[usbname]['Size'])}\n")
            print(green("PASS"))
            return res[usbname]['Size']

        finally:
            print(f"{'*'*20}TestCase ended {blue('|usb_2.0|USB Available Space|')}{'*'*20}\n")
            close()

    else:
        print("INSERT THE USB")


# usb_capacity()