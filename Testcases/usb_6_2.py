from utilities.utility import *


@fun_count
def usb_change_label():
    print(f"{'*' * 20}TestCase started {blue('|usb_6.2|Change Label|')}{'*' * 20}")
    logger.info(f"{'*' * 20}TestCase started {'|usb_6.2|Change Label|'}{'*' * 20}")
    path = dev
    print(path)
    mlabel(path, usb_name)
    usb_eject()
    usb_reconnect()
    rename = exec_command(f"mlabel -i {path} -s")

    try:
        assert usb_name.upper() == rename.split()[-1]

    except AssertionError:
        print(f"Actual name of USB for rename is {green(usb_name.upper())}")
        logger.info(f"Actual name of USB for rename is {usb_name.upper()}")
        print(f"Expected result of USB rename is {red(rename.split()[-1])}")
        error_msg = f"Expected result of USB rename is {rename.split()[-1]}"
        logger.info(f"Expected result of USB rename is {rename.split()[-1]}")
        print(f"{red('FAIL')}")
        logger.error('FAIL')
        return 'FAIL', error_msg

    else:
        print(f"Actual name of USB for rename is {green(usb_name.upper())}")
        logger.info(f"Actual name of USB for rename is {usb_name.upper()}")
        print(f"Expected result of USB rename is {green(rename.split()[-1])}")
        logger.info(f"Expected result of USB rename is {rename.split()[-1]}")
        print(f"{green('PASS')}")
        logger.info('PASS')
        return 'PASS', None

    finally:
        usb_rename_to_original()
        close()
        print(f"{'*'*20}TestCase Ended {blue('|usb_6.2|Change Label|')}{'*'*20}\n")
        logger.info(f"{'*'*20}TestCase Ended {'|usb_6.2|Change Label|'}{'*'*20}\n")


usb_change_label()
