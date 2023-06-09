from utilities.usb import *


@fun_count
def delete_file(name, path):

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20} \n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    res = remove_file(name, path)

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    if res[-1]:
        return 'PASS', None
    else:
        return 'FAIL', res[0]


# delete_file('test1', '/home/demo/Test_destination/')
