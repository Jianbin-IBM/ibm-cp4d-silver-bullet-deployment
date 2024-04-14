# Introduction

- Support py script and notebook deployment.
- Support R shiny deployment. 
- Support deploy to SPARK and any customised environment.
- Do not support py or R script as "online" API yet.

## Prerequisites

Download the corresponding latest CPDCTL executable from: https://github.com/IBM/cpdctl/releases to a local folder. 
Then add your local folder to your system path to ensure cpdctl can be executed anywhere.

Please note although product team endevour to make sure it is bachwards compatiable, but appreciate your report to us if you met any issues,

## Deployment
Set your working directory under **deployment_with_cpdctl**.

### Step 1: Configure YAML file
Please make a copy of configuration_template_python.yaml or configuration_template_R.yaml  and then modify the configuration accordingly. 

I tried to make the yaml file variables to be similar to previous versions of this tool, however 
there are some key differences.


### Step 2 for Python : Deploy!
Run below command to deploy your python code package or notebook:

```
python deploy_with_cpdctl.py --yaml_file [your_yaml_file]
```

**Note:** If no yaml_file is provided it will default to: configuration_template_python.yaml

The tool will upload the asset, it currently supports jupyter notebooks (.ipynb) and code package. If a 
a previously uploaded asset with the same name is found, it will print the following message:

```
#######################################################
File exists on CP4D, to update file change yaml 
configuration: deployment_info -> force_2_update
#######################################################
```

Otherwise it will print the following message:

```
#######################################################
Notebook [notebook_example.ipynb] successfully uploaded to cp4d
with asset id [747ed3a3-e716-4c11-9ded-a53466b8c788].
#######################################################
```
Note: Asset id and notebook name will be different


### Step 3 for Python : Run Job

Run below command to run your python code package or notebook:

```
python run_job_with_cpdctl.py --yaml_file [your_yaml_file] --test_run [True/False]
```

**Note:** If no yaml_file is provided it will default to: configuration_template_python.yaml
```
#######################################################
Job [notebook_example_job] created successfully
with job id [37084ce6-11b6-4610-8572-9a349147e7a5].
#######################################################
```

Note: Job id and job name will be different


**Note** If a job has been previously created using the same name, it will use the same job, to run a
new job, however if force_new_job is set to true in the yaml file, it will delete the previous job and
create a new job.

If --test_run is set to True, it will run the job with the specified runtime variables and print the notebook or code package
logs to console. An example of this looks like:

**Code Package Example Output**

...

Pandas version = 1.4.3
sum is 5
2023-05-07 22:42:35.026431

Sum of first 100 million numbers is: 49999995000000
Execution time: 1.0233614444732666 seconds
0:00:01.023471

Execution time: 1.0024995803833008 seconds
0:00:02.026528


**Note:** This is using batch_job_example folder, with main file as main_batch_job.py

**Notebook Example Output**

...

Cell 1:
hello world

**Note:** This is from the notebook_example folder, with main file as cpdctl-test-notebook.ipynb

### Step 2 for R: Deploy!
Run below command to deploy your python code package or notebook:

```
python deploy_r_with_cpdctl.py --yaml_file [your_yaml_file]
```

**Note:** If no yaml_file is provided it will default to: configuration_template_R.yaml


## Additional Notes

- CPDCTL is a versatile tool and has many capabilties, this tool simplifies the deploy and run process, 
however it has been made to be easily be modified.

- For data source connections/data assets created in Watson Studio, 
  you need to promote or replica those you needed in deployment space with exactly same configuration.  
