from utilities.usb import *


def delete_file(name, path):

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20} \n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    remove_file(name, path)

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")
