# This is an example code for applications with input and output, usually needed for online application
# You must load your input from "input.json" from the same folder that main python file sit with.
# Your output must be in JSON format and you must also dump your output JSON to stderr which will be processed.


# In deployment space, there might be missing python libraries. If so, the first thing is to install missing libraries
# Below is an example to install ibm-watson-machine-learning
import subprocess
#output = subprocess.run(["pip3", "install", "torch","torchvision","torchaudio", "--upgrade"], capture_output=True, text=True).stdout
#output = subprocess.run(["pip3", "install", "onnxruntime"], capture_output=True, text=True).stdout
#print(output)

import os
import warnings
import json
import sys

from mnist_predict import mnist_predict

warnings.filterwarnings("ignore")

# print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getEnvVariables() :
    vars = {}
    for name, value in os.environ.items():
        vars[name] = value
    return vars

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
def load_input_json():
    data = json.load(sys.stdin)
    print('Input JSON data loaded')

    return data

# Output must be in JSON format
# Users can define their own output, as long as it can be processed by their own applications.
def your_own_process(input_json):

    output_json = mnist_predict(input_json)

    # output_json=input_json

    print('Output JSON data generated')
    return output_json


if __name__ == '__main__':

    input_json = load_input_json()

    output_json = your_own_process(input_json)

    # we use stderr to save your output result
    eprint(output_json, end='')


