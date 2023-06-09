from utilities.usb import *
from paramiko import *
from socket import *
from collections import defaultdict
from simple_colors import *
from utilities.parser_creation import *
import os
import sys
import re
import time
import subprocess
from time import sleep
import logging
from utilities.reports import *


# User inputs
user_config_file = get_attr('./user_data/user_config.ini', 'user_config_file')

# SSH/Login Details
user_name = get_attr(user_config_file, 'user_name')
password = get_attr(user_config_file, 'password')
ip = get_attr(user_config_file, 'ip')
server = get_attr(user_config_file, 'server')

# Developer inputs
dev_config_file = get_attr('./dev_data/dev_config.ini', 'dev_config_file')

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


test_case = get_attr(user_config_file, 'pick_test')


def ssh_connect(ip, user_name, password):
    # Adding auto policy for SSH connection
    ssh = SSHClient()
    try:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(ip, username=user_name, password=password)

    except TimeoutError:
        print(red("Connection Error or Connection Timed Out"))
        logger.error("Connection Error or Connection Timed Out")
        return 0

    except:
        print('Connection ERROR: Failed to connect the machine!!')
        logger.error('Connection ERROR: Failed to connect the machine!!')
        return 0
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

    try:
        # running commands
        _stdin, _stdout, _stderr = client.exec_command("df -h | grep Mounted")
        label = _stdout.read().decode().strip('\n').split()

        _stdin, _stdout, _stderr = client.exec_command("df -h | grep media")
        usb_list = _stdout.read().decode().strip('\n').split('\n')

        for line in usb_list:
            temp = line.split()
            details[label[0]] = temp[0]
            details[label[1]] = temp[1]
            details[label[2]] = temp[2]
            details[label[3]] = temp[3]
            details[label[5]] = temp[5]
            usb_details[(temp[5]).split('/')[-1]] = dict(details)

    except AttributeError:
        print("Connection Timeout")
        logger.info("Connection Time out")

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
        logger.error("No USB Devices Found or Device not Mounted")
        return 0, "No USB Devices Found or Device not Mounted"

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
    print(green("USB renamed to it's original name"))
    logger.info("USB renamed to it's original name")


# To eject the USB
def usb_eject():
    try:
        d = super_access(password, f"mlabel -i {dev} -s").strip().split()[-1]
        if d:
            super_access(password, f"eject {dev}")
            logger.info('USB Ejected !!')
            print(green("USB Ejected !!"))
            return 1
    except AttributeError:
        print(red('NO USB FOUND : unable to Eject'))
        logger.error('NO USB FOUND : unable to Eject')
        return 0


# To eject the USB
def usb_reconnect():
    super_access(password, f"eject -t {dev[:len(dev) - 1]}")
    d = super_access(password, f"df | grep {dev}")
    if d:
        logger.info('USB Reconnected !!')
        print(green('USB Re-Connected !!'))
        return 1
    else:
        print(red("No USB Found !!"))
        logger.error('No USB FOUND !!')
        return 0


# To Safely eject the USB
def usb_safe_eject():
    d = super_access(password, f"df | grep {dev}")
    if d:
        unmount(dev)
        super_access(password, f"eject {dev}")
        logger.info('USB Safely Ejected !!')
        print(green("USB Safely Ejected !!"))
        return 1
    else:
        print(red("No USB Found or Unable to Eject!!"))
        logger.error('No USB FOUND or Unable to Eject!!')
        return 0


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
        logger.error(f"In this {source_path} destination {test_folder_name} folder Not Found!!")
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
        logger.error(f"In this {source_path} destination {test_files_names} Not Found!!")
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
    logger.info("Shutting Down Linux Machine.........................")
    channel_.send(opr)
    channel_.send(f"{password}\n")
    sleep(1)
    logger.info(channel_.recv(40960).decode())
    sleep(300)
    print("Powered ON Successfully...")
    logger.info("Powered ON Successfully...")


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
    logger.info("Under sleep for 60 seconds...")
    sleep(60)
    print("background process of copy resumed")
    logger.info("background process of copy resumed")
    channel_.send("fg\n")
    sleep(10)
    # print(channel_.recv(40960).decode())
    logger.info(channel_.recv(40960).decode())


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
    logger.info("Power Saver Mode ON.....")
    channel_1.send(f"echo {password} | sudo -S rtcwake -s 60 -m mem\n")
    sleep(2)
    logger.info(channel_1.recv(40960).decode())
    sleep(60)
    print("Powered ON...")
    logger.info("Powered ON...")
    sleep(70)


