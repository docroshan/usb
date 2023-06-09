from utilities.usb import *


def usb_version():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    # usb = USB(password, usb_name)
    # usb.usb_config()

    op = str(super_access('fubeus@12', 'lsusb -v | grep -B 23 "Mass Storage" | grep id'))
    id = []
    regex = re.findall(r'\d{1}x\d{4}', op)

    for reg in range(0, len(regex), 2):
        id.append(f"{regex[reg].split('x')[-1]}:{regex[reg+1].split('x')[-1]}")

    for i in id[:1]:
        port = str(super_access('fubeus@12', f"lsusb -v -d {i} | grep bcdUSB"))

        print("Expected Results:", green(float(port_ver)))
        print("Actual Results:", green(float(port.split('\n')[0].split()[-1])))
        n = '\n'
        logging.info(f"Expected Results: {float(port_ver)}")
        logging.info(f"Actual Results: {float(port.split(n)[0].split()[-1])}")

        try:
            assert float(port.split('\n')[0].split()[-1]) == float(port_ver)
            print(yellow("Port Version matched !!"))
            print(green("\n\tPASS\n"))
            logging.info("Port Version matched !!\n")
            logging.info("\tPASS\n")

        except AssertionError:
            print(red("Port Version mis-matched !!\n"))
            print(red("\n\tFAIL\n"))
            logging.info("Port Version mis-matched !!\n")
            logging.error("\tFAIL\n")

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")
