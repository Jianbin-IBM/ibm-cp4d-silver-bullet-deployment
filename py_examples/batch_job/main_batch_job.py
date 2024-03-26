# This is an example code for applications without input and output, usually suitable for batch job application

# In deployment space, there might be missing python libraries. If so, the first thing is to install missing libraries
# Below is an example to install ibm-watson-machine-learning
import subprocess
# output = subprocess.run(["pip3", "install", "ibm-watson-machine-learning", "--upgrade"], capture_output=True, text=True).stdout
# print(output)

import warnings

warnings.filterwarnings("ignore")

import pandas as pd

print('Pandas version =', pd.__version__)
# print('seaborn version =', sns.__version__)

# os.system('pip install xxx.whl')

############### Insert your main code ##################
a = 1
b = 4
c = a + d
print('sum is', c)

import time

# get the start time
st = time.time()

from datetime import datetime

# Returns a datetime object containing the local date and time
dateTimeObj = datetime.now()
print(dateTimeObj)

# main program
# find sum to first 1 million numbers
sum_x = 0
for i in range(10000000):
    sum_x += i

print('Sum of first 100 million numbers is:', sum_x)

# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

dur = datetime.now() - dateTimeObj
print(dur)

# get the start time
st = time.time()
# wait for 5 seconds
time.sleep(1)
# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
dur = datetime.now() - dateTimeObj
print(dur)




