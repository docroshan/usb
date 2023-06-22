from utilities.usb import *


@fun_count
def usb_mount_point():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    usb = USB(password, usb_name)
    usb.usb_config()

    sleep(0.7)

    ssh = ssh_connect(ip, user_name, password)
    stdin, stdout, stderr = ssh.exec_command(f'df | grep {dev}')

    d = stdout.read().decode().split('% ')[-1].strip()
    flag = 0

    print("Expected Results:", yellow(mount_point))
    print("Actual Results:", green(d.lower()))

    logger.info(f"Expected Results: {mount_point}")
    logger.info(f"Actual Results: {d.lower()}")

    try:
        assert mount_point.lower() == d.lower()
        print(yellow("Mount Point matched !!"))
        print(green("\n\tPass\n"))
        logger.info("Mount Point matched !!\n")
        logger.info("\tPASS\n")
        flag += 1

    except AssertionError:
        print(red("Mount Point mis-matched !!"))
        print(red("\n\tFAIL\n"))
        logger.error("Mount Point mis-matched !!\n")
        logger.error("\tFAIL\n")

    usb_rename_to_original()

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    if flag:
        return 'PASS', None
    else:
        return 'FAIL', 'Mount Point mis-matched'


usb_mount_point()
