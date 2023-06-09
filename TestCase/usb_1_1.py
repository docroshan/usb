from utilities.usb import *


def usb_mount_point():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    usb = USB(password, usb_name)
    usb.usb_config()

    sleep(0.7)

    ssh = ssh_connect(ip, user_name, password)
    stdin, stdout, stderr = ssh.exec_command(f'df | grep {dev}')

    d = stdout.read().decode().split('% ')[-1].strip()

    print("Expected Results:", yellow(mount_point))
    print("Actual Results:", green(d.lower()))
    logging.info(f"Expected Results: {mount_point}")
    logging.info(f"Actual Results: {d.lower()}")

    try:
        assert mount_point.lower() == d.lower()
        print(yellow("Mount Point matched !!"))
        print(green("\n\tPass\n"))
        logging.info("Mount Point matched !!\n")
        logging.info("\tPASS\n")

    except AssertionError:
        print(red("Mount Point mis-matched !!"))
        print(red("\n\tFAIL\n"))
        logging.info("Mount Point mis-matched !!\n")
        logging.error("\tFAIL\n")

    usb_rename_to_original()

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")
