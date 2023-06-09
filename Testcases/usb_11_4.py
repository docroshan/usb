from utilities.utility import *


def reboot_during_copy():
    print(f"{'*' * 20}TestCase started {blue('|usb_11.4|Reboot Copy|')}{'*' * 20}")
    power_event("sudo reboot\n")
    print("Rebooted...!")
    usb_loc = usb_df()[current_usb_name]["Mounted"]
    source_loc_file_size = run_command(f"cd {source_path} && ls -lh | grep -w {test_file_name}")
    dst_loc_file_size = run_command(f"cd {usb_loc} && ls -lh |grep -w {test_file_name}")
    print("Test File Name:", source_loc_file_size.split()[-1], "File Size:", source_loc_file_size.split()[4])
    print("Test File Name:", dst_loc_file_size.split()[-1], "File Size:", dst_loc_file_size.split()[4])

    if dst_loc_file_size != str():
        dst_loc_file_size = dst_loc_file_size.split()[4]
    try:
        assert source_loc_file_size.split()[4] != dst_loc_file_size

    except AssertionError:
        print(f"{red(test_file_name)} file copy process able to resume after reboot")
        print(red("Fail"))

    else:
        print(f"{green(test_file_name)} file copy process not able to resume after reboot")
        print(green("PASS"))

    finally:
        exec_command(f"rm {usb_loc+'/'+test_file_name}")
        close()
        print(f"{'*' * 20}TestCase ended {blue('|usb_11.4|Reboot Copy|')}{'*' * 20}\n")


# reboot_during_copy()
