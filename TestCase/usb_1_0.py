from utilities.usb import *


def get_usb_name():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    usb = USB(password, usb_name)
    usb.usb_config()

    time.sleep(0.7)  # required time gap: else file is not updated

    d = super_access(password, f"mlabel -i {dev} -s").strip().split()[-1]

    print("Expected Results:", yellow(usb_name))
    logging.info(f"Expected Results:{usb_name}")

    print("Actual Results:", green(d.lower()))
    logging.info(f"Actual Results:{d.lower()}")

    try:
        assert d.lower() == usb_name.lower()
        logging.info("Name matched !!\n")
        logging.info("\tPASS\n")
        print(yellow("Name matched !!"))
        print(green("\n\tPass\n"))

    except AssertionError:
        logging.info("Name mis-matched !!")
        logging.error("\tFail\n")
        print(red("Name mis-matched !!\n"))
        print(red("\n\tFAIL\n"))

    usb_rename_to_original()

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")
