# How to develop and deploy an online API for any R script

This folder contains an example R project that can be deployed an online API.
The high level idea of deploying R project to be an online API are
1. Zip and upload your own R project to IBM Cloud Pak for Data(CP4D)'s deployment space 
   and have it deployed as an online API. You own R project can come from your local folder or git repo.
2. You only need to focus on your R project development inside or outside of CP4D. 
   If you need to connect databases, 
   CP4D provides a way to use internal connection without disclosing any credentials in the code.
3. Once your R project is ready, CP4D platform Engineers will help to manually deploy your project. CICD can be enabled once your application is verified.

See more details below.

## How to prepare your R project
1. Your main R script must be able to process a JSON as input and then output to a JSON as well. 
   Reason is the same JSON input/output will be used to invoke the online API.
1. Make sure all your needed R code is within one folder. 
  Reason is if your code is everywhere, it will be complex to zip and upload them to CP4D's deployment piece by piece.
1. Do not store any unnecessary data in your R project folder since it mainly for code. 
   Data file will make the folder size unnecessarily larger.
2. Inside your project folder, your R code structure can be as complex as it can be. It is recommended to put the main R file in the root folder.


## How to install R libraries and user your own libraries
Each R online deployment will have its own R environment with its own R libraries. 
We support below 3 options in sequence. The later step will skip exiting libraries.
1. Save all your needed R libraries to a storage volume, 
   especially for those not able to be installed from CRAN. 
   These R libraries will be transferred to deployed R env.
   - Create a folder under root directory of storage volume, for example: r_lib_your_prj_name. 
     Due to a limitation, folder "r_lib_your_prj_name" must be under root directory.
   - Upload/update your r lib to this folder. Please contact Jianbin for guidance on this or watch
     - [How to uploade R libraries to storage volume](../videos/How%20to%20uploade%20R%20libraries%20to%20storage%20volume.mp4)
     - [How to update specific R lib in storage volume](../videos/How%20to%20update%20specific%20R%20lib%20in%20storage%20volume.mp4)
   - Change in the storage volume won't trigger CICD. 
     You may need to "touch" or "update" your code repo to start a new deployment.
2. Create a folder: **own_r_libs** under your project's root directory
and then save your libraries inside. Do not change the folder name. 
   [own_r_libs](./own_r_libs) is an example of including own **gcm.ReferenceTables** 
   - "own_r_libs" will be saved in Git Repo hence it is only suitable for very small packages.
   - When CICD is enabled, any change of "own_r_libs" can trigger an automated deployment.
3. You must contain an "install_r_pkgs.R" file to install needed R libraries for the deployment,
   following this example [install_r_pkgs.R](./install_r_pkgs.R) 
   
## How to define your input and output JSON
1. Must have a list inside input and output JSON to allow 1 or more records to be processed as a batch to improve throughput.
1. Both input and output can be self-defined JSON. 
1. It is highly recommended to follow CP4D's definition because your online API can be tested with CP4D's UI directly.
1. Here is a CP4D-compliant input json example:
    ```
    input_json = {"input_data":[{
            "fields":["AGE","SEXE"],
            "values":[
                [33,"F"],
                [59,"F"],
                [28,"M"]
                ]
            }]}
    ```
1. Here is a CP4D-compliant output json example:
    ```
    output_json = {
          "fields": [
            "prediction_classes",
            "probability"
          ],
          "values": [
            [
              "setosa",
              [0.3563,0.322, 0.3218],
            ],
            [
              "setosa",
              [0.3562,0.322,0.3217]
            ],
            [
              "setosa",
              [0.3562, 0.322,0.3217]
            ]
          ]
        }
    ```
1. "fields" is optional, it is a list of features.
1. "input_data" and "values" is a must.
1. "values" is a list of one or multiple inputs.
1. [predict.R](./predict.R) is an example of using own defined input/output JSON
1. [predict_cpd_compatible_json.R](./predict_cpd_compatible_json.R) is an example of using own defined input/output JSON

## How to test your online API
1. Follow this example [test_online_api.py](./test_online_api.py) to test your online API.
1. Please modify username, password and your API link according.

## How to deploy
It will be done by CPD engineer together with you, if interested, refer to: [Deploy R Online API](../../deployment_with_wml_client/Deploy%20R%20Online%20API.md)