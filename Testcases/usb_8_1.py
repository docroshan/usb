from utilities.utility import *


def single_file_copy():
    print(f"{'*' * 20}TestCase started {blue('|usb_8.1|Single File Copying|')}{'*' * 20}")
    copy = copy_file()
    if copy != 0:
        output = run_command(f"cd {destination_path} && ls | grep -w {test_file_name}")
        file_name = output.strip("\n")

        try:
            assert file_name == test_file_name

        except AssertionError:
            print(f"{red(destination_path)} not able to copy to {test_file_name}")
            print(f"{red('FAIL')}")

        else:
            print(f"{green(test_file_name)} copied to {green(destination_path)}")
            print(f"{green(file_name)} present in {green(destination_path)} this location")
            print(f"{green('PASS')}")

        finally:
            sleep(0.5)
            print(f"Deleting Copied file {green(destination_path)} in this destination {green(test_file_name)}")
            run_command(f"cd {destination_path} && rm {test_file_name}")
            print(f"{'*' * 20}TestCase ended {blue('|usb_8.1|Single File Copy|')}{'*' * 20}\n")
            close()

    else:
        pass


# single_file_copy()
