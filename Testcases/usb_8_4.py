from utilities.utility import *


@fun_count
def parallel_copy():
    print(f"{'*' * 20}TestCase started {blue('|usb_8.4|Parallel Copy|')}{'*' * 20}")
    logger.info(f"{'*' * 20}TestCase started {'|usb_8.4|Parallel Copy|'}{'*' * 20}")
    copy = copy_parallel()
    test_files_names = " ".join([test_file_name1, test_file_name2])
    destination_paths = " ".join([destination_path1+current_usb_name, destination_path2, destination_path3])

    if copy != 0:
        output = defaultdict(str)
        res = sorted(test_files_names.split())
        try:
            # Checking all location files copied
            for path in destination_paths.split():
                output[path] = " ".join((run_command(f"cd {path} && find {test_files_names}")).split('\n')[:-1])

        except TypeError:
            print("Multiple files need to be given in destination paths")

        else:
            # Verifying with user input
            for dst_path, files in output.items():
                if files != " ".join(res):
                    print(red(f"Failed in Copying to this destination location {dst_path}"))
                    error_msg = f"Failed in Copying to this destination location {dst_path}"
                    logger.error(f"Failed in Copying to this destination location {dst_path}")
                    print(f"{red('FAIL')}")
                    logger.error('FAIL')
                    return 'FAIL', error_msg
            else:
                print(f"{green(test_files_names)} copied to all destination locations {destination_paths.split()}")
                logger.info(f"{test_files_names} copied to all destination locations {destination_paths.split()}")
                print(f'{green("PASS")}')
                logger.info("PASS")
                return 'PASS', None

        finally:
            # removing all files in destination locations
            for dst_path, files in output.items():
                sleep(0.5)
                run_command(f"cd {dst_path} && rm {files}")
            print("\nDeleting all files copied to the location")
            logger.info("Deleting all files copied to the location")
            print(f"{'*' * 20}TestCase ended {blue('|usb_8.4|Parallel Copy|')}{'*' * 20}\n")
            logger.info(f"{'*' * 20}TestCase ended {'|usb_8.4|Parallel Copy|'}{'*' * 20}\n")

    else:
        print(f"{'*' * 20}TestCase started {blue('|usb_8.4|Parallel Copy|')}{'*' * 20}\n")
        logger.info(f"{'*' * 20}TestCase started {'|usb_8.4|Parallel Copy|'}{'*' * 20}\n")


parallel_copy()
