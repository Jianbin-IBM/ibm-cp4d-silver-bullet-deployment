import subprocess
import argparse
import yaml
import os
import shutil
from cpdctl_api import remove_suffix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy Code Packages')

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
        # print('\nsend_email_when_fail: ', email_setting['send_email_when_fail'])
        # print('send_email_when_successful: ', email_setting['send_email_when_successful'])
    else:
        email_setting = []
        # print('\nEmail not enabled')

    # Job variables
    environment_name = deployment_info['runtime']

    # Email variables
    sender = email_setting['sender']
    receivers = email_setting['receivers']
    smtp_server = email_setting['smtp_server']

    # determine which space to be in
    if(deployment_info.get('space_id')):
        space_type = "deployment"
        space_id = deployment_info['space_id']
    elif(deployment_info.get('project_id')):
        space_type = "project"
        space_id = deployment_info['project_id']
    else:
        print("Space id or Project id missing, please update yaml file")
        exit()

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


    # DEFINING THE ENVIORMENT SPACE
    query_string = "(resources[?entity.environment.display_name == '{}'].metadata.asset_id)[0]".format(environment_name)
    env_id = subprocess.run(["cpdctl", "environment", "list", "--space-id", space_id, "--output", "json", "-j", query_string, "--raw-output"],
                            capture_output=True, text=True).stdout
    # env_id = env_id.removesuffix("\n") #python 3.9+
    env_id = remove_suffix(env_id, "\n")  # python 3.4+

    if(env_id == 'null'):
        print("Error: Incorrect Enviorment Name in yaml file, to get a list ")
        print("of enviroment names on CP4D: ")
        print("Deployment Space -> Manage -> Enviorments -> Templates")
        exit()

    # entrypoint = "/" + prj_info['main_file']
    
    # check if the directory provided is valid
    if(not os.path.isdir(prj_info['code_dir'])):
        print("Error: Incorrect Code Directory, update prj_info: main_file")
        exit()

    main_file = prj_info['main_file']
    main_file_path = prj_info["code_dir"] + "/" + main_file

    if main_file.endswith(".ipynb"):
        # Step 2: Uploading the asset to CP4D
        from cpdctl_api import upload_notebook

        notebook_id = upload_notebook(main_file_path, deployment_info["code_pkg_name"], env_id,
                                      deployment_info["force_2_update"], space_id, space_type)
    elif main_file.endswith(".R"):
        shutil.make_archive(deployment_info["code_pkg_name"], 'zip', prj_info["code_dir"])
        code_pkg_zip = deployment_info["code_pkg_name"] + ".zip"
        if prj_info["r_shiny_app"]:
            from cpdctl_api import upload_rshiny_asset, search_asset, create_r_shiny_app, search_r_shiny_app

            # if main_file is not app.R, force copy to app.R
            if main_file != 'app.R':
                print('app.R is not found, copy', main_file, 'to be app.R')
                os.remove(prj_info["code_dir"] + "/app.R")
                subprocess.run(["cp", "-f", main_file_path, prj_info["code_dir"] + "/app.R"], stdout=subprocess.DEVNULL,
                               stderr=subprocess.STDOUT)

            # need to delete deployment before delete assets
            if (deployment_info.get('rshiny_app_serving_name')):
                rshiny_app_serving_name = deployment_info["rshiny_app_serving_name"]
            else:
                rshiny_app_serving_name = deployment_info["code_pkg_name"] + "_app"

            print("\n-- Check if RShiny App exists: ", rshiny_app_serving_name)

            # check if rshiny app exists with same serving name
            asset_id = search_r_shiny_app(rshiny_app_serving_name, space_id)
            if (asset_id == None):
                pass
            else:
                print("Found existing deployed RShiny App with same name", asset_id)
                subprocess.run(
                    ["cpdctl", "ml", "deployment", "delete", "--deployment-id", asset_id, "--space-id", space_id],
                    capture_output=True, text=True).stdout

                # sleep 10s and wait for deletion.
                import time

                # Sleep for 10 seconds
                time.sleep(10)
                print(asset_id, "has been deleted")

            # uppload rshiny code package
            shiny_asset_id = upload_rshiny_asset(code_pkg_zip, deployment_info["code_pkg_name"], space_id)

            # if main_file is not app.R, delete app.R
            if main_file != 'app.R':
                os.remove(prj_info["code_dir"] + "/app.R")
                print('app.R has been removed')

            # deploy app
            rshiny_name = deployment_info['code_pkg_name']
            shiny_asset_id = search_asset("shiny_asset", rshiny_name, space_id, space_type)
            create_r_shiny_app(deployment_info, shiny_asset_id, space_id)
        else:
            # Step 2: Uploading the asset to CP4D
            from cpdctl_api import upload_code_package

            code_package_id = upload_code_package(code_pkg_zip, deployment_info["code_pkg_name"],
                                                  deployment_info["force_2_update"], space_id, space_type)
        os.remove(code_pkg_zip)
    else:
        print("Error: Does not support file type: ", main_file)
