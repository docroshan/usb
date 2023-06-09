from utilities.utility import *


def folder_copy():
    print(f"{'*' * 20}TestCase started {blue('|usb_8.3|Folder Copy|')}{'*' * 20}")
    copy = copy_folder()
    if copy != 0:
        output = run_command(f"cd {destination_path} && find {test_folder_name}")
        folder_name = (output.strip('\n')).split()[0]

        try:
            assert test_folder_name == folder_name

        except AssertionError:
            print(f"{red(test_folder_name)} not able to copy to {destination_path}")
            print(f"{red('FAIL')}")

        else:
            print(f"{green(test_folder_name)} folder copied to {destination_path}")
            print(f"{green(folder_name)} folder are present in {destination_path} this location")
            print(f"{green('PASS')}")

        finally:
            sleep(0.5)
            print(f"Deleting Copied folder {test_folder_name} in this destination {destination_path}")
            run_command(f"cd {destination_path} && echo {password} | sudo -S rm -rf {test_folder_name}")
            print(f"{'*' * 20}TestCase ended {blue('|usb_8.3|Folder Copy|')}{'*' * 20}\n")
            close()

    else:
        pass


# folder_copy()
