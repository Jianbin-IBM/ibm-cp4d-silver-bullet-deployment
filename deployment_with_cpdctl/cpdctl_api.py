import subprocess
import os
import json
import requests
import platform
import tarfile
import zipfile
import yaml

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def get_space_command(space_type):
    if(space_type == "deployment"):
        space_command = "--space-id"
        return space_command
    elif(space_type == "project"):
        space_command = "--project-id"
        return space_command
    else:
        print("Error: Incorrect Space Type:", space_type, "please use project or deployment space")
        exit()

def install_cpdctl(cpdctl_config):
    if(os.path.exists("cpdctl")):
        pass
    else: 
        if(cpdctl_config['download_cpdctl']):
            # This code will allow to download from internet
            PLATFORM = platform.system().lower()
            CPDCTL_ARCH = "{}_amd64".format(PLATFORM)
            CPDCTL_RELEASES_URL="https://api.github.com/repos/IBM/cpdctl/releases"
            CWD = os.getcwd()
            PATH = os.environ['PATH']
            CPD_CONFIG = os.path.join(CWD, '.cpdctl.config.yml')

            response = requests.get(CPDCTL_RELEASES_URL)
            assets = response.json()[0]['assets']
            platform_asset = next(a for a in assets if CPDCTL_ARCH in a['name'])
            cpdctl_url = platform_asset['url']
            cpdctl_file_name = platform_asset['name']

            response = requests.get(cpdctl_url, headers={'Accept': 'application/octet-stream'})
            with open(cpdctl_file_name, 'wb') as f:
                f.write(response.content)
        else:
            # if file exists
            cpdctl_file_name = cpdctl_config['cpdctl_filepath']

        CWD = os.getcwd()
        PATH = os.environ['PATH']
        CPD_CONFIG = os.path.join(CWD, '.cpdctl.config.yaml')

        os.environ['PATH'] = f"{CWD}:{PATH}"
        os.environ['CPD_CONFIG'] = CPD_CONFIG

        if cpdctl_file_name.endswith('tar.gz'):
            with tarfile.open(cpdctl_file_name, "r:gz") as tar:
                tar.extractall()
        elif cpdctl_file_name.endswith('zip'):
            with zipfile.ZipFile(cpdctl_file_name, 'r') as zf:
                zf.extractall()

        if CPD_CONFIG and os.path.exists(CPD_CONFIG):
            os.remove(CPD_CONFIG)
   
