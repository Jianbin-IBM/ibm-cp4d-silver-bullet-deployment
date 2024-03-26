# How to develop and deploy an online API for any R script

This folder contains an example python project that can be deployed an online API.
The high level idea of deploying python project to be an online API are
1. Zip and upload your own python project to IBM Cloud Pak for Data(CP4D)'s deployment space 
   and have it deployed as an online API. You own python project can come from your local folder or git repo.
2. You only need to focus on your python project development inside or outside of CP4D. 
   If you need to connect databases, 
   CP4D provides a way to use internal connection without disclosing any credentials in the code.
3. Once your python project is ready, CP4D platform Engineers will help to manually deploy your project. 
   CICD can be enabled once your application is verified.
   
Please follow below examples to create your own.

## MNIST example
All python online project must have a [main_online.py](main_online.py), which must have 2 functions
1. preprocess(): it will only run once
2. main_process(): it will run again and again whenever online API is called

Inside preprocess() and main_process(), you can call your own functions, 
like what [main_predict.py](main_predict.py) did. 

If your projects have any additional libraries needed, 
you can do "pip install xx --index https://artifactory.gcp.anz/artifactory/api/pypi/pypi/simple/ --trusted-host artifactory.gcp.anz --user"

## How to test your online API
In this example [main_online.py](main_online.py), 
"main" won't be called with online API, it is the best place to test your your own project.  
If it works, very like your online deployment will work 
provided we make sure all needed python libraries all installed.

## How to deploy
It will be done by CPD engineer together with you, if interested, 
refer to: [Deploy Python Online API with preprocess](../../../deployment_with_wml_client/Deploy%20Python%20Online%20API%20with%20preprocess.md)

