from utilities.usb import *


@fun_count
def get_usb_name():
    global d

    print(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    usb = USB(password, usb_name)
    usb.usb_config()

    time.sleep(0.7)  # required time gap: else file is not updated
    flag = 0
    try:
        d = super_access(password, f"mlabel -i {dev} -s").strip().split()[-1]
    except AttributeError:
        print("No USB Found !!")

    print("Expected Results:", usb_name)
    logger.info(f"Expected Results:{usb_name}")

    print("Actual Results:", d.lower())
    logger.info(f"Actual Results:{d.lower()}")

    try:
        assert d.lower() == usb_name.lower()
        print("Name matched !!")
        print("\n\tPass\n")
        logger.info("Name matched !!\n")
        logger.info("\tPASS\n")
        flag += 1

    except AssertionError:
        print("Name mis-matched !!")
        print("\n\tFAIL\n")
        logger.error("Name mis-matched !!")
        logger.error("\tFail\n")

    usb_rename_to_original()

    print("*" * 20, os.path.basename(__file__), "Test Case Completed", "*" * 20, "\n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    if flag:
        return 'PASS', None
    else:
        return 'FAIL', 'Name mis-matched'


get_usb_name()
