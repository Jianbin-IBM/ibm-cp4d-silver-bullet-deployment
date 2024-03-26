# Usage
It is to show you how to deploy any python project as batch job or online API.

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
python deploy_with_wml_client_py.py --yaml_file [your_yaml_file] --test_run [True/False]
```

- If set "test_run" to be **True**: run the job immediately after deployment
- If set "test_run" to be **False**: only deploy the code package, but not run the job

Once successfully deployed, you will see below output(function_deployment_id will be different):

```
------------------------------------------------------------------------------------------------
Successfully finished deployment creation, deployment_uid='6f5fcc90-2931-4d46-b683-cc67aded2624'
------------------------------------------------------------------------------------------------


function_deployment_id = "6f5fcc90-2931-4d46-b683-cc67aded2624"
```

For "online" deployment, a "Deployment endpoint" will be generated:
```
Deployment endpoint =  https://cpd-cp4data.cluster-adp-ac369665a3d2e9405656d188474ca7f8-0000.eu-de.containers.appdomain.cloud/ml/v4/deployments/3f9536e8-2a8f-4726-8d7d-8c91d2c39eb1/predictions
```

For "batch job" deployment, if you set "test_run" to be **True**, 
you will see below output in addition(job_id will be different):

```job_id: "da717590-10b7-45df-a12b-6e2f2345fc06" successfully submitted```


For "online" deployment, if you set "test_run" to be **True**, 
you will see below output in addition(job_id will be different):
```
result=
 {'predictions': [{'values': [{'stdout': "\n\nLoading payload from local JSON file: input.json\ninput json=\n {'input_data': [{'fields': [], 'values': [1]}]}\n\n\nSaving payload into local JSON file: output.json\n", 'output': {'input_data': [{'fields': [], 'values': [1]}]}}]}]}
```

## Step 3: Run Job

Once the code package is successfully deployed, you can
- Either use CPD WebUI to schedule your job. 
  More in: https://www.ibm.com/docs/en/cloud-paks/cp-data/4.5.x?topic=assets-creating-deployment-job
- Alternatively, you can run your job with below command, 
  which is particularly useful when you want to use an external scheduler (eg. Control M): 

```python run_job.py --yamm_file [your_yaml_file]  --function_deployment_id=[function_deployment_id generated above]```

For "batch job" deployment, 
you will see below output in addition(job_id will be different):

```job_id: "da717590-10b7-45df-a12b-6e2f2345fc06" successfully submitted```

For "online" deployment, 
you will see below output in addition(job_id will be different):
```
result=
 {'predictions': [{'values': [{'stdout': "\n\nLoading payload from local JSON file: input.json\ninput json=\n {'input_data': [{'fields': [], 'values': [1]}]}\n\n\nSaving payload into local JSON file: output.json\n", 'output': {'input_data': [{'fields': [], 'values': [1]}]}}]}]}
```

## How to input/output data
There are multiple options to supply input. 

- Option 1: Read input and/or write output directly within your python project. 
  Input/output can be files, tables from databases, external APIs and so on.
- Option 2: You can also supply input externally. 
  It is very common for "online" deployment to generate some output based on the input, eg predictions.
  
  1) [main_online.py](../py_examples/online/main_online.py) provided an exemplary code
     to process input JSON from stdin and also write output JSON to stderr. 
     The reason we use stderr instead of stdout to save the output is 
     because we then can use stdout to show all the running log.
  2) [test_main_onlne.py](../py_examples/online/test_main_online.py) 
     provided an exemplary testing code.
     If worked fine, your deployment in CPD will work as well.

## Additional Notes

- For data source connections/data assets created in Watson Studio, 
  you need to promote or replica those you needed in deployment space with exactly same configuration. 
  
- CPD3.5 needs complex workaround to connect data source connections in deployment space. 
Hence currently we recommend getting connection credentials inside your projects, eg from a local configuration file and so on.
This is not an issue for CPD4.x.
  
- For "model" deployment, we have 2 options here
  
    1) To develop a new API (Future work): 
       ```deploy_model --yaml_file [your_yaml_file]```
        
    2) Invoke your Model inside your own python projects, 
       then we can deploy with code package as well. 
       
- Use "online" mode when it is very necessary, because "online" deployment will consume the CPU/Memory resources all the time, 
  while "batch job" only consume resource in a fractional time. 
 
