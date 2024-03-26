# This is an example code for applications with input and output
# It can be deployed as batch job and also can be deployed as online application

# If there are missing python libraries, the first thing is to install missing libraries
# Below is an example to install ibm-watson-machine-learning
import subprocess
# output = subprocess.run(["pip3", "install", "ibm-watson-machine-learning", "--upgrade"], capture_output=True, text=True).stdout
# print(output)

import os
import warnings
import json
import sys
from your_own_process import *

warnings.filterwarnings("ignore")

# print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getEnvVariables() :
    vars = {}
    for name, value in os.environ.items():
        vars[name] = value
    return vars

def load_input_json():
    data = json.load(sys.stdin)
    print('Input JSON data loaded')
    return data


# Please modify this code according your own online process


# input JSON format must have "input_data", "fields" and "values", an example below
# more explained in: https://cloud.ibm.com/apidocs/machine-learning#deployments-compute-predictions

# {"input_data":[{
#         "fields":["AGE","SEXE"],
#         "values":[
#             [33,"F"],
#             [59,"F"],
#             [28,"M"]
#             ]
#         }]}

# Output must be in JSON format
#  - Users can define their own output, as long as it can be processed by their own applications.
#  - If want to be consist with model deployment, output JSON should have "fields" and "values".
#     Example below:
#     output_json = {
#       "fields": [
#         "prediction_classes",
#         "probability"
#       ],
#       "values": [
#         [
#           7,
#           [
#             0.9999523162841797,
#             8.347302582478733e-08
#           ]
#         ],
#         [
#           2,
#           [
#             8.570060003876279e-07,
#             0.9999991655349731
#           ]
#         ]
#       ]
#     }


if __name__ == '__main__':

    print('Start your application')

    input_json = load_input_json()

    import io

    # Redirect stderr to a StringIO object
    original_stderr = sys.stderr
    sys.stderr = io.StringIO()

    output_json = your_own_process(input_json)
    print('Output JSON data generated')

    # Your code that writes to stderr
    print("This goes to stderr")

    # Clear the StringIO object (optional)
    sys.stderr.truncate(0)
    sys.stderr.seek(0)

    # Redirect stderr back to the original object
    sys.stderr = original_stderr
    # Here stderr is used to save your output result
    eprint(output_json, end='')


