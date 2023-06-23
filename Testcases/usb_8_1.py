from utilities.utility import *


@fun_count
def single_file_copy():
    print(f"{'*' * 20}TestCase started {blue('|usb_8.1|Single File Copying|')}{'*' * 20}")
    logger.info(f"{'*' * 20}TestCase started {'|usb_8.1|Single File Copying|'}{'*' * 20}")
    copy = copy_file()
    if copy != 0:
        output = run_command(f"cd {destination_path} && ls | grep -w {test_file_name}")
        file_name = output.strip("\n")

        try:
            assert file_name == test_file_name

        except AssertionError:
            print(f"{red(destination_path)} not able to copy to {test_file_name}")
            error_msg = f"{destination_path} not able to copy to {test_file_name}"
            logger.error(f"{destination_path} not able to copy to {test_file_name}")
            print(f"{red('FAIL')}")
            logger.error('FAIL')
            return 'FAIL', error_msg

        else:
            print(f"{green(test_file_name)} copied to {green(destination_path)}")
            logger.info(f"{test_file_name} copied to {destination_path}")
            print(f"{green(file_name)} present in {green(destination_path)} this location")
            logger.info(f"{file_name} present in {destination_path} this location")
            print(f"{green('PASS')}")
            logger.info('PASS')
            return 'PASS', None

        finally:
            sleep(0.5)
            print(f"Deleting Copied file {green(destination_path)} in this destination {green(test_file_name)}")
            logger.info(f"Deleting Copied file {destination_path} in this destination {test_file_name}")
            run_command(f"cd {destination_path} && rm {test_file_name}")
            print(f"{'*' * 20}TestCase ended {blue('|usb_8.1|Single File Copy|')}{'*' * 20}\n")
            logger.info(f"{'*' * 20}TestCase ended {'|usb_8.1|Single File Copy|'}{'*' * 20}\n")
            close()

    else:
        pass


single_file_copy()
