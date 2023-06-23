from utilities.utility import *


@fun_count
def sleep_during_copy():
    print(f"{'*' * 20}TestCase started {blue('|usb_11.1|Sleep During Copy|')}{'*' * 20}")
    logger.info(f"{'*' * 20}TestCase started {'|usb_11.1|Sleep During Copy|'}{'*' * 20}")
    usb_reconnect()
    copy_sleep()
    usb_loc = usb_df()[current_usb_name]["Mounted"]
    source_loc_file_size = run_command(f"cd {source_path} && ls -lh | grep -w {test_file_name}")
    dst_loc_file_size = run_command(f"cd {usb_loc} && ls -lh |grep -w {test_file_name}")
    print("Test File Name:", source_loc_file_size.split()[-1], "File Size:", source_loc_file_size.split()[4])
    logger.info(f"Test File Name:{source_loc_file_size.split()[-1]}, File Size: {source_loc_file_size.split()[4]}")
    print("Test File Name:", dst_loc_file_size.split()[-1], "File Size:", dst_loc_file_size.split()[4])
    logger.info(f"Test File Name:{dst_loc_file_size.split()[-1]}, File Size: {dst_loc_file_size.split()[4]}")

    if dst_loc_file_size != str():
        dst_loc_file_size = dst_loc_file_size.split()[4]
    try:
        assert source_loc_file_size.split()[4] == dst_loc_file_size

    except AssertionError:
        print(f"{red(test_file_name)} file copy process not able to resume after sleep")
        error_msg = f"{test_file_name} file copy process not able to resume after sleep"
        logger.error(f"{red(test_file_name)} file copy process not able to resume after sleep")
        print(red("Fail"))
        logger.error("Fail")
        return 'FAIL', error_msg

    else:
        print(f"{green(test_file_name)} file copy process able to resume after sleep")
        logger.info(f"{test_file_name} file copy process able to resume after sleep")
        print(green("PASS"))
        logger.info("PASS")
        return 'PASS', None

    finally:
        exec_command(f"rm {usb_loc+'/'+test_file_name}")
        print(f"{usb_loc+'/'+test_file_name} file removed")
        logger.info(f"{usb_loc+'/'+test_file_name} file removed")
        close()
        print(f"{'*' * 20}TestCase ended {blue('|usb_11.1|Sleep During Copy|')}{'*' * 20}\n")
        logger.info(f"{'*' * 20}TestCase ended {'|usb_11.1|Sleep During Copy|'}{'*' * 20}\n")


sleep_during_copy()
