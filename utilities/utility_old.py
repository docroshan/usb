from paramiko import *
from socket import *
import configparser
from collections import defaultdict
from simple_colors import *
from parser_creation import *
import os
import sys
import re
from time import sleep


config_file = get_attr('../config/config.ini', 'config_file')
user_name = get_attr(config_file, 'user_name')
password = get_attr(config_file, 'password')
usb_name = get_attr(config_file, 'usb_name')
ip = get_attr(config_file, 'ip')
test_file_name = get_attr(config_file, 'test_file_name')
server = get_attr(config_file, 'server')
mount_point = get_attr(config_file, 'mount_point')
port_ver = get_attr(config_file, 'port_ver')
source_path = get_attr(config_file, 'source_path')
destination_path = get_attr(config_file, 'destination_path')
file_type = get_attr(config_file, 'file_type')

parser = configparser.ConfigParser()
parser.read("config.ini")

data = defaultdict(str)

for i in parser.sections():
    for var, val in parser.items(i):
        data[var] += "".join(val)


def ssh_connect(server, user_name, password):
    ssh = SSHClient()
    # Adding auto policy for SSH connection
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect(server, username=user_name, password=password)

    except gaierror:
        print(red("Connection Error !!, connection to machine failed or timing issue.."))
    return ssh


def usb_df():                                                          # FOR RUNNING "df" COMMAND
    sleep(1)
    usb_details = defaultdict(dict)
    details = defaultdict(str)

    client = ssh_connect(data["ip"], data["user_name"], data["password"])

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
        return red("No USB Devices Found or Device not Mounted")

    return d


# vishwa
def dev_path():
    path = usb_df()
    if path == "USB NOT FOUND":
        return "USB NOT FOUND"
    else:
        temp = [i for i in path]
        return path[temp[0]]["Filesystem"]


# To rename the usb back to its original name
def usb_rename_to_original():
    super_access(password, f"mlabel -i {dev} ::{current_usb_name}")
    super_access(password, f"eject {dev}")
    super_access(password, f"eject -t {dev[:len(dev) - 1]}")
    print("\nUSB renamed to it's original name")


# To eject the USB
def usb_eject():
    super_access(password, f"eject {dev}")


# For copying a file
def copy_file(file_name=test_file_name):
    file_path = f"{source_path}{file_name}"
    print(file_path, source_path, destination_path)
    super_access(password, f"cp {file_path} {destination_path}")


# For deleting/removing a file
def remove_file(file = test_file_name):
    file_path = f"{source_path}{file}"
    super_access(password, f"rm {file_path}")


# For unmounting & format the usb
def quick_file_format():
    super_access(password, f'umount {dev}')
    result = super_access(password, f"mkfs.fat {dev}")
    return result


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


def exec_command(command):
    sleep(0.3)
    client = ssh_connect(data["ip"], data["user_name"], data["password"])
    _stdin, _stdout, _stderr = client.exec_command(f"echo {data['password']} | sudo -S {command}")
    return _stdout.read().decode() if _stdout else ""


def mlabel(dev_path, usbname):
    exec_command(f"mlabel -i {dev_path} ::{usbname}")
    exec_command(f"eject {dev_path}")
    exec_command(f"eject -t {dev_path[:-1]}")


def available_usb():
    usb_details = usb_df()
    print(f"Available USB's are:")
    for i in usb_details:
        print(i, end="|")
    print()


def mount():
    sleep(0.4)
    lst = exec_command("lsblk | grep sd")
    for points in lst.split("\n")[:-1]:
        if points.split()[0] not in ["sda", "├─sda1", "├─sda2", "└─sda3"]:
            if "part" in points.split():
                if len(points.split()) != 7:
                    return "/dev/"+(points.split()[0])[2:]
                else:
                    return "USB Mounted"


def unmount(path):
    exec_command(f"umount {path}")


def remount(path):
    exec_command(f"eject {path}")
    exec_command(f"eject -t {path[:-1]}")


def close():
    sleep(0.4)
    client = ssh_connect(data["ip"], data["user_name"], data["password"])
    client.close()


dev = devpath()
try:
    current_usb_name = super_access(password, f"mlabel -i {dev} -s").strip().split()[-1]
    create_config('USB', 'dev', dev, config_file)
    create_config('USB', 'current_usb_name', current_usb_name, config_file)
except AttributeError:
    print(yellow("Config file not updated with current usb details"))

