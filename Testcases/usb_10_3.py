from utilities.usb import *


@fun_count
def safe_eject_drive():
    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    res = usb_safe_eject()

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    if res:
        return 'PASS', None
    else:
        return 'FAIL', 'USB Not Ejected or USB Not Found'
