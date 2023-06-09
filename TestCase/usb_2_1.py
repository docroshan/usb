from utilities.usb import *


def usb_available_space():
    print(f"{'*'*20}TestCase started {blue('|usb_2.1|USB Available Space|')}{'*'*20}")
    available_usb()
    usbname = data["current_usb_name"].upper()
    path = dev_path(usbname)
    if path != "USB NOT FOUND":
        res = usb_df()
        try:
            assert data["available_storage"] == (((res[usbname]['Avail']).split('/'))[-1])

        except AssertionError:
            print(red("FAIL"))

        else:
            print(f"Available space of USB is {green(data['available_storage'])}")
            print(f"Expected result of of USB is {green(res[usbname]['Avail'])}\n")
            print(green("PASS"))
            return res[usbname]['Avail']

        finally:
            print(f"{'*'*30}TestCase ended {blue('|usb_2.1|USB Available Space|')}{'*'*20}")
            close()

    else:
        print("INSERT THE USB")


# usb_available_space()
