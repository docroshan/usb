from utilities.utility import *


def usb_rename_drive():
    print(f"{'*' * 20}TestCase started {blue('|usb_6.1|rename Drive|')}{'*' * 20}")
    mlabel(dev, usb_name)
    usb_rename = exec_command(f"mlabel -i {dev} -s").split()[-1]
    try:
        assert usb_rename == usb_name.upper()

    except AssertionError:
        print(f"Actual name of usb drive to be changed to {usb_name.upper()}")
        print(f"Renaming the drive failed, Expected name of the usb drive is {usb_rename.upper()}")
        print(red("FAIL"))

    else:
        print(f"Actual name of usb drive to be changed to {usb_name.upper()}")
        print(f"Renaming the drive failed, Expected name of the usb drive is {usb_rename.upper()}")
        print(green("PASS"))

    finally:
        usb_rename_to_original()
        print(f"{'*'*20}TestCase Ended {blue('|usb_6.1|Rename Drive|')}{'*'*20}\n")
        close()


# usb_rename_drive()
