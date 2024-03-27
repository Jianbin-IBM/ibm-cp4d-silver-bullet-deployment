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
        SILVER_BULLET_BRANCH = 'master'
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


                        def command = """
                        curl -s https://api.github.com/repos/IBM/cpdctl/releases | \
                          jq -r '.[0].assets[] | select (.name == "cpdctl_linux_amd64.tar.gz") | .url'  | \
                          xargs -I {} curl -sSL -H 'Accept: application/octet-stream' "{}" -o cpdctl_darwin_arm64.tar.gz
                        
                        tar -xvf cpdctl_darwin_arm64.tar.gz
        
                        echo "Installed cpdctl in version:"
                        ./cpdctl version
                        """
                        
                        //sh command
                                        
                        // Clone the yaml files
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
