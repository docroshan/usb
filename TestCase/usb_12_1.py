from utilities.usb import *


# To print partition details
def print_partition(channel):
    channel.send('p\n')
    sleep(1)


def delete_partition(channel):
    channel.send('d\n')
    sleep(1)


def new_partition(channel):
    channel.send('n\n')
    sleep(1)


def merge_partition():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    stdout = super_access(password, f"lsblk | grep {(dev[:len(dev) - 1]).split('/')[-1]}")
    stale, *ans = stdout.strip().split('\n')

    ssh = ssh_connect(ip, user_name, password)
    channel = ssh.invoke_shell()
    channel.recv(4096)

    unmount(dev)

    channel.send(f'sudo fdisk {dev[:len(dev) - 1]}\n')
    channel.send(f'{password}\n')
    sleep(1)
    channel.recv(10240)

    print_partition(channel)

    for _ in range(len(ans)):
        delete_partition(channel)
        channel.send('\n')

    new_partition(channel)

    for _ in range(4):
        channel.send('\n')
        sleep(1)

    channel.send('Y\n')
    channel.send('t\n')
    channel.send('L\n')
    channel.send('07\n')
    channel.send('w\n')
    sleep(1)

    output = channel.recv(8068).decode()
    print(output)
    logging.info(output)

    quick_file_format()
    usb_eject()
    usb_reconnect()

    print(green("Partitions Merged !!"))
    logging.info("Partitions Merged !!")

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logging.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")
