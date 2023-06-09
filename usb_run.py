from TestCase.usb_1_0 import *
from TestCase.usb_1_1 import *
from TestCase.usb_1_2 import *
from TestCase.usb_4_0 import *
from TestCase.usb_5_0 import *
from TestCase.usb_7_0 import *
from TestCase.usb_7_1 import *
# from TestCase.usb_6_0 import *
from TestCase.usb_10_0 import *
from TestCase.usb_10_1 import *
from TestCase.usb_10_2 import *
from TestCase.usb_12_0 import *
from TestCase.usb_12_1 import *


start = time.time()
res = super_access(password, f"mlabel -i {dev_path} -s").split()[-1]
print(res)
# get_usb_name()
# usb_mount_point()
# usb_version()
# usb_capacity()
# usb_available_space()
# usb_unmount()
# usb_mount()
# usb_format()
# file_format_fat()
# file_ops()
# delete_file('')
# usb_rename_drive()
# safe_eject_drive()

end = time.time()
print("Total time taken: "+green(str(round(end - start, 2))))
