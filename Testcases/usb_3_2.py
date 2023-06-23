from utilities.utility import *


@fun_count
def usb_mount():
    sleep(0.4)
    print(f"{'*'*20}TestCase started {blue('|usb_3.2|USB mounting|')}{'*'*20}")
    logger.info(f"{'*'*20}TestCase started {'|usb_3.2|USB mounting|'}{'*'*20}")
    mount_point = mount(current_usb_name)
    if mount_point is not None:
        if mount_point == f"{current_usb_name} is already mounted":
            print(mount_point)
            logger.info(mount_point)
            print(green("PASS"))
            logger.info("PASS")
            print(f"{'*' * 20}TestCase Ended {blue('|usb_3.1|USB mounting|')}{'*' * 20}\n")
            logger.info(f"{'*' * 20}TestCase Ended {'|usb_3.1|USB mounting|'}{'*' * 20}\n")

        elif mount_point != f"{current_usb_name} is already mounted":
            print(mount_point)
            logger.info(mount_point)
            exec_command(f"mkdir {mount_point_loc}")
            exec_command(f"mount {mount_point}  {mount_point_loc}")
            usbname = mount_point_loc.split('/')[-1]

            try:
                mount_path = usb_df()[usbname]['Mounted']
                assert mount_path == mount_point_loc

            except AssertionError:
                error_msg = f"Not abel to mount the USB at specified mount point {mount_point_loc}"
                print(f"Not abel to mount the USB at specified mount point {mount_point_loc}")
                logger.error(f"Not abel to mount the USB at specified mount point {mount_point_loc}")
                print(red("FAIL"))
                logger.error("FAIL")
                return 'FAIL', error_msg

            except KeyError:
                print(red('USB NOT FOUND...!!'))
                logger.error('USB NOT FOUND...!!')

            else:
                print(f"Mount point given by user {green(mount_point_loc)}")
                logger.info(f"Mount point given by user {mount_point_loc}")
                print(f"USB mounted at {green(mount_path)}\n")
                logger.info(f"USB mounted at {mount_path}\n")
                print(green("PASS"))
                logger.info("PASS")
                return 'PASS', None

            finally:
                # again making mount point to default
                remount(mount_point)
                print(f"{'*'*20}TestCase Ended {blue('|usb_3.2|USB mounting|')}{'*'*20}\n")
                logger.info(f"{'*'*20}TestCase Ended {'|usb_3.2|USB mounting|'}{'*'*20}\n")
                close()
    else:
        print("USB Not Found")


usb_mount()