def user_login(wml_credentials):
    """
    user_login takes credentials and attempts to login the user into the a Cloud Pak for Data instance, will verify by checking if the user can search for deployments,
    (user can have no deployment spaces and will still be able to authenticate user). Will exit if incorrect information provided or user not able to authenticated. All
    following functions in cpdctl_api will require user to be authenticated, must be first step in order to use any other function.

    Inputs:
        wml_credientials (dictionary): dictionary that need to contain the following key-value pairs:  
            {
                username: username for Cloud Pak for Data user
                password: password for Cloud Pak for Data user
                url: url to Cloud Pak for Data Cluster/Cloud
            }

            OR

            {
                apikey: apikey for Cloud Pak for Data user
                region: region that Cloud Park for Data Cloud is hosted on
                url: url to Cloud Pak for Data Cluster/Cloud
            }
    """
    # Unset any previous user to avoid confusion of users
    subprocess.run(["cpdctl", "config", "profile", "unset", "cpd"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # define user
    user = wml_credentials.get('username')

    # check if using password to login
    if(wml_credentials.get('password')):
        user_pass = wml_credentials['password']
        subprocess.run(["cpdctl", "config", "user", "set", "cpd_pass", "--username", user, "--password", user_pass], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(["cpdctl", "config", "profile", "set", "cpd", "--url", wml_credentials['url'], "--user", "cpd_pass"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(["cpdctl", "config", "profile", "use", "cpd"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # check if using apikey to login
    elif(wml_credentials.get('apikey')):
        user_api = wml_credentials['apikey']
        print("user: " + user)
        print("using api key: " + user_api)
        # user_region = wml_credentials['region']
        subprocess.run(["cpdctl", "config", "user", "set", "cpd_api", "--username", user, "--apikey", user_api], capture_output=True, text=True).stdout
        subprocess.run(["cpdctl", "config", "profile", "set", "cpd", "--url", wml_credentials['url'], "--user", "cpd_api"], capture_output=True, text=True).stdout
        subprocess.run(["cpdctl", "config", "profile", "use", "cpd"], capture_output=True, text=True).stdout

    # check if using token to login
    elif(wml_credentials.get('token')):
        # currently not supported
        pass
    else:
        print("User login info incorrectly provided")
        exit()

    
    # try to search for spaces to verify user has been correctly authenticated
    try:
        auth_verify = subprocess.run(["cpdctl", "space", "list", "--output", "yaml"], capture_output=True, text=True).stdout
        #print("output from cpdctl: " + auth_verify)
        auth_verify = yaml.safe_load(auth_verify)
        #print("output after yaml: " + auth_verify)
        # print(auth_verify)
        verify = auth_verify['first']
        print("User authenticated successfully")
    except:
        print("Error: User authentication failed, check credentials or CPD url")
        exit()
    

def verify_user_deployment_access(space_id):
    """
    verify_user_deployment_access checks if the currently authenticated user has access to the deployment space provided. Will exit if space_id is invalid, or if
    user doesn't have access to the space

    Input:
        space_id (string): The ID of the space to use
    """
    # this function will verify if a user has access to a deployment space
    try:
        space_verify = subprocess.run(["cpdctl", "space", "get", "--space-id", space_id, "--output", "yaml"], capture_output=True, text=True).stdout
        space_verify = yaml.safe_load(space_verify)
        verify = space_verify["entity"]["name"]
    except:
        print("Error: User doesn't have permission to the deployment space, contact Deployment Space owner for permissions")
        exit()

def verify_user_project_access(project_id):
    """
    verify_user_project_access checks if the currently authenticated user has access to the project space provided. Will exit if project_id is invalid, or if
    user doesn't have access to the project

    Input:
        project_id (string): The ID of the project to use
    """
    try:
        project_verify = subprocess.run(["cpdctl", "project", "get", "--project-id", project_id, "--output", "yaml"], capture_output=True, text=True).stdout
        project_verify = yaml.safe_load(project_verify)
        verify = project_verify["entity"]["name"]
    except:
        print("Error: User doesn't have permission to the project space, contact Project Space owner for editor permissions")
        exit()

def search_asset(asset_type, file_name, space_id, space_type):
    """
    search_asset will try and return the asset_id from the file name in a given deployment or project space, will return either None or the asset_id of 
    the first asset that matches the file name

    Usage: Deployment or Project Space
    
    Input:
        asset_type (string): Either notebook, code_package or shiny_asset
        file_name (string): File Name for the asset to search on Cloud Pak for Data
        space_id (string): The ID of the project or deployment space to use
        space_type (string): Either deployment or project
    """
    space_command = get_space_command(space_type)

    # Search if asset with same name exits in Deployment Space
    asset_id = subprocess.run(["cpdctl", "asset", "search", "--type-name", asset_type, "--query", file_name, space_command, space_id,
                                        "--output", "yaml", "-j", "results[0].metadata.asset_id", "--raw-output"], 
                                        capture_output=True, text=True).stdout
    asset_id = yaml.safe_load(asset_id)


    # Will return either None or the asset_id  
    return asset_id

def search_asset_metadata(asset_type, file_name, space_id, space_type):
    """
    search_asset_metadata will try and return the metadata from the file name in a given deployment or project space, will return either None or the metadata 
    of the first asset that matches the file name

    Usage: Deployment or Project Space
    
    Input:
        asset_type (string): Either notebook, code_package or shiny_asset
        file_name (string): File Name for the asset to search on Cloud Pak for Data
        space_id (string): The ID of the project or deployment space to use
        space_type (string): Either deployment or project
    """
    space_command = get_space_command(space_type)

    # Search if asset with same name exits in Deployment Space
    output = subprocess.run(["cpdctl", "asset", "search", "--type-name", asset_type, "--query", file_name, space_command, space_id,
                                        "--output", "yaml", "--raw-output"], 
                                        capture_output=True, text=True).stdout
    output = yaml.safe_load(output)

    # Will return either None or the asset_metadata  
    if(output['total_rows'] == 0):
        return None
    else:
        metadata = (output['results'][0]['metadata'])
        return metadata

def upload_asset(local_file_path: str, remote_file_path: str, commands, space_id:str , space_type):
    """
    upload_asset will add the file data to the cloud object storage from local directory, this wont create the asset on CP4D, but you need to
    run this step before we can create any asset in a deployment or project space.

    Usage: Deployment or Project Space

    Input:
        local_file_path (string): Path to the file that you want to upload to CP4D
        remote_file_path (string): Path for cloud pak for data, usually follow structure {asset_type}/{filename}
        commands (list): List of commands needed to upload the file (will vary depending on asset type, see respetive functions)
        space_id (string): The ID of the project or deployment space to use
        space_type (string): Either deployment or project
    """
    print("\n-- Start to upload asset to: ", remote_file_path)

    space_command = get_space_command(space_type)

    # Remote file location of asset will be stored under the asset directory
    subprocess.run(["cpdctl", "asset", "file", "upload", "--path", remote_file_path, "--file", local_file_path, space_command, space_id], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)    

    asset_id = subprocess.run(commands, capture_output=True, text=True).stdout

    # asset_id = asset_id.removesuffix("\n") #python 3.9+
    asset_id = remove_suffix(asset_id, "\n")  # python 3.4+
            
    return asset_id

def upload_notebook(local_file_path: str, notebook_name: str, env_id: str, update_file: bool, space_id: str, space_type):
    """
    upload_notebook will create a notebook asset in either a deployment or project space on CP4D

    Usage: Deployment or Project Space

    Input: 
        local_file_path (string): Path to the file that you want to upload to CP4D
        notebook_name (string): Name for file on CP4D, doesn't have to be the same as local file name
        env_id (string): CP4D enviorment that the notebook will use to run
        update_file (boolean): If set to true, will create a new version of the file
        space_id (string): The ID of the project or deployment space to use
        space_type (string): Either deployment or project
    """
    print("\n-- Start to upload notebook: ", notebook_name)

    space_command = get_space_command(space_type)

    file_name = notebook_name + ".ipynb"
    remote_file_path = "notebook/" + file_name

    notebook_id = search_asset("notebook", file_name, space_id, space_type)

    if(notebook_id != None):
        # Create a new version of the notebook, if there already exists a notebook
        if(update_file):
            subprocess.run(["cpdctl","asset", "file", "upload", "--path", remote_file_path, "--file", local_file_path, "--space-id", space_id])
            subprocess.run(["cpdctl", "notebook", "version", "create", "--notebook-id", notebook_id])
            
            print("Notebook [{}] successfully updated on cp4d".format(file_name))
            
        else:
            
            print("File exists on CP4D, to update file change yaml ")
            print("configuration: deployment_info -> force_2_update")
            
            exit()


    else:
        # Notebooks requires a runtime, which specifys the enviroment
        runtime = {'environment': env_id}
        runtime_json = json.dumps(runtime)

        commands = ["cpdctl", "notebook", "create", "--file-reference", remote_file_path, "--name", file_name, 
                    space_command, space_id, "--runtime", runtime_json, "--output", "json", "-j", "metadata.asset_id", "--raw-output"]
        notebook_id = upload_asset(local_file_path, remote_file_path, commands, space_id, space_type)
        
        print("Notebook [{}] successfully uploaded to cp4d".format(file_name))
        print("with asset id [{}].".format(notebook_id))

def upload_code_package(local_file_path: str, code_pkg_name: str, update_file: bool, space_id: str, space_type):
    """
    upload_code_package will create a code package asset in either a deployment or project space on CP4D

    Usage: Deployment or Project Space

    Input: 
        local_file_path (string): Path to the file that you want to upload to CP4D
        code_pkg_name (string): Name for file on CP4D, doesn't have to be the same as local file name
        update_file (boolean): If set to true, will create a new version of the file
        space_id (string): The ID of the project or deployment space to use
        space_type (string): Either deployment or project
    """
    print("\n-- Start to upload code package: ", code_pkg_name)

    space_command = get_space_command(space_type)
 
    file_name = code_pkg_name + ".zip"
    remote_file_path = "code_package/" + file_name

    code_pkg_id = search_asset("code_package", file_name, space_id, space_type)
    if(code_pkg_id == None):
        commands = ["cpdctl", "code-package", "create", "--file-reference", remote_file_path, "--name", file_name, space_command, space_id, "--output", "json", "-j", "asset_id", "--raw-output"]
        
        if(update_file):
            code_pkg_id =  upload_asset(local_file_path, remote_file_path, commands, space_id, space_type)
            
            print("Code Package [{}] successfully uploaded to cp4d".format(file_name))
            print("with asset id [{}].".format(code_pkg_id))
            
        else:
            
            print("File exists on CP4D, to update file change yaml ")
            print("configuration: deployment_info -> force_2_update")
            
            exit()
    else:
        # For code pacakges, we can only update the file reference for now, unfortunately it won't show that the file is updated via GUI on CP4D Platform 
        subprocess.run(["cpdctl", "asset", "file", "upload", "--path", remote_file_path, "--file", local_file_path, space_command, space_id], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)    

        
        print("Code Package [{}] successfully updated on cp4d".format(file_name))
        
def upload_rshiny_asset(local_file_path: str, shiny_asset_name: str, space_id: str, ):
    print("\n-- Start to upload RShiny code package: ", shiny_asset_name)

    remote_file_path = "shiny_asset/" + shiny_asset_name
    local_file_path = local_file_path

    # search if existing asset is there with same name
    shiny_asset_id = search_asset("shiny_asset", shiny_asset_name, space_id, "deployment")
    if (shiny_asset_id != None):
        print("Found existing assets with name code package name:",shiny_asset_id)
        subprocess.run(["cpdctl", "asset", "delete", "--asset-id", shiny_asset_id, "--space-id", space_id],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(shiny_asset_id, "has been deleted")

    subprocess.run(
        ["cpdctl", "asset", "file", "upload", "--path", remote_file_path, "--file", local_file_path, "--space-id",
         space_id],
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    metadata = {
        "name": shiny_asset_name,
        "asset_type": "shiny_asset",
        "asset_category": "USER",
        "origin_country": "au"
    }
    metadata_json = json.dumps(metadata)

    entity = {
        "shiny_asset": {
            "software_spec": {
                "base_id": "7fbf1305-59a7-5b77-b881-1416ce2ee903"
            }
        }
    }

    entity_json = json.dumps(entity)

    attachments = [
        {
            "asset_type": "shiny_asset",
            "name": shiny_asset_name,
            "description": "attachment for shiny asset",
            "mime": "application/text",
            "object_key": remote_file_path
        }
    ]
    attachments_json = json.dumps(attachments)

    result = subprocess.run(
        ["cpdctl", "asset", "create", "--metadata", metadata_json, "--entity", entity_json, "--attachments",
         attachments_json, "--space-id", space_id, "--output", "yaml", "-j", "metadata.asset_id", "--raw-output"],
        capture_output=True, text=True).stdout

    rshiny_asset_id = yaml.safe_load(result)

    
    print("Shinny App Package [{}] successfully uploaded on cp4d".format(shiny_asset_name))
    

    return rshiny_asset_id

def search_job(space_id: str, job_name: str, space_type):
    # here we search if a job exists
    space_command = get_space_command(space_type)

    # Get a list of jobs that currently exist in the deployment space  
    total_jobs = subprocess.run(["cpdctl", "job", "list", space_command, space_id, "--output", "yaml", "-j", "results[:].metadata.name", "--raw-output"], 
                                    capture_output=True, text=True).stdout
    jobs_list = yaml.safe_load(total_jobs)

    # Loop throught the list, and see if any current job exists with job_name (The new job we want to create), if job exits, we will update
    # new job index to point to existing job otherwise it will stay as -1
    new_job_index = -1
    if(jobs_list != None):
        for i in range(0, len(jobs_list)):
            job = jobs_list[i]
            if job == job_name:
                new_job_index = i

    # If job is found, we will delete that existing job, as that job points to the previous version of the file.        
    if(new_job_index != -1):
        # Based on the previous search, we find the job id of the exisiting job.
        job_id_list = subprocess.run(["cpdctl", "job", "list", space_command, space_id, "--output", "yaml", "-j", "results[:].metadata.asset_id", "--raw-output"], 
                                    capture_output=True, text=True).stdout
        job_id_list = yaml.safe_load(job_id_list)    
        job_id = job_id_list[new_job_index]
        return job_id
    else:
        return None

def create_job(job_name, job_json, asset_id, space_id: str, space_type):
    space_command = get_space_command(space_type)

    job_id = search_job(space_id, job_name, space_type)


    if(job_id == None):
        job_id = subprocess.run(["cpdctl", "job", "create", "--job", job_json, space_command, space_id, "--output", "json", "-j", 
                                    "metadata.asset_id", "--raw-output"], 
                                    capture_output=True, text=True).stdout

        # job_id = job_id.removesuffix("\n") #python 3.9+
        job_id = remove_suffix(job_id, "\n")  # python 3.4+
        
    return job_id
    
def create_notebook_job(notebook_id, env_id, deployment_info, space_id: str, space_type):
    job_name = deployment_info["code_pkg_name"] + "_job"
    if(deployment_info.get('job_name')):
        job_name = deployment_info["job_name"]

    # here we have to serach if there is already a job, because we are now creating a revision, there wont be a need to delete the job
    # and if an existing job is found, maybe we can check if we need to update any variables, otherwise we can just say that there is an 
    # existing job (maybe give the option to override an old job, potential YAML setting)


    # Job Configuration Data
    job = {
        'asset_ref': notebook_id, 
        'configuration': {
            'env_id': env_id, 
            'env_variables':deployment_info['job_configuration_variables']
        }, 
        'description': 'my job', 
        'name': job_name
    }
    job_json = json.dumps(job)
 
    job_id = create_job(job_name, job_json, notebook_id, space_id, space_type)
    
    print("Job [{}] created successfully".format(job_name))
    print("with job id [{}].".format(job_id))
    
    return job_id

def create_codepackage_job(code_package_id, env_id, deployment_info, entrypoint, space_id: str, space_type):
    job_name = deployment_info["code_pkg_name"] + "_job"
    if(deployment_info.get('job_name')):
        job_name = deployment_info["job_name"]

    # Job Configuration Data
    job = {
        'asset_ref': code_package_id, 
        'configuration': {
            'env_id': env_id, 
            'env_variables': deployment_info['job_configuration_variables'],
            'entrypoint': entrypoint,
        }, 
        'description': 'my code package job', 
        'name': job_name,
    }

    job_json = json.dumps(job)
    
    job_id = create_job(job_name, job_json, code_package_id, space_id, space_type)
    
    print("Job [{}] created successfully".format(job_name))
    print("with job id [{}].".format(job_id))
    
    return job_id
    
def search_hardware_spec( hardware_spec, space_id):
    hardware_spec_list = subprocess.run(["cpdctl", "environment", "hardware-specification" ,"list", "--space-id", space_id, 
                                        "--output", "yaml", "-j", "resources[:].metadata", "--raw-output"], 
                                    capture_output=True, text=True).stdout
   
    hardware_spec_list = yaml.safe_load(hardware_spec_list)
    for spec in hardware_spec_list:
        if spec['name'] == hardware_spec:
            return spec['asset_id']

    return None

def search_r_shiny_app(serving_name, space_id):
    asset_id = subprocess.run(["cpdctl", "ml", "deployment", "list", "--space-id", space_id, "--serving-name", serving_name,
                                "--output", "json", "-j", "resources[0].metadata.id", "--raw-output"], 
                                    capture_output=True, text=True).stdout
    asset_id = yaml.safe_load(asset_id) 

    return asset_id

def create_r_shiny_app(deployment_info, rshiny_asset_id, space_id):
    asset = {
        "id": rshiny_asset_id
    }
    asset_json = json.dumps(asset)    


    # create hardware spec json
    hardware_spec = deployment_info['hardware_spec']
    hardware_spec_id = search_hardware_spec(hardware_spec, space_id)

    if(hardware_spec_id != None):
        hardware_spec_details = {
            "id" : hardware_spec_id,
            "rev" : 'latest',
            "name" : hardware_spec,
            "num_nodes" : 1
        }
        hardware_spec_details_json = json.dumps(hardware_spec_details)
    else:
        print("error in getting hardware spec")

    # create rshiny json
    if(deployment_info.get('rshiny_app_serving_name')):
        rshiny_app_serving_name = deployment_info["rshiny_app_serving_name"]
    else:
        rshiny_app_serving_name = deployment_info["code_pkg_name"] + "_app"

    print("\n-- Start to create RShiny App: ",rshiny_app_serving_name)

    # check if rshiny app exists with same serving name
    asset_id = search_r_shiny_app(rshiny_app_serving_name, space_id)
    if(asset_id == None):
        pass
    else:
        print("Found existing deployed RShiny App with same name",asset_id)
        subprocess.run(["cpdctl", "ml", "deployment","delete", "--deployment-id", asset_id, "--space-id", space_id], 
                        capture_output=True, text=True).stdout

        # sleep 10s and wait for deletion.
        import time
        # Sleep for 10 seconds
        time.sleep(10)
        print(asset_id, "has been deleted",)

    rshiny_details = {
        "authentication" : deployment_info['authentication'],
        "parameters" : {
            "serving_name": rshiny_app_serving_name,
        }
    }
    rshiny_details_json = json.dumps(rshiny_details)

    subprocess.Popen(["cpdctl", "ml", "deployment", "create", "--space-id", space_id, "--name", rshiny_app_serving_name, "--asset", asset_json,
                    "--r-shiny", rshiny_details_json, "--hardware-spec", hardware_spec_details_json])

    print(rshiny_app_serving_name, "has been submitted for deployment.")
    print("You may need to wait 1-10 minutes before it is active.")

def run_job(deployment_info, job_id, env_id, space_id: str, space_type):
    space_command = get_space_command(space_type)

    job_name = deployment_info["code_pkg_name"] + "_job"
    if (deployment_info.get('job_name')):
        job_name = deployment_info["job_name"]
 
    job_run = {
                'configuration': {
                    'env_id' : env_id,
                    'env_variables': deployment_info['environment_configuration_variables']
                }
            }   
    job_run_json = json.dumps(job_run)

    # subprocess.run(["cpdctl", "job", "run", "create", "--space-id", space_id,
    #                   "--job-id", job_id, "--job-run", job_run_json], capture_output=False)

    # no waiting
    subprocess.Popen(["cpdctl", "job", "run", "create", space_command, space_id,
                    "--job-id", job_id, "--job-run", job_run_json])

    print("Job [{}] submitted to run with job id [{}].".format(job_name, job_id))

def get_date_str():
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    return date_str