from paramiko import *
from socket import *
from collections import defaultdict
from simple_colors import *
from utilities.parser_creation import *
import os
import sys
import re
from time import sleep
import logging

# user_data_file = read_config('./config/test_user_config.ini')
# user_config_file = d['user_config_file']
# user_name = d['user_name']
# password = d['password']
# ip = d['ip']
# server = d['server']

# User inputs
user_config_file = get_attr('./config/test_user_config.ini', 'user_config_file')
# SSH/Login Details
user_name = get_attr(user_config_file, 'user_name')
password = get_attr(user_config_file, 'password')
ip = get_attr(user_config_file, 'ip')
server = get_attr(user_config_file, 'server')

# Developer inputs
dev_config_file = get_attr('./config/dev_config.ini', 'dev_config_file')
# USB Details
usb_name = get_attr(dev_config_file, 'usb_name')
file_type = get_attr(dev_config_file, 'file_type')
port_ver = get_attr(dev_config_file, 'port_ver')
total_storage = get_attr(dev_config_file, 'total_storage')
available_storage = get_attr(dev_config_file, 'available_storage')
current_usb_name = get_attr(dev_config_file, "current_usb_name")

# File\Image Paths
source_path = get_attr(dev_config_file, 'source_path')
iso_image = get_attr(dev_config_file, 'iso_image')

test_file_path = get_attr(dev_config_file, 'test_file_path')
destination_path = get_attr(dev_config_file, 'destination_path')
destination_path1 = get_attr(dev_config_file, 'destination_path1')
destination_path2 = get_attr(dev_config_file, 'destination_path2')
destination_path3 = get_attr(dev_config_file, 'destination_path3')

# Test Files
filename = get_attr(dev_config_file, 'filename')
test_file_name = get_attr(dev_config_file, 'test_file_name')
test_file_name1 = get_attr(dev_config_file, 'test_file_name1')
test_file_name2 = get_attr(dev_config_file, 'test_file_name2')

# Folder Paths
test_folder_name = get_attr(dev_config_file, 'test_folder_name')

# Mounting\Partition Details
mount_point = get_attr(dev_config_file, 'mount_point')
mount_point_loc = get_attr(dev_config_file, 'mount_point_loc')
partitions_number = get_attr(dev_config_file, 'partitions_number')
partition_size = get_attr(dev_config_file, 'partition_size')


def ssh_connect(ip, user_name, password):
    ssh = SSHClient()
    # Adding auto policy for SSH connection
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect(ip, username=user_name, password=password)

    except gaierror:
        logging.error("Connection Error !!, connection to machine failed or timing issue..")
    return ssh


def exec_command(command):
    sleep(0.3)
    client = ssh_connect(ip, user_name, password)
    _stdin, _stdout, _stderr = client.exec_command(f"echo {password} | sudo -S {command}")
    return _stdout.read().decode() if _stdout else ""


def run_command(x):
    client = ssh_connect(ip, user_name, password)
    _stdin, _stdout, _stderr = client.exec_command(x)
    return _stdout.read().decode() if _stdout else ""


def usb_df():                                                          # FOR RUNNING "df" COMMAND
    sleep(1)
    usb_details = defaultdict(dict)
    details = defaultdict(str)

    client = ssh_connect(ip, user_name, password)

    # running commands
    _stdin, _stdout, _stderr = client.exec_command("df -h | grep Mounted")
    label = _stdout.read().decode().strip('\n').split()

    _stdin, _stdout, _stderr = client.exec_command("df -h | grep media")
    usb_list = _stdout.read().decode().strip('\n').split('\n')

    try:
        for line in usb_list:
            temp = line.split()
            details[label[0]] = temp[0]
            details[label[1]] = temp[1]
            details[label[2]] = temp[2]
            details[label[3]] = temp[3]
            details[label[5]] = temp[5]
            usb_details[(temp[5]).split('/')[-1]] = dict(details)

    except IndexError:
        return "USB NOT FOUND"

    else:
        return dict(usb_details)


# Can be used to run any commands which needs "SUDO" user to execute
def super_access(password, command):
    sleep(0.5)
    ssh = ssh_connect(ip, user_name, password)
    stdin, stdout, stderr = ssh.exec_command(f'echo {password} | sudo -S {command}')
    res = stdout.read().decode().strip('\n')
    if res != '':
        return res
    else:
        pass


# returns dev path(Roshan)
def devpath():
    sleep(1)
    ssh = ssh_connect(ip, user_name, password)
    try:
        stdin, stdout, stderr = ssh.exec_command('df | grep media')
        d = stdout.read().decode().strip('\n').split()[0]

    except:
        logging.error("No USB Devices Found or Device not Mounted")
        return red("No USB Devices Found or Device not Mounted")

    return d


# vishwa
def dev_path(devicename):
    path = usb_df()
    if path == "USB NOT FOUND":
        return "USB NOT FOUND"
    else:
        return path[devicename]['Filesystem']


