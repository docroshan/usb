from pathlib import *
import subprocess
import time
from utilities.parser_creation import *
from utilities.reports import *


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
        subprocess.run(['python', f'Testcases/{value}.py'], check=True)

except subprocess.CalledProcessError:
    print('Unable to run File or File Not Found')

# Getting all the paths of the log file in 'results' directory
path = Path('results')
win_paths = ['./'+str(i).split('\\')[-1] for i in path.iterdir() if i.suffix == '.log' and i.is_file()]
print('Log File Paths:', win_paths)

# for reading each testcase csv result and creating one csv file
count = 0
with open('./results/testresult.csv', 'w', newline='') as f1:
    writer = csv.writer(f1)
    writer.writerow(['TestCase No.', 'TestCase Name', 'Status', 'Remarks'])

    for tc in list_:
        with open(f'./results/{tc}.csv', 'r') as f:
            lines = f.readlines()
            for i in lines[1:]:
                print(i)
                number, tc_name, status, reason = i.split(',')
                count += int(number)
                writer.writerow([count, tc_name, status, reason.strip('\n')])

html_reports()

# Merging current running Test cases log files into a single output-log
with open('output.log', 'w') as output_file:
    for path in win_paths:
        content = open(path, 'r').read()
        output_file.write(content)

end = time.time()
print(f"Total time taken:{str(round((end - start), 2))} sec")
