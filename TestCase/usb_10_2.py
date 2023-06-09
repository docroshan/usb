from utilities.usb import *


def safe_eject_drive():
    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    usb_safe_eject()

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")
