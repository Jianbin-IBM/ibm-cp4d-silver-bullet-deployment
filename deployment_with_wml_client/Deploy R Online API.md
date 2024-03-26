# Usage
It is to deploy any R project as online API.

Set your working directory under **deployment_with_wml_client**.

Please make sure you have latest **ibm-watson-machine-learning** package. 
This tool is verified in 1.0.253 onwards.

```
pip install ibm-watson-machine-learning --upgrade
```

## Step 1: Ready your code
2 prerequistes should be met:
1. Ensure you put all the code into one root directory. 
You can have many subdirectories and dependencies inside the root directory.

2. Ensure you have main python script is under the root directory. 

## Step 2: Configure YAML file
Please make a copy of configuration_template.yaml and then modify the configuration accordingly. 

I tried to make the yaml file self-explainable, please let me know if there is any confusing part!

## Step 3: Deploy!
Run below command to deploy your python code package:

```
python deploy_with_wml_client_r_online.py --yaml_file [your_yaml_file] --test_run [True/False]
```

- If set "test_run" to be **True**: run the job immediately after deployment
- If set "test_run" to be **False**: only deploy the code package, but not run the job

For "online" deployment, once successfully deployed, a "Deployment endpoint" will be generated:
```
Deployment endpoint =  https://cpd-cp4data.cluster-adp-ac369665a3d2e9405656d188474ca7f8-0000.eu-de.containers.appdomain.cloud/ml/v4/deployments/3f9536e8-2a8f-4726-8d7d-8c91d2c39eb1/predictions
```

For "online" deployment, if you set "test_run" to be **True**, 
you will see below output in addition(job_id will be different):
```
result=
 {'predictions': [{'values': [{'stdout': "\n\nLoading payload from local JSON file: input.json\ninput json=\n {'input_data': [{'fields': [], 'values': [1]}]}\n\n\nSaving payload into local JSON file: output.json\n", 'output': {'input_data': [{'fields': [], 'values': [1]}]}}]}]}
```

## Example
[r_online](../r_examples/r_online) provided an example.