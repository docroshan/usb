import logging

from utilities.usb import *


def usb_format():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    quick_file_format()

    print(green("\nUSB Formatted !!\n"))
    logger.info("USB Formatted Successfully!!")

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")