# For deleting/removing a file
def remove_file(file_name, path):
    from Testcases.usb_7_1 import find_file

    _count = 0
    unknown = []
    for name in file_name.split():
        if find_file(path, name):
            super_access(password, f"rm {path}{name}")
            print(green(name), "File Deleted From:", green(path), '\n')
            logger.info(f"{name} File Deleted From: {path}")
            _count += 1

        else:
            print(red(f"{name} File NOT FOUND in {path}"))
            logger.error(f"{name} File NOT FOUND in {path}")
            unknown.append(name)

    if len(file_name.split()) == _count:
        return 'File Deleted', 1
    else:
        return f"File Not Found: {' '.join(unknown)}", 0


# def fat_file_format():
#     unmount(dev)
#     super_access(password, f"mkfs.fat {dev}")
#     if current_usb_name == super_access(password, f"mlabel -i {dev} -s").strip('\n').split()[-1]:
#         logger.info('USB Formatted')
#         print(green('USB Formatted'))
#         usb_eject()
#         usb_reconnect()
#     else:
#         logger.error('USB Not Formatted')
#         print(red('USB Not Formatted !!'))


def fat_file_format():
    unmount(dev)
    super_access(password, f"mkfs.fat {dev}")
    logger.info('USB Formatted')
    print(green('USB Formatted'))
    usb_eject()
    usb_reconnect()


# To unmount & format the usb
def quick_file_format():
    fat_file_format()
    usb_rename_to_original()


def ntfs_file_format():
    unmount(dev)
    super_access(password, f"mkfs.ntfs {dev}")
    logger.info('USB Formatted')
    usb_eject()
    usb_reconnect()


def exfat_file_format():
    unmount(dev)
    super_access(password, f"mkfs.exfat {dev}")
    logger.info('USB Formatted')
    usb_eject()
    usb_reconnect()


def formatting_bootable_usb():
    boot_point = (devpath().split('/')[-1])[:-1]
    ssh = ssh_connect(ip, user_name, password)
    stdout, stdin, stderr = ssh.exec_command(f"lsblk | grep {boot_point}")
    partitions = stdin.read().decode()
    partiton_num = len(partitions.split('\n')[:-1])
    path = devpath()
    # print(path)

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
            logger.info(f"deleted {i}")
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

    logger.info(terminal.recv(1609560).decode())


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
    logger.info('USB Renamed........')


def available_usb():
    usb_details = usb_df()
    print(f"Available USB's are:")
    for i in usb_details:
        print(i, end="|")
        # logger.info(i)
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
    logger.info('USB Unmounted')
    print(green('USB Unmounted'))


def remount(path):
    exec_command(f"eject {path}")
    exec_command(f"eject -t {path[:-1]}")


def close():
    sleep(0.4)
    client = ssh_connect(ip, user_name, password)
    client.close()


count = 0
csv_data = defaultdict(list)


def pass_fail():
    _fail = 0
    _pass = 0
    for testcase, num in csv_data.items():
        if num[1].upper() == 'FAIL':
            _fail += 1
        else:
            _pass += 1

    with open(f'./results/{test_case}.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('Total number of TestCases', len(csv_data)))
        writer.writerow(['Total Pass TestCases', _pass])
        writer.writerow(['Total Fail TestCases', _fail])


def fun_count(func):
    def wrapper(*args, **kwargs):
        global count
        count += 1
        res = func(*args, **kwargs)  # (Pass, None)or(Fail, Reason/Remarks)
        csv_data[func.__name__] += [count, res[0], res[1]]

        with open(f'./{test_case}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Testcase No.', 'Testcase Name', 'Status', 'Remarks'])
            for func_name, num in csv_data.items():
                writer.writerow([num[0], func_name.upper(), num[1], num[-1]])
        pass_fail()
        html_reports()
        return func
    return wrapper


logging.basicConfig(filename=f'./results/{test_case}.log', format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

dev = devpath()
if dev[0]:
    try:
        current_usb_name = super_access(password, f"mlabel -i {dev} -s").strip().split()[-1]
        create_config('USB_CURRENT_DATA', 'dev', dev, dev_config_file)
        create_config('USB_CURRENT_DATA', 'current_usb_name', current_usb_name, dev_config_file)

    except AttributeError:
        logger.critical("Config file not updated with current usb details\n")
        print(red("Config file not updated with current usb details\n"))
else:
    print(red(dev[1]))
    logger.error(dev[1])
    logger.critical("Config file not updated with current usb details\n")
    print(red("Config file not updated with current usb details\n"))
