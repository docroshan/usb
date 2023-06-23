from utilities.utility import *


@fun_count
def multiple_file_copy():
    print(f"{'*' * 20}TestCase started {blue('|usb_8.2|Multi File Copying|')}{'*' * 20}")
    logger.info(f"{'*' * 20}TestCase started {'|usb_8.2|Multi File Copying|'}{'*' * 20}")
    copy = copy_multi_file()
    test_files_names = " ". join([test_file_name1, test_file_name2])
    if copy != 0:
        output = run_command(f"cd {destination_path} && ls | find {test_files_names}")
        files = output.split('\n')[:-1]
        res = sorted(test_files_names.split())

        try:
            assert res == files

        except AssertionError:
            print(f"{red(test_files_names)} not able to copy to {destination_path}")
            error_msg = f"{test_files_names} not able to copy to {destination_path}"
            logger.error(f"{test_files_names} not able to copy to {destination_path}")
            print(f"{red('FAIL')}")
            logger.error('FAIL')
            return 'FAIL', error_msg

        else:
            print(f"{green(test_files_names)} files copied to {destination_path}")
            logger.info(f"{test_files_names} files copied to {destination_path}")
            print(f"{green(' '.join(files))} files are present in {destination_path} this location")
            logger.info(f"{' '.join(files)} files are present in {destination_path} this location")
            print(f"{green('PASS')}")
            logger.info('PASS')
            return 'PASS', None

        finally:
            sleep(0.5)
            print(f"Deleting Copied file {green(test_files_names)} in this destination {green(destination_path)}")
            logger.info(f"Deleting Copied file {test_files_names} in this destination {destination_path}")
            run_command(f"cd {destination_path} && rm {test_files_names}")
            print(f"{'*' * 20}TestCase ended {blue('|usb_8.2|Multi File Copy|')}{'*' * 20}\n")
            logger.info(f"{'*' * 20}TestCase ended {'|usb_8.2|Multi File Copy|'}{'*' * 20}\n")
            close()

    else:
        pass


multiple_file_copy()
