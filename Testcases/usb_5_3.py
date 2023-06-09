from utilities.usb import *


def file_format_exfat():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    exfat_file_format()

    print(green("\nUSB Formatted using EX-FAT FileSystem !!\n"))
    logger.info("USB Formatted with EX-FAT FileSystem Successfully!!")

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    return 'PASS', None
