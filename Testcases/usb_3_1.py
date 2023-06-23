from utilities.utility import *


@fun_count
def usb_unmount():
    print(f"{'*'*20}TestCase started {blue('|usb_3.1|USB Umounting|')}{'*'*20}")
    logger.info(f"{'*'*20}TestCase started {'|usb_3.1|USB Umounting|'}{'*'*20}")
    usb = usb_df()

    try:
        print(usb[current_usb_name.upper()]['Filesystem'])
        logger.info(usb[current_usb_name.upper()]['Filesystem'])
        unmount(usb[current_usb_name.upper()]['Filesystem'])
        usb_mount_point = exec_command(f"df | grep -w {dev}")
        assert (usb[current_usb_name.upper()]['Filesystem']) != usb_mount_point

    except TypeError:
        print("USB NOT MOUNTED")
        logger.error("USB NOT FOUND")

    except AssertionError:
        print(red('FAIL'))
        error_msg = "USB NOT MOUNTED"
        logger.error('FAIL')
        return 'FAIL', error_msg

    else:
        print("unmounting this Filesystem...........")
        logger.info("unmounting this Filesystem...........")
        print(f"{green('USB unmounted Successfully!!')}")
        logger.info(f"{'USB unmounted Successfully!!'}")
        print(green('PASS'))
        logger.info('PASS')
        return 'PASS', None

    finally:
        print(f"{'*'*20}TestCase ended {blue('|usb_3.1|USB Unmounting|')}{'*'*20}\n")
        logger.info(f"{'*'*20}TestCase ended {'|usb_3.1|USB Unmounting|'}{'*'*20}\n")
        close()


usb_unmount()
