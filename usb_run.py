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
    open('output.log', 'w')  # Creating output.log file
    for value in list_:
        create_config('TEST_CASES', 'pick_test', value, user_config_file)
        subprocess.run(['python', f'Testcases/{value}.py'], check=True)

        # Merging current running Test cases logs into a single output-log
        testcase_name = open(f'./Testcases/{value}.py', 'r').readlines()[-1][:-3]  # Fetching function name
        content = open(f'./results/{testcase_name}.log', 'r').read() # Fetching contents of individual logs
        open('output.log', 'a').write(content)  # appending logs

    # for reading each testcase csv result and creating one csv file
    count = 0
    with open('./results/testresult.csv', 'w', newline='') as f1:
        writer = csv.writer(f1)
        writer.writerow(['TestCase No.', 'TestCase Name', 'Status', 'Remarks'])

        for tc in list_:
            try:
                with open(f'./results/{tc}.csv', 'r') as f:
                    lines = f.readlines()
                    for i in lines[1:]:
                        number, tc_name, status, reason = i.split(',')
                        count += int(number)
                        writer.writerow([count, tc_name, status, reason.strip('\n')])
            except FileNotFoundError:
                pass

    html_reports()


except subprocess.CalledProcessError:
    print('Unable to run File or File Not Found')

end = time.time()
print(f"Total time taken:{str(round((end - start), 2))} sec")
