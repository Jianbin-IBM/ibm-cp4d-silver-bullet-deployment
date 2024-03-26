import subprocess
import argparse
import yaml
import ast
import os
from cpdctl_api import remove_suffix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Code Packages')

    parser.add_argument('--yaml_file', '-y', type=str,
                        default='configuration_template_R.yaml')

    args = parser.parse_args()
    yaml_file = args.yaml_file

    # Read YAML file
    print('-- Loading configuration yaml file:',yaml_file)
    with open(yaml_file, 'r') as stream:
        configuration = yaml.safe_load(stream)

    # Variables from the YAML file
    wml_credentials = configuration['wml_credentials']
    # cpdctl_config = configuration['cpdctl_config']
    prj_info = configuration['prj_info']
    deployment_info = configuration['deployment_info']

    if "email_setting" in configuration:
        email_setting = configuration['email_setting']
        print('\n\rsend_email_when_fail: ', email_setting['send_email_when_fail'])
        print('send_email_when_successful: ', email_setting['send_email_when_successful'])
    else:
        email_setting = []
        print('\n\rEmail not enabled')

    # Job variables
    environment_name = deployment_info['runtime']

    # Email variables
    sender = email_setting['sender']
    receivers = email_setting['receivers']
    smtp_server = email_setting['smtp_server']

    # this is the file that is to be uploaded
    local_file = prj_info['main_file']


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
        space_command = "--space-id"
        from cpdctl_api import verify_user_deployment_access
        verify_user_deployment_access(space_id)
    elif(deployment_info.get('project_id')):
        space_type = "project"
        space_id = deployment_info['project_id']
        space_command = "--project-id"
        from cpdctl_api import verify_user_project_access
        verify_user_project_access(space_id)
    else:
        print("Space id or Project id missing, please update yaml file")
               
        exit()


    # DEFINING THE ENVIORMENT SPACE
    query_string = "(resources[?entity.environment.display_name == '{}'].metadata.asset_id)[0]".format(environment_name)
    env_id = subprocess.run(["cpdctl", "environment", "list", space_command, space_id, "--output", "json", "-j", query_string, "--raw-output"],
                            capture_output=True, text=True).stdout
    # env_id = env_id.removesuffix("\n") #python 3.9+
    env_id = remove_suffix(env_id, "\n")  # python 3.4+

    if(env_id == 'null'):
        
        print("Incorrect Enviorment Name in yaml file, to get a list ")
        print("of enviroment names on CP4D: ")
        print("Deployment Space -> Manage -> Enviorments -> Templates")
        
        exit()

    if local_file.endswith(".ipynb"):
        from cpdctl_api import search_asset
        notebook_name = deployment_info['code_pkg_name'] + ".ipynb"
        notebook_id = search_asset("notebook", notebook_name ,space_id, space_type)

        from cpdctl_api import create_notebook_job
        job_id = create_notebook_job(notebook_id, env_id, deployment_info, space_id, space_type)

        # Step 4: Run a test job (Optional)
        from cpdctl_api import run_job
        run_job(deployment_info, job_id, env_id, space_id, space_type)
    elif local_file.endswith(".R"):
        if prj_info["r_shiny_app"]:
            from cpdctl_api import search_asset, create_r_shiny_app
            rshiny_name =  deployment_info['code_pkg_name']
            shiny_asset_id = search_asset("shiny_asset", rshiny_name, space_id, space_type)
            
            create_r_shiny_app(deployment_info, shiny_asset_id, space_id)
        else:        
            entrypoint = "/" + prj_info['main_file']

            from cpdctl_api import search_asset
            code_pkg_filename = deployment_info['code_pkg_name'] + ".zip"
            code_pkg_id = search_asset("code_package", code_pkg_filename ,space_id, space_type)

            from cpdctl_api import create_codepackage_job
            job_id = create_codepackage_job(code_pkg_id, env_id, deployment_info, entrypoint, space_id, space_type)

            # Step 4: Run job
            from cpdctl_api import run_job
            run_job(deployment_info, job_id, env_id, space_id, space_type)
    else:
        print("File type not supported. ")  
