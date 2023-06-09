from utilities.usb import *


# To print partition details
def print_partition(connect):
    connect.send('p\n')
    sleep(1)


def delete_partition(connect):
    connect.send('d\n')
    sleep(1)


def new_partition(connect):
    connect.send('n\n')
    sleep(1)


@fun_count
def drive_partition():

    print(f"{'*' * 20} {cyan(os.path.basename(__file__))} Test Case Started {'*' * 20}")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Started {'*' * 20}")

    res = super_access(password, f"sudo fdisk -l | grep {dev[:len(dev) - 1]}").split()[2]
    print("Total USB Disk size:", green(res))
    logger.info(f"Total USB Disk size: {res}")

    flag = 0
    result = re.findall(r'\d', partition_size)
    if (int(partitions_number)*int(result[0])) <= float(res):
        print("Creating", green(partitions_number), "Partitions of", green(partition_size), "each.\n")
        logger.info(f"Creating {partitions_number} Partitions of {partition_size} each.\n")

        ssh = ssh_connect(ip, user_name, password)
        channel = ssh.invoke_shell()
        channel.recv(4096)

        # unmount(dev) all available partitions
        for x in range(1, int(partitions_number)+1):
            dev_ = f'{dev[:len(dev) - 1]}{x}'
            unmount(dev_)

        channel.send(f'sudo fdisk {dev[:len(dev) - 1]}\n')
        channel.send(f'{password}\n')
        sleep(1)
        channel.recv(10240)

        print_partition(channel)

        stdout = super_access(password, f"lsblk | grep {(dev[:len(dev) - 1]).split('/')[-1]}")
        stale, *before_partition = stdout.strip().split('\n')

        # partition deletion
        for _ in range(len(before_partition)):
            delete_partition(channel)
            channel.send('\n')

        # new partition creation
        for _ in range(int(partitions_number)):
            new_partition(channel)

            for _ in range(3):
                channel.send('\n')
                sleep(1)

            channel.send(f"{partition_size}\n")
            sleep(1)
            channel.send('Y\n')

        # file format each partition(inside disk manager)
        # for part in range(1, int(partitions_number)+1):
        #     channel.send('t\n')
        #     channel.send(f'{part}\n')
        #     channel.send('L\n')
        #     channel.send('07\n')

        channel.send('w\n')
        sleep(1)
        output = channel.recv(102400).decode()
        print(output)
        print()
        logger.info(output)
        logger.info('')

        # format & renames the newly created partitions
        for x in range(1, int(partitions_number)+1):
            dev_ = f'{dev[:len(dev) - 1]}{x}'
            unmount(dev_)
            super_access(password, f"mkfs.vfat {dev_}")
            print(f"Formatted partition {x}")
            mlabel(dev_, f'Partition_{x}')
            sleep(1)

        usb_eject()
        usb_reconnect()

        print(green("Partitions Created !!"))
        logger.info(f"Partitions Created !!")

        flag += 1

    else:
        print(red("Memory Exceeding, Cannot create"), green(partitions_number), red("Partitions of"), green(partition_size), red("each.)\n"))
        logger.error(f"Memory Exceeding, Cannot create {partitions_number} Partitions of {partition_size} each.")

    print("*" * 20, cyan(os.path.basename(__file__)), "Test Case Completed", "*" * 20, "\n")
    logger.info(f"{'*' * 20} {os.path.basename(__file__)} Test Case Completed {'*' * 20}\n")

    if flag:
        return 'PASS', None
    else:
        return 'FAIL', 'Partitions not created: Memory Exceeding or USB not Found'
