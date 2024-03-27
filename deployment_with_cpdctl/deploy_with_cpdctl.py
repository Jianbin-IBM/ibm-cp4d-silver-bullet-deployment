import subprocess
import argparse
import yaml
import os
import shutil
from cpdctl_api import remove_suffix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy Code Packages')

    parser.add_argument('--yaml_file', '-y', type=str,
                        default='configuration_template_python.yaml')

    args = parser.parse_args()
    yaml_file = args.yaml_file
    
    # Read YAML file
    print('\n-- Loading configuration yaml file:',yaml_file)
    with open(yaml_file, 'r') as stream:
        configuration = yaml.safe_load(stream)

    # Variables from the YAML file
    wml_credentials = configuration['wml_credentials']
    # cpdctl_config = configuration['cpdctl_config']
    prj_info = configuration['prj_info']
    deployment_info = configuration['deployment_info']

    if "email_setting" in configuration:
        email_setting = configuration['email_setting']
        #print('\n\rsend_email_when_fail: ', email_setting['send_email_when_fail'])
        #print('send_email_when_successful: ', email_setting['send_email_when_successful'])
    else:
        email_setting = []
        #print('\n\rEmail not enabled')

    # Job variables
    environment_name = deployment_info['runtime']

    # Email variables
    sender = email_setting['sender']
    receivers = email_setting['receivers']
    smtp_server = email_setting['smtp_server']

    # this is the file that is to be uploaded
    main_file = prj_info['main_file']

    """
    # Step 0: Ensure that cpdctl is correctly installed
    from cpdctl_api import install_cpdctl
    install_cpdctl(cpdctl_config)
    """
        
    # Step 1: Login User
    from cpdctl_api import user_login
    user_login(wml_credentials)

    # determine which space to be in
    if(deployment_info.get('space_id')):
        space_type = "deployment"
        space_id = deployment_info['space_id']
        from cpdctl_api import verify_user_deployment_access
        verify_user_deployment_access(space_id)
    elif(deployment_info.get('project_id')):
        space_type = "project"
        space_id = deployment_info['project_id']
        from cpdctl_api import verify_user_project_access
        verify_user_project_access(space_id)
    else:
        print("Space id or Project id missing, please update yaml file")
               
        exit()

    subprocess.run(["export", "cpdctl=./cpdctl"], capture_output=True, text=True).stdout

    # DEFINING THE ENVIORMENT SPACE
    query_string = "(resources[?entity.environment.display_name == '{}'].metadata.asset_id)[0]".format(environment_name)
    env_id = subprocess.run(["cpdctl", "environment", "list", "--space-id", space_id, "--output", "json", "-j", query_string, "--raw-output"],
                            capture_output=True, text=True).stdout
    # env_id = env_id.removesuffix("\n") #python 3.9+
    env_id = remove_suffix(env_id, "\n")  # python 3.4+

    if(env_id == 'null'):
        
        print("Incorrect Enviorment Name in yaml file, to get a list ")
        print("of enviroment names on CP4D: ")
        print("Deployment Space -> Manage -> Enviorments -> Templates")
               
        exit()

    # we will have 2 different cases for now, one for notebook, one for zip file
    if main_file.endswith(".ipynb"):
        # Step 2: Uploading the asset to CP4D
        from cpdctl_api import upload_notebook
        local_file_path = prj_info["code_dir"] + "/" + main_file
        notebook_id = upload_notebook(local_file_path, deployment_info["code_pkg_name"], env_id, deployment_info["force_2_update"], space_id, space_type)

    elif main_file.endswith(".py"):
        # modified by JB
        enable_email_sending_flag =  True
        if not enable_email_sending_flag:
            entrypoint = "/" + prj_info['main_file']
        else:
            # This is to enable sending email with wrapper.py
            # step 1: copy wrapper.py to prj_info["code_dir"]
            import shutil
            shutil.copyfile('wrapper.py',os.path.join(prj_info['code_dir'],'wrapper.py') )

            # step 2: create dummy_example.yaml in prj_info["code_dir"]
            dummy = {}
            # move url to deployment info for easier implementation
            deployment_info['url'] = wml_credentials['url']
            dummy['deployment_info'] = deployment_info
            dummy['prj_info'] = prj_info
            dummy['email_setting'] = email_setting
            # Save the dictionary to a YAML file
            with open(os.path.join(prj_info['code_dir'],'dummy.yaml'), 'w') as file:
                yaml.dump(dummy, file)

            entrypoint = "/wrapper.py"

        from cpdctl_api import upload_code_package
        shutil.make_archive(deployment_info["code_pkg_name"], 'zip', prj_info["code_dir"])
        local_zip_file = deployment_info["code_pkg_name"] + ".zip"

        # Step 2: Uploading the asset to CP4D
        code_package_id = upload_code_package(local_zip_file, deployment_info["code_pkg_name"],
                                       deployment_info["force_2_update"], space_id, space_type)
        os.remove(local_zip_file)

    else:
        print("Error: Does not support file type: ", main_file)
