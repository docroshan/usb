from utilities.usb import *


def find_file(path, file_name):
    file_path = f"{path}{file_name}"
    res = super_access(password, f"find {file_path}")
    if file_path == res:
        return True
    else:
        return False


def file_ops(file_name=filename, source=source_path, destination=destination_path):

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    file_path = f"{source}{file_name}"
    file_paths = []
    file_names = []

    if len(file_name.split()) > 1:
        for name in file_name.split():
            if find_file(source, name):
                file_paths.extend([f"{source}{name}"])
                file_names.append(name)
            else:
                print(green(name), red(f"FILE Not Found in:"), yellow(source), '\n')
                logging.error(f"{name} FILE Not Found in: {source}")

        super_access(password, f"cp -p {' '.join(file_paths)} {destination}")

        print(green(', '.join(file_names)), "Files Copied To:", green(destination), '\n')
        logging.info(f"{', '.join(file_names)} Files Copied To: {destination}")

    else:
        if find_file(source, file_name.split()[0]):
            super_access(password, f"cp {file_path} {destination}")

            print(green(file_name.split()[0]), "File Copied To:", green(destination), '\n')
            logging.info(f"{file_name.split()[0]} File Copied To: {destination}")

        else:
            print(green(file_name), red(f"FILE Not Found in:"), yellow(source), '\n')
            logging.error(f"{file_name} FILE Not Found in: {source}")

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")
