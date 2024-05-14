# Introduction
"**Silver Bullet on Deploying Any Data Science Projects to IBM Cloud Pak for Data**"
 aims to deploy any python/R Data Science projects and ML models to IBM Cloud Pak for Data (CPD) on-prem or CPDaas. 
With a simplified and consistent interface, users without any prior knowledge of IBM Cloud Pak for Data can be enabled in several minutes.  
By configuring a self-explained YAML file, all the deployments can be done with one-line script, 
 which can be used to enable CI/CD very easily.

**Features**
- Support projects developed within or outside of Watson Studio in IBM Cloud Pak for Data.
- Support CPD 3.5/4.0/4.5/4.6/4.7/4.8 and potentially all future versions
- Support Python/R Scripts, Python/R notebooks, R Shiny.  
- Support "batch job"  and "online" deployment
- Support all ML frameworks, as long as it can be done with python/R.
- Email notification can be enabled if there is an accessible SMTP server. 
  It is particularly useful when python/R failed due to bugs or imperfect data.
- Contain **stderr** and **stdout** in job logs and easy to know what happened in detail. 

Authors: Jianbin Tang, jbtang@au1.ibm.com; Rutvik Dave, Rutvik.Dave@ibm.com

Also appreciate help from: 
- Xavier Mary
- Cedric Jouan
- Randy Phoa
- Carlos Mejia Johnson

# Usage
There are 2 ways to deploy. 
- With [cpdctl](https://github.com/IBM/cpdctl), please refer to [**deployment_with_cpdctl**](deployment_with_cpdctl)
- With [wml client](https://pypi.org/project/ibm-watson-machine-learning/), please refer to [**deployment_with_wml_client**](deployment_with_wml_client)

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


# License
- Apache License 2.0.
- Feel free to fork it!   
- Not a license requirement, but if you like it or used it, 
  appreciate your "watch" and "star" the project :) 
- Welcome your feedbacks and contributions. 

  
Thank you!