# To rename the usb back to its original name
def usb_rename_to_original():
    sleep(1)
    super_access(password, f"mlabel -i {dev} ::{current_usb_name}")
    usb_eject()
    usb_reconnect()
    logging.info("USB renamed to it's original name")


# To eject the USB
def usb_eject():
    try:
        d = super_access(password, f"mlabel -i {dev} -s").strip().split()[-1]
        if d:
            super_access(password, f"eject {dev}")
            logging.info('USB Ejected !!')
            print(green("USB Ejected !!"))
    except AttributeError:
        print(red('NO USB FOUND : unable to Eject'))
        logging.error('NO USB FOUND : unable to Eject')


# To eject the USB
def usb_reconnect():
    super_access(password, f"eject -t {dev[:len(dev) - 1]}")
    logging.info('USB Reconnected !!')
    print(green('USB Re-Connected !!'))


# To Safely eject the USB
def usb_safe_eject():
    unmount(dev)
    usb_eject()
    logging.info("USB Safely Ejected")


# For copying a file
def copy_file(file_name=test_file_name):
    file_path = f"{source_path}{file_name}"
    print(f"Source File Path: {source_path}\nDestination File Path: {destination_path}\n")
    output = run_command(f"cd {source_path} && find {file_name}")
    if output.strip('\n') == file_name:
        super_access(password, f"cp {file_path} {destination_path}")
    else:
        print(f"{red(f'In this {source_path} destination {file_name} Not Found!!')}")
        return 0


def copy_multi_file(file_name=(test_file_name1, test_file_name2)):
    test_files_names = " ".join(file_name)
    print(f"Source File Path: {source_path}\nDestination File Path: {destination_path}\n")
    output = run_command(f"cd {source_path} && find {test_files_names}")
    files = output.split('\n')[:-1]
    res = sorted(test_files_names.split())
    if files == res:
        run_command(f"cd {source_path} && echo {password} | sudo -S cp {test_files_names} {destination_path}")
    else:
        print(f"{red(f'In this {source_path} destination {file_name} Not Found!!')}")
        return 0


def copy_folder(folder_name=test_folder_name):
    file_path = f"{source_path}{folder_name}/"
    print(f"Source File Path: {source_path}\nDestination File Path: {destination_path}\n")
    output = run_command(f"cd {source_path} && find {folder_name}")
    if test_folder_name == (output.strip('\n')).split()[0]:
        super_access(password, f"cp -r {file_path} {destination_path}")
    else:
        print(f"{red(f'In this {source_path} destination {test_folder_name} folder Not Found!!')}")
        return 0


def copy_parallel(file_name=(test_file_name1, test_file_name2)):
    test_files_names = " ".join(file_name)
    destination_path_1 = destination_path1 + current_usb_name

    destination_paths = " ".join([destination_path_1, destination_path2, destination_path3])
    output = run_command(f"cd {source_path} && ls | find {test_files_names}")
    res = " ".join(sorted(output.split('\n')[:-1]))

    if res == test_files_names:
        run_command(f"cd {source_path} && parallel cp {test_files_names} ::: {destination_paths}")
    else:
        print(f"{red(f'In this {source_path} destination {test_files_names} Not Found!!')}")
        return 0


def power_event(opr, file_name=test_file_name):
    usb_loc = usb_df()[current_usb_name]["Mounted"]
    ssh = ssh_connect(ip, user_name, password)
    channel_ = ssh.invoke_shell()
    sleep(1)
    channel_.send(f"echo {password} | sudo -S killall -9 /dev/rtc0\n")
    sleep(1)
    channel_.send(f"cp {source_path+file_name} {usb_loc} &\n")
    sleep(2)
    print("Shutting Down Linux Machine.........................")
    channel_.send(opr)
    channel_.send(f"{password}\n")
    sleep(1)
    print(channel_.recv(40960).decode())
    sleep(300)
    print("Powered ON Successfully...")


def copy_sleep():
    usb_loc = usb_df()[current_usb_name]["Mounted"]
    ssh = ssh_connect(ip, user_name, password)
    channel_ = ssh.invoke_shell()
    sleep(1)
    channel_.send(f"echo {password} | sudo -S killall -9 /dev/rtc0\n")
    sleep(1)
    channel_.send(f"cp {source_path+test_file_name} {usb_loc} &\n")
    sleep(2)
    channel_.send("sleep 60\n")
    print("Under sleep for 60 seconds...")
    sleep(60)
    print("background process of copy resumed")
    channel_.send("fg\n")
    sleep(10)
    print(channel_.recv(40960).decode())


