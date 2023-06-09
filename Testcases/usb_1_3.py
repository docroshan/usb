from utilities.usb import *


@fun_count
def usb_version():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    # usb = USB(password, usb_name)
    # usb.usb_config()

    op = str(super_access('fubeus@12', 'lsusb -v | grep -B 23 "Mass Storage" | grep id'))
    id = []
    flag = 0
    regex = re.findall(r'\d{1}x\d{4}', op)

    for reg in range(0, len(regex), 2):
        id.append(f"{regex[reg].split('x')[-1]}:{regex[reg+1].split('x')[-1]}")

    for i in id[:1]:
        port = str(super_access('fubeus@12', f"lsusb -v -d {i} | grep bcdUSB"))

        print("Expected Results:", green(float(port_ver)))
        print("Actual Results:", green(float(port.split('\n')[0].split()[-1])))
        n = '\n'
        logger.info(f"Expected Results: {float(port_ver)}")
        logger.info(f"Actual Results: {float(port.split(n)[0].split()[-1])}")

        try:
            assert float(port.split('\n')[0].split()[-1]) == float(port_ver)
            print(yellow("Port Version matched !!"))
            print(green("\n\tPASS\n"))
            logger.info("Port Version matched !!\n")
            logger.info("\tPASS\n")
            flag += 1

        except AssertionError:
            print(red("Port Version mis-matched !!"))
            print(red("\n\tFAIL\n"))
            logger.error("Port Version mis-matched !!\n")
            logger.error("\tFAIL\n")

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    if flag:
        return 'PASS', None
    else:
        return 'FAIL', 'Port Version Mis-matched'


# usb_version()
