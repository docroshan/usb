from utilities.utility import *


@fun_count
def usb_available_space():
    print(f"{'*'*20}TestCase started {blue('|usb_2.2|USB Available Space|')}{'*'*20}")
    logger.info(f"{'*'*20}TestCase started {'|usb_2.2|USB Available Space|'}{'*'*20}")
    available_usb()
    usbname = current_usb_name.upper()
    path = dev
    if path != "USB NOT FOUND":
        res = usb_df()
        try:
            assert available_storage == (((res[usbname]['Avail']).split('/'))[-1])

        except AssertionError:
            print(f"Available space of USB is {green(available_storage)}")
            logger.info(f"Available space of USB is {available_storage}")
            print(f"Expected result of of USB is {red(res[usbname]['Avail'])}\n")
            error_msg = f"Available space of USB is {available_storage}, Expected result of of USB is {res[usbname]['Avail']}"
            logger.info(f"Expected result of of USB is {res[usbname]['Avail']}\n")
            print(red("FAIL"))
            logger.error("FAIL")
            return 'FAIL', error_msg

        else:
            print(f"Available space of USB is {green(available_storage)}")
            logger.info(f"Available space of USB is {available_storage}")
            print(f"Expected result of of USB is {green(res[usbname]['Avail'])}\n")
            logger.info(f"Expected result of USB is {res[usbname]['Avail']}\n")
            print(green("PASS"))
            logger.info("PASS")
            return 'PASS', None
        finally:
            print(f"{'*'*30}TestCase ended {blue('|usb_2.2|USB Available Space|')}{'*'*20}\n")
            logger.info(f"{'*'*30}TestCase ended {'|usb_2.2|USB Available Space|'}{'*'*20}\n")
            close()

    else:
        print("INSERT THE USB")
        logger.error("INSERT THE USB")


usb_available_space()
