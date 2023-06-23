from utilities.utility import *


@fun_count
def usb_capacity():
    print(f"{'*'*20}TestCase started {blue('|usb_2.1|USB Capacity|')}{'*'*20}")
    logger.info(f"{'*'*20}TestCase started {'|usb_2.1|USB Capacity|'}{'*'*20}")
    available_usb()
    usbname = current_usb_name.upper()
    path = dev

    if path != "USB NOT FOUND":
        res = usb_df()
        try:
            assert total_storage == (res[usbname]['Size'])

        except AssertionError:
            print(f"Actual Capacity of USB is {green(total_storage)}")
            logger.info(f"Actual Capacity of USB is {total_storage}")
            print(f"Expected result of of USB is {red(res[usbname]['Size'])}\n")
            error_msg = f'''Actual Capacity of USB is {total_storage}, Expected result of of USB is {res[usbname]['Size']}'''
            logger.info(f"Expected result of of USB is {res[usbname]['Size']}\n")
            print(red("FAIL"))
            logger.error("FAIL")
            return "FAIL", error_msg

        except TypeError:
            print(red('USB NOT FOUND'))
            logger.error("USB NOT FOUND..!!")

        else:
            print(f"Total Capacity of USB is {green(total_storage)}")
            logger.info(f"Total Capacity of USB is {total_storage}")
            print(f"Expected result of of USB is {green(res[usbname]['Size'])}\n")
            logger.info(f"Expected result of USB is {res[usbname]['Size']}\n")
            print(green("PASS"))
            logger.info("PASS")
            return "PASS", None

        finally:
            print(f"{'*'*20}TestCase ended {blue('|usb_2.1|USB Capacity|')}{'*'*20}\n")
            logger.info(f"{'*'*20}TestCase ended {'|usb_2.1|USB Capacity|'}{'*'*20}\n")
            close()

    else:
        print("INSERT THE USB")
        logger.error("INSERT THE USB")


usb_capacity()
