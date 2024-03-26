# Usage

It is to show you how to deploy any python project as online API.

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
python deploy_with_wml_client_py_online_preprocess.py --yaml_file [your_yaml_file] --test_run [True/False]
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

## Step 3: Test your online API

Once the code package is successfully deployed, you can
- Either use CPD WebUI to schedule your job. 
  More in: https://www.ibm.com/docs/en/cloud-paks/cp-data/4.5.x?topic=assets-creating-deployment-job
- Alternatively, you can run your job with below command, 
  which is particularly useful when you want to use an external scheduler (eg. Control M): 

```python run_job.py --yamm_file [your_yaml_file]  --function_deployment_id=[function_deployment_id generated above]```

For "batch job" deployment, 
you will see below output in addition(job_id will be different):

```job_id: "da717590-10b7-45df-a12b-6e2f2345fc06" successfully submitted```


This script does support "online" deployment as well. 
It will run the whole python project when is called. 
Hence it can be slow because some python projects will have pre-process, 
for example, 
- install needed libraries
- load large ML into memory.
Hence we recommend to use [Deploy Python Online API with preprocess](./Deploy Python Online API with preprocess)
For "online" deployment, 
you will see below output in addition(job_id will be different):
```
result=
 {'predictions': [{'values': [{'stdout': "\n\nLoading payload from local JSON file: input.json\ninput json=\n {'input_data': [{'fields': [], 'values': [1]}]}\n\n\nSaving payload into local JSON file: output.json\n", 'output': {'input_data': [{'fields': [], 'values': [1]}]}}]}]}
```

## Example
[mnist_with_preprocess](../py_examples/online/mnist_with_preprocess) provided an example.