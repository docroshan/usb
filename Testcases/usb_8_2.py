from utilities.utility import *


def multiple_file_copy():

    print(f"{'*' * 20}TestCase started {blue('|usb_8.2|Multi File Copying|')}{'*' * 20}")
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
            print(f"{red('FAIL')}")

        else:
            print(f"{green(test_files_names)} files copied to {destination_path}")
            print(f"{green(' '.join(files))} files are present in {destination_path} this location")
            print(f"{green('PASS')}")

        finally:
            sleep(0.5)
            print(f"Deleting Copied file {green(test_files_names)} in this destination {green(destination_path)}")
            run_command(f"cd {destination_path} && rm {test_files_names}")
            print(f"{'*' * 20}TestCase ended {blue('|usb_8.2|Multi File Copy|')}{'*' * 20}\n")
            close()

    else:
        pass


# multiple_file_copy()
