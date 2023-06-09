from pathlib import *
import subprocess
import time
from utilities.parser_creation import *

print(f"{'*' * 20}", __name__.usb_run)
start = time.time()

list_ = []
user_config_file = get_attr('./user_data/user_config.ini', 'user_config_file')

config = configparser.ConfigParser()
config.read(user_config_file)
section = 'TEST_CASES_FOR_EXECUTION'
for i in config.items(section):
    if i[0] == 'all' and i[-1] == 'Yes':
        for key, value in config.items(section)[1:]:
            list_ += [key]
        break
    else:
        if i[-1] == 'Yes':
            list_ += [i[0]]

try:
    for value in list_:
        create_config('TEST_CASES', 'pick_test', value, user_config_file)
        subprocess.run(['python', f'./Testcases/{value}.py'], check=True)

except subprocess.CalledProcessError:
    print('Unable to run File or File Not Found')

# To get all the paths of the log file in result dir
path = Path('./results/')
win_paths = ['./results/'+str(i).split('\\')[-1] for i in path.iterdir() if i.suffix == '.log' and i.is_file()]

# Merging all available log files into a single log
with open('./output.log', 'w') as output_file:
    for path in win_paths:
        if path.split('/')[-1].split('.')[0] in list_:
            content = open(path, 'r').read()
            output_file.write(content)

end = time.time()
print(f"Total time taken:{str(round((end - start), 2))} sec")
