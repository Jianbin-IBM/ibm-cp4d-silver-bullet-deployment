# Introduction
 "**S**ilver **B**ullet on **D**eployment with **W**atson **M**achine **L**earning" 
 aims with deploying any python projects to any IBM Cloud Pak for Data (CPD) system. 
 With simplified interface and clear yaml example, users can be enabled in several minutes.

There are 2 ways to deploy. One is using [wml client](https://pypi.org/project/ibm-watson-machine-learning/) 
which is is a library that allows to work with Watson Machine Learning service on IBM Cloud and IBM Cloud for Data. 
The other is using [cpdctl](https://github.com/IBM/cpdctl). 
In the code repo, we provided APIs and examples for both methods.

**Features**
- Support projects developed with Watson Studio in IBM Cloud Pak for Data.
- Support projects developed outside of Watson Studio.
- Support CPD 3.5/4.0/4.5/4.6/4.7.
- Support "batch job"  and "online" deployment.
- Support CPD as a platform and also CPD as a service.
- Support all ML frameworks, as long as it can be done with python.
- It can be used to enable CI/CD.
- If there is an accessible SMTP server within CPD, email notification can be enabled. 
  It is particularly useful when python scripts failed due to bugs or imperfect data.
- Contain **stderr** and **stdout** in job logs, so you know what happened in detail. 


Authors: Jianbin Tang, jbtang@au1.ibm.com; Rutvik Dave, Rutvik.Dave@ibm.com

Also appreciate help from: 
- Xavier Mary
- Cedric Jouan
- Randy Phoa
- Carlos Mejia Johnson


# License
- Apache License 2.0.
- Feel free to fork it!   
- Not a license requirement, but if you like it or used it, 
  appreciate your "watch" and "star" the project :) 
- Welcome your feedbacks and contributions. 

  
Thank you!

# Code Structure

- **deployment_with_wml_client**
  - APIs to deploy any python projects to Watson Machine Learning (WML) deployment space. 
  - It supports batch job and online deployment.
  - Jupyter notebook can be deployed after converting it to py.
  - Not support deploy to SPARK environment.
- **deployment_with_cpdctl** : 
  - APIs to deploy any python projects to Watson Machine Learning deployment space.
  - It supports py script and notebook deployment. 
  - It supports deploy to SPARK and any customised environment.
  - Not support "online" deployment yet.
- **batch_job_example** : an example "batchjob" project code folder to be deployed.
- **online_example** : an example "online" project code folder to be deployed.
- **notebook_example** : an example with example notebooks to be deployed.

# Usage
We have 2 ways to deploy: 
- With WML client, please refer to [**deployment_with_wml_client**](deployment_with_wml_client)
- With cpdctl, please refer to [**deployment_with_cpdctl**](deployment_with_cpdctl)

