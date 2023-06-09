from utilities.usb import *


def find_file(path, file_name):
    file_path = f"{path}{file_name}"
    res = super_access(password, f"find {file_path}")
    if file_path == res:
        return True
    else:
        return False


@fun_count
def file_operation(file_name=filename, source=source_path, destination=destination_path):

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}\n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    file_path = f"{source}{file_name}"
    file_paths = []
    file_names = []
    _count = 0
    unknown = []

    # Checking single or multiple file
    if len(file_name.split()) > 1:
        # multi-file copy
        for name in file_name.split():          # collecting file names & paths
            if find_file(source, name):         # checking whether file is present in designated location or not
                file_paths.extend([f"{source}{name}"])
                file_names.append(name)
                _count += 1
            else:
                unknown.append(name)
                print(green(name), red(f"FILE Not Found in:"), yellow(source), '\n')
                logger.error(f"{name} FILE Not Found in: {source}")

        super_access(password, f"cp -p {' '.join(file_paths)} {destination}")

        print(green(', '.join(file_names)), "Files Copied To:", green(destination), '\n')
        logger.info(f"{', '.join(file_names)} Files Copied To: {destination}")

    else:
        # single file copy
        if find_file(source, file_name.split()[0]):
            super_access(password, f"cp {file_path} {destination}")

            print(green(file_name.split()[0]), "File Copied To:", green(destination), '\n')
            logger.info(f"{file_name.split()[0]} File Copied To: {destination}")
            _count += 1
        else:
            print(green(file_name), red(f"FILE Not Found in:"), yellow(source), '\n')
            logger.error(f"{file_name} FILE Not Found in: {source}")
            unknown.append(file_name)

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    if len(file_name.split()) == _count:
        return 'PASS', None
    else:
        return 'FAIL', f"File Not Found {' '.join(unknown)} or Unable to copy file"


# file_operation('test5', '/home/demo/Test_repo/', '/home/demo/Test_destination/')
