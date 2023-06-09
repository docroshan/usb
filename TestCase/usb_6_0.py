from utilities.usb import *


def usb_rename_drive():
    print(f"{'*' * 20}TestCase started {blue('|usb_6.0|Rename Drive|')}{'*' * 20}")
    mlabel(dev, usb_name)
    rename = exec_command(f"mlabel -i {dev} -s")

    try:
        assert usb_name.upper() == rename.split()[-1]

    except AssertionError:
        print(f"Actual name of USB for rename is {green(usb_name.upper())}")
        print(f"Expected result of USB rename is {red(rename.split()[-1])}")
        print(f"{red('FAIL')}")

    else:
        print(f"Actual name of USB for rename is {green(usb_name.upper())}")
        print(f"Expected result of USB rename is {green(rename.split()[-1])}")
        print(f"{green('PASS')}")

    finally:
        usb_rename_to_original()
        close()
        print(f"{'*'*20}TestCase Ended {blue('|usb_6.0|Rename Drive|')}{'*'*20}\n")

# usb_rename_drive()
