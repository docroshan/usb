from utilities.utility import *


def usb_unmount():
    print(f"{'*'*20}TestCase started {blue('|usb_3.1|USB Umounting|')}{'*'*20}")
    usb = usb_df()
    print("unmounting this Filesystem...........")
    print(usb[current_usb_name.upper()]['Filesystem'])
    unmount(usb[current_usb_name.upper()]['Filesystem'])
    print(f"{green('USB unmounted Successfully!!')}")
    print(f"{'*'*20}TestCase ended {blue('|usb_3.1|USB Unmounting|')}{'*'*20}\n")
    close()


# usb_unmount()