def copy_hibernate(file_name=test_file_name):
    usb_loc = usb_df()[current_usb_name]["Mounted"]
    ssh = ssh_connect(ip, user_name, password)
    channel_1 = ssh.invoke_shell()
    sleep(1)
    channel_1.send(f"echo {password} | sudo -S killall -9 /dev/rtc0\n")
    sleep(1)
    channel_1.send(f"cp {source_path + file_name} {usb_loc} &\n")
    sleep(1)
    print("Power Saver Mode ON.....")
    channel_1.send(f"echo {password} | sudo -S rtcwake -s 60 -m mem\n")
    sleep(2)
    print(channel_1.recv(40960).decode())
    sleep(60)
    print("Powered ON...")
    # sleep(200)


# For deleting/removing a file
def remove_file(file_name, path):
    from TestCase.usb_7_0 import find_file

    file_paths = []
    if find_file(path, file_name):
        for name in file_name.split():
            file_paths.extend([f"{path}{name}"])
        super_access(password, f"rm {' '.join(file_paths)}")
        print(green(file_name), "File Deleted From:", green(' '.join(file_paths)), '\n')
        logging.info(f"{file_name} File Deleted From: {' '.join(file_paths)}")
    else:
        print(red(f"File NOT FOUND in {' '.join(file_paths)}\n"))
        logging.error(f"File NOT FOUND in {' '.join(file_paths)}")


def fat_file_format():
    unmount(dev)
    super_access(password, f"mkfs.fat {dev}")
    logging.info('USB Formatted')
    usb_eject()
    usb_reconnect()


# To unmount & format the usb
def quick_file_format():
    fat_file_format()
    usb_rename_to_original()


def ntfs_file_format():
    unmount(dev)
    super_access(password, f"mkfs.ntfs {dev}")
    logging.info('USB Formatted')
    usb_eject()
    usb_reconnect()


def exfat_file_format():
    unmount(dev)
    super_access(password, f"mkfs.exfat {dev}")
    logging.info('USB Formatted')
    usb_eject()
    usb_reconnect()


def formatting_bootable_usb():
    boot_point = (devpath().split('/')[-1])[:-1]
    ssh = ssh_connect(ip, user_name, password)
    stdout, stdin, stderr = ssh.exec_command(f"lsblk | grep {boot_point}")
    partitions = stdin.read().decode()
    partiton_num = len(partitions.split('\n')[:-1])
    path = devpath()
    print(path)

    terminal = ssh.invoke_shell()
    sleep(1)
    terminal.send(f"sudo umount {path}\n")
    sleep(1)
    terminal.send(f"{password}\n")
    sleep(1)
    terminal.send(f"sudo fdisk {path[:-1]}\n")
    sleep(1)

    # deleting all partitions
    for i in range(1, partiton_num):
        if partiton_num-1 == i:
            terminal.send("d\n")
            break
        else:
            terminal.send("d\n")
            sleep(1)
            print(f"deleted {i}")
            terminal.send(f"{i}\n")
            sleep(1)

    terminal.send("n\n")
    sleep(1)
    terminal.send("1\n")
    sleep(1)
    terminal.send("2048\n")
    sleep(1)
    terminal.send("\n")
    sleep(1)
    terminal.send("w\n")
    sleep(1)

    print(terminal.recv(1609560).decode())


# Returns mount points
def mount_points():
    sleep(1)
    ssh = ssh_connect(ip, user_name, password)
    d = []
    stdin, stdout, stderr = ssh.exec_command('df | grep media')
    df = stdout.read().decode().strip('\n').split('\n')

    for i in df:
        d += [i.split('% ')[-1]]

    if d == '':
        return red("No USB drives found !!")
    else:
        return d


def mlabel(dev_path, usbname):
    exec_command(f"mlabel -i {dev_path} ::{usbname}")
    logging.info('USB Renamed........')


def available_usb():
    usb_details = usb_df()
    logging.info(f"Available USB's are:")
    for i in usb_details:
        print(i, end="|")
    print()


def mount(devicename):
    sleep(0.4)
    lst = exec_command("lsblk | grep sd")
    for points in lst.split("\n")[:-1]:
        if points.split()[0] not in ["sda", "├─sda1", "├─sda2", "└─sda3"]:
            if "part" in points.split():
                if len(points.split()) == 7 and devicename == (points.split()[-1].split('/'))[-1]:
                    return f"{green(devicename)} is already mounted"
                else:
                    if len(points.split()) != 7:
                        return "/dev/"+(points.split()[0])[2:]


def unmount(path):
    exec_command(f"umount {path}")
    logging.info('USB Unmounted')


def remount(path):
    exec_command(f"eject {path}")
    exec_command(f"eject -t {path[:-1]}")


def close():
    sleep(0.4)
    client = ssh_connect(ip, user_name, password)
    client.close()


logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

dev = devpath()
try:
    current_usb_name = super_access(password, f"mlabel -i {dev} -s").strip().split()[-1]
    create_config('USB_CURRENT_DATA', 'dev', dev, dev_config_file)
    create_config('USB_CURRENT_DATA', 'current_usb_name', current_usb_name, dev_config_file)
    logging.info('')
except AttributeError:
    logging.error("Config file not updated with current usb details")
