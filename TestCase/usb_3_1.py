from utilities.usb import *


def usb_mount():
    sleep(0.4)
    print(f"{'*'*20}TestCase started {blue('|usb_3.1|USB mounting|')}{'*'*20}")
    mount_point = mount(data["current_usb_name"])
    if mount_point is not None:
        if mount_point == f"{data['current_usb_name']} is already mounted":
            print(mount_point)
            print(green("PASS"))
            print(f"{'*' * 20}TestCase Ended {blue('|usb_3.1|USB mounting|')}{'*' * 20}\n")
        elif mount_point != f"{data['current_usb_name']} is already mounted":
            print(mount_point)
            exec_command(f"mkdir {data['mount_point_loc']}")
            exec_command(f"mount {mount_point}  {data['mount_point_loc']}")
            usbname = data['mount_point_loc'].split('/')[-1]
            mount_path = usb_df()[usbname]['Mounted']

            try:
                assert mount_path == data['mount_point_loc']

            except AssertionError:
                print(red("FAIL"))

            else:
                print(f"Mount point given bye user {green(data['mount_point_loc'])}")
                print(f"USB mounted at {green(mount_path)}\n")
                print(green("PASS"))

            finally:
                # again making mount point to default
                remount(mount_point)
                print(f"{'*'*20}TestCase Ended {blue('|usb_3.1|USB mounting|')}{'*'*20}\n")
                close()
    else:
        print("USB Not Found")


# usb_mount()
