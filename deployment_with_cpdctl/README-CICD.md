# CICD with Jenkins
This read me contains the steps to achieve automation on IBM's Cloud Pak for Data (CP4D) platform using a jenkins pipeline. For the project, you will need a Jenkins instance set up, you can select default settings for setup. 

## Set up

For this project once you have a jenkins instance set up, you will need to install the default plugins but also the following plugins.

- Pipeline Utility Steps v2.16.2
- Python Plugin v1.3
- SSH server v3.322 

Additionally you will need to setup an SSH key for your Github with the public key associated with your account and the private key stored as a secret in the Jenkins Credentials Provider. To generate a new SSH key follow the steps here: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Once you have a SSH key generated, go to Manage Jenkins -> Security -> Credentials -> Add Credentials -> Jenkins Credentials Provider: Jenkins

That will open a screen in which you can store your secret. Select Kind as SSH username with private key, and store your private key there. You can leave id blank and it will auto generate an id for you or you can input a field, but the ID will be used in a later step as CREDENTIAL_ID.

To start a new project, on the Jenkins dashboard select new item, and select Pipeline. For options select:
- Do not allow concurrent builds
- Build Triggers: GitHub hook trigger for GITScm polling

And for the pipeline script add the following script.

## Pipeline Script

Once you create your project, under Configure, input the following script. The variables that you have to modify are:

CREDENTIAL_ID: The id of the credentials previously generated.  
REPO_URL: The link to the repo in which the individual project files are located. This has to be unique for each project you have.   
REPO_BRANCH: The branch in which you wish to deploy onto CP4D.  
YAML_URL: This will be the link to repo that contains all the yaml configuration files for the various projects you wish to implement a cicd pipeline for. Once set up, you can reuse this for multiple projects.  
YAML_BRANCH: The branch in which you have stored the configurations files in.  
SILVER_BULLET_URL: The repo url to the silver bullet code, this should remain unchanged.  
SILVER_BULLER_BRANCH: The branch should be master, this should remain unchaged.
```grovy script
pipeline {
    agent any
    
    environment {
        CREDENTIAL_ID = 'YOUR CREDENTIAL ID HERE'
        // Url and Branch for the Repo where code is located
        REPO_URL = 'YOUR GITHUB PROJECT LINK HERE'
        REPO_BRANCH = 'main'
        // Url and Branch for the yaml configuration files 
        YAML_URL = 'YOUR GITHUB CONFIGURATIONS LINK HERE'
        YAML_BRANCH = 'main'
        // Url and Branch for Silver Bullet Code
        SILVER_BULLET_URL = 'https://github.com/Jianbin-IBM/ibm-cp4d-silver-bullet-deployment.git'
        SILVER_BULLET_BRANCH = 'cicd'
    }
    
    stages {
        stage('Clone') {
            steps {
                script {
                    // Delete the entire workspace
                    deleteDir()

                    // Create 'code' directory and clone the first repository
                    dir('code') {
                        git branch: env.REPO_BRANCH, credentialsId: env.CREDENTIAL_ID, url: env.REPO_URL
                    }
                }
            }
        }
        stage('Install CPDCTL and Dependencies'){
            steps{
                script{
                    sh "pip3 install pyyaml"
                    sh "pip3 install requests"
                    
                    // Create 'silver-bullet' directory and clone the second repository
                    dir('silver-bullet') {
                        checkout([$class: 'GitSCM', branches: [[name: env.SILVER_BULLET_BRANCH]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: 'deployment_with_cpdctl']]]], userRemoteConfigs: [[url: 'https://github.com/Jianbin-IBM/ibm-cp4d-silver-bullet-deployment.git']]])
                        dir('deployment_with_cpdctl/yaml_files'){
                            git branch: env.YAML_BRANCH, credentialsId: env.CREDENTIAL_ID, url: env.YAML_URL
                        }
                    }
                }
            }
        }
        stage('Run Deployments') {
            steps {
                script {
                    dir('silver-bullet/deployment_with_cpdctl') {
                        // Iterate over files in yaml_files directory
                        def yamlFilesDir = 'yaml_files'
            
                        // Get a list of YAML files in yaml_files directory
                        def yamlFiles = sh(script: 'ls yaml_files/*.yaml', returnStdout: true).trim().split('\n')
            
                        yamlFiles.each { yamlFile ->
                            echo "yaml file: $yamlFile"
                            
                            def yamlContent = readYaml file: yamlFile.trim()
                            def githubURL = yamlContent.prj_info.github_url

                            if(githubURL == env.REPO_URL) {
                                sh "python3 deploy_with_cpdctl.py --yaml $yamlFile" 
                            }
                        }
                    }
                }
            }
        }
    }
}

```

## Usage



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
