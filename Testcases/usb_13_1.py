from utilities.utility import *


def bootable_usb():
    print(f"{'*'*20}TestCase started {blue('usb_13.1')}{'*'*20}")
    path = devpath()
    exec_command(f"umount {dev}")
    print(f"Installing IOS image in {dev} path")
    ssh = ssh_connect(ip, user_name, password)
    stdout, stdin, stderr = ssh.exec_command(f"echo {password} | sudo -S dd if={iso_image} of={dev[:-1]} bs=1M status=progress")
    print(stderr.read().decode())
    sleep(40)
    exec_command(f"eject {path}")
    exec_command(f"eject -t {path[:-1]}")
    sleep(2)
    print("usb reconnectd")
    formatting_bootable_usb()
    exec_command(f"mkfs.fat {path}")
    exec_command(f"eject {path}")
    exec_command(f"eject -t {path[:-1]}")
    usb_rename_to_original()
    print(f"{'*'*20}TestCase ended {blue('usb_13.1')}{'*'*20}\n")


# bootable_usb()
