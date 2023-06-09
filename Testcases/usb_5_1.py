from utilities.usb import *


@fun_count
def file_format_fat():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    fat_file_format()

    print(green("\nUSB Formatted using FAT FileSystem !!\n"))
    logger.info("USB Formatted with FAT FileSystem Successfully!!")

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    return 'PASS', None
