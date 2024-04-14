# Introduction
 "**S**ilver **B**ullet on **D**eployment with **W**atson **M**achine **L**earning" 
 aims with deploying any python/R projects to IBM Cloud Pak for Data (CPD) on-prem or CPDaas. 
 With simplified interfaces and intuitive yaml example, users without any prior knowledge of CPD can be enabled in several minutes.

There are 2 ways to deploy. One is using [wml client](https://pypi.org/project/ibm-watson-machine-learning/) 
which is is a library that allows to work with Watson Machine Learning service on IBM Cloud and IBM Cloud for Data. 
The other is using [cpdctl](https://github.com/IBM/cpdctl). 
In the code repo, we provided APIs and examples for both methods.

**Features**
- Support projects developed within or outside of Watson Studio in IBM Cloud Pak for Data.
- Support CPD 3.5/4.0/4.5/4.6/4.7/4.8 and potentially all future versions
- Support Python/R Scripts, Python/R notebooks, R Shiny.  
- Support "batch job"  and "online" deployment
- Support all ML frameworks, as long as it can be done with python/R.
- It provided one line deployment script to enable CI/CD.
- Email notification can be enabled if there is an accessible SMTP server. 
  It is particularly useful when python/R failed due to bugs or imperfect data.
- Contain **stderr** and **stdout** in job logs and easy to know what happened in detail. 


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
- **deployment_with_cpdctl** : 
  - Support py script and notebook deployment.
  - Support R shiny deployment. 
  - Support deploy to SPARK and any customised environment.
  - Do not support py or R script as "online" API yet.
  
- **deployment_with_wml_client**
  - Support py script deployment as job or online API
  - Support r script deployment as online API
  - Do not support Jupyter notebook directly and only can be deployed after converting it to py.
  - Do not support deploy to SPARK environment and any customised environment.
  
- **py_examples** :  contains examples for python
- **r_example** : contains examples for R

# Usage
We have 2 ways to deploy: 
- With cpdctl, please refer to [**deployment_with_cpdctl**](deployment_with_cpdctl)
- With WML client, please refer to [**deployment_with_wml_client**](deployment_with_wml_client)
