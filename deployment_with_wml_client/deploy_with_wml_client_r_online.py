# for those using older ibm_watson_machine_learning version, please update use below code
import subprocess
# output = subprocess.run(["pip3", "install", "ibm-watson-machine-learning", "--upgrade"], capture_output=True, text=True).stdout
# print(output)

import argparse
import yaml
import ast

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy Code Packages')

    parser.add_argument('--yaml_file', '-y', type=str,
                        default='cpd471_prod_online_r_randy.yaml')

    parser.add_argument(
        '--test_run', '-t',
        default = 'True',
        help='True or False flag, input should be either "True" or "False".',
        type=ast.literal_eval,
        dest='test_run'
    )
    args = parser.parse_args()

    yaml_file = args.yaml_file
    test_run = args.test_run

    # Read YAML file
    print('\n-- Loading configuration yaml file:',yaml_file)
    with open(yaml_file, 'r') as stream:
        configuration = yaml.safe_load(stream)

    # print(configuration)

    wml_credentials = configuration['wml_credentials']
    deployment_info = configuration['deployment_info']
    prj_info = configuration['prj_info']
    if "email_setting" in configuration:
        email_setting = configuration['email_setting']
        #print('\n\rsend_email_when_fail: ',email_setting['send_email_when_fail'])
        #print('send_email_when_successful: ', email_setting['send_email_when_successful'])
    else:
        email_setting = []
        #print('\n\rEmail not enabled')


    print('\n\rCode Package to be deployed:')
    print(prj_info,'\n\r')

    # step 1: login to wml
    from wml_client_api import wml_login
    wml_client = wml_login(wml_credentials)

    space_id = deployment_info['space_id']
    wml_client.set.default_space(space_id)
    print("\n\rSet space id successfully:", space_id)

    # install_r_pkgs.py is need to install R libraries
    import shutil,os
    shutil.copyfile('install_r_pkgs.py', os.path.join(prj_info['code_dir'], 'install_r_pkgs.py'))

    # From cpd 4.x, deployment function can get the token inside. Hence we don't need password as parameters anymore.
    if "version" in wml_credentials:
        version = wml_credentials['version']
        if version[0]>'3':
            # remove credentials to avoid disclosure of the password.
            if "password" in wml_credentials:
                del wml_credentials['password']

    # This is a generator code needed by CP4D to run your code. In most cases, you don't have to modify it.
    def my_deployable_function(wml_credentials=wml_credentials, deployment_info=deployment_info, prj_info=prj_info,
                               email_setting=email_setting):

        import os
        import subprocess
        import requests, json
        import shutil
        from urllib3.exceptions import InsecureRequestWarning

        def get_user_token(url, username, password):
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            payload = {"username": username, "password": password}
            body = json.dumps(payload)
            h = {"cache-control": "no-cache", "content-type": "application/json"}
            # r = (requests.post(url + "/icp4d-api/v1/authorize", data=body, headers=h, verify=False)).json()
            r = (requests.post(url + "/icp4d-api/v1/authorize", data=body, headers=h, verify=False))
            # print('r=', r.json())

            if r.ok:
                headers = {"Authorization": "Bearer " + r.json()['token']}
                return True, headers, ""
            else:
                return False, None, r.text

        # for those using older ibm_watson_machine_learning version, please update use below code
        # output = subprocess.run(["pip3", "install", "ibm-watson-machine-learning", "--upgrade"], capture_output=True,
        #                         text=True).stdout
        # print(output)

        # get USER_ACCESS_TOKEN directly without leaking token, username and password in the deployment function
        if "version" in wml_credentials:
            version = wml_credentials['version']
            if version[0] > '3':
                user_token = os.environ["USER_ACCESS_TOKEN"]
                wml_credentials['token'] = user_token

        if "password" in wml_credentials:
            auth_ok, headers, error_msg = get_user_token(wml_credentials['url'],
                                                         wml_credentials['username'],
                                                         wml_credentials['password'])
            if not auth_ok:
                print("You are not authenticated yet.")
            else:
                print("You are successfully authenticated!")
        else:
                user_token = os.environ["USER_ACCESS_TOKEN"]
                headers = {"Authorization": "Bearer " + user_token}

        if email_setting:
            send_email_when_successful = email_setting['send_email_when_successful']
            send_email_when_fail = email_setting['send_email_when_fail']
            sender = email_setting['sender']
            receivers = email_setting['receivers']
            smtp_server = email_setting['smtp_server']
        else:
            send_email_when_successful = False
            send_email_when_fail = False

        from ibm_watson_machine_learning import APIClient
        wml_client = APIClient(wml_credentials)

        space_id = deployment_info['space_id']
        wml_client.set.default_space(space_id)

        def get_assets_dict():
            assets_dict = {x["metadata"]["name"]: x["metadata"]["asset_id"] for x in
                           wml_client.data_assets.get_details()["resources"]}
            return assets_dict

        import smtplib
        def send_email(smtp_server, sender, receivers, message):
            try:
                smtpObj = smtplib.SMTP(smtp_server)
                smtpObj.sendmail(sender, receivers, message)
                print("Notification Email Sent Successfully")
            # except SMTPException:
            except:
                print("Error: unable to send email")

        def download_folder_from_volume(cpd_url, headers, sv_name: str, sv_path: str, local_file: str):
            # /zen-volumes/display_name/v1/volumes/files/target_file_path?compress=tar' -H 'Accept: application/json' -H 'Authorization: Bearer {token}'
            cpd_url = cpd_url.rstrip("/")

            requests.packages.urllib3.disable_warnings()

            url_encoded_path = sv_path.lstrip("/").replace("/", "%2F")
            #print('url_encoded_path=', url_encoded_path)

            endpoint = f"{cpd_url}/zen-volumes/{sv_name}/v1/volumes/files/{url_encoded_path}?compress=tar"
            #print('endpoint=', endpoint)

            response = requests.get(endpoint, headers=headers, verify=False)
            # The directory /myfiles/ gets created automatically by the PUT request
            if response.status_code >= 300:
                raise ValueError(f"Could not download file. rc={response.status_code} {response.text}")
            open(local_file, 'wb').write(response.content)

            print(local_file, 'downloaded from storage volume:', sv_name)

        def get_date_str():
            from datetime import datetime
            date_str = datetime.now().strftime("%Y-%m-%d")
            return date_str

        date_str = get_date_str()

        # download code tar file and then untar it
        assets_dict = get_assets_dict()
        code_pkg_name = deployment_info['code_pkg_name']
        tar_file_name = code_pkg_name + ".tar.gz"
        wml_client.data_assets.download(assets_dict[tar_file_name], tar_file_name)
        subprocess.run(["tar", "xzf", tar_file_name])

        # Define the path to the directory
        r42_env_path = "r42_env"
        # Check if the directory exists
        if os.path.exists(r42_env_path) and os.path.isdir(r42_env_path):
            # If the directory exists, do your process here
            print("The 'r42_env' folder exists. Assume Conda ENV created")
            # Perform your process here
        else:
            #### install R
            print('-- Start to install R virtual env ...')
            p = subprocess.run(
                "conda create -p r42_env r=4.2 python=3.10.10 -c https://artifactory.gcp.anz/artifactory/api/conda/conda-forge --override-channels -y".split(),
                capture_output=True, text=True)

            #### Download lib zip and unzip to R
            if "storage_volume" in prj_info and "r_lib_path" in prj_info:
                print('-- Start to Copy R libraries from Storage Volume to R env ...')
                storage_volume = prj_info['storage_volume']
                r_lib_path = prj_info['r_lib_path']
                tar_file_name = 'r_lib.tar'
                download_folder_from_volume(wml_credentials['url'], headers, storage_volume, r_lib_path, tar_file_name)
                # unzip to target folder
                p = subprocess.run(["tar", "xzf", tar_file_name, "-C", "r42_env/lib/R/library", "--strip-components=1"])

            #### copy own libs from own_r_libs to r42_env/lib/R/library
            print('-- Start to Copy R libraries from own_r_libs to R env ...')
            own_r_libs_path = "own_r_libs"
            # Check if the directory exists
            if os.path.exists(own_r_libs_path) and os.path.isdir(own_r_libs_path):
                # Source and destination directories
                source_dir = "own_r_libs"
                destination_dir = "r42_env/lib/R/library"

                # Ensure the destination directory exists
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                # Copy all files and folders from source to destination
                for item in os.listdir(source_dir):
                    source_item = os.path.join(source_dir, item)
                    destination_item = os.path.join(destination_dir, item)
                    if not os.path.exists(destination_item):
                        if os.path.isdir(source_item):
                            shutil.copytree(source_item, destination_item)
                        else:
                            shutil.copy2(source_item, destination_item)

            #### install R lib
            print('-- Start to install R libraries ...')
            p = subprocess.run("conda run -p r42_env python install_r_pkgs.py".split(), capture_output=True, text=True)
            # stdout = p.stdout
            # print('stdout:', stdout)
            # stderr = p.stderr
            # print('stderr:', stderr)

        def score(payload):
            # output = subprocess.run(["python", prj_info['main_file']], capture_output=True, text=True).stdout

            import json
            import ast
            json_string = json.dumps(payload, ensure_ascii=False)

            p = subprocess.run(["r42_env/bin/Rscript", "--vanilla",
                                     prj_info['main_file'], json_string], capture_output=True, text=True)
            stdout = p.stdout
            # print('stdout:', stdout)
            stderr = p.stderr
            # print('stderr:', stderr)

            # # need to remove ending dummy output
            # idx = stderr.find('>>>', 0)
            # stderr = stderr[:idx]

            if p.returncode:

                if send_email_when_fail:
                    ############### send email with error msg ##################
                    message = """Subject: {} Error [{}]\r\n

Receipients: {}

This message is sent from Cloud Pak for Data platform.

### Start of Error Message ###

{}

### End of Error Message ###""".format(date_str, code_pkg_name, receivers, stderr)

                    send_email(smtp_server, sender, receivers, message)

                output_json = {"stderr": stderr, "stdout": stdout}

            else:

                if send_email_when_successful:
                    ############### send successful notification ###############
                    message = """Subject: {} Success [{}]\r\n

Receipients: {}

This message is sent from Cloud Pak for Data platform.

### Start of Message ###

{}

### End of Message ###""".format(date_str, code_pkg_name, receivers, stdout)

                    send_email(smtp_server, sender, receivers, message)

                #output_json = {"stderr": stderr, "stdout": stdout}
                try:
                    output_json = ast.literal_eval(stderr)
                except Exception as e:
                    output_json = {"info": ["JSON String not found on output: ", stderr]}

            return {"predictions": [output_json]}  # work

        return score


    # step 2: upload_code_2_deployment_space
    from wml_client_api import upload_code_2_deployment_space
    code_pkg_name = deployment_info['code_pkg_name']
    upload_code_2_deployment_space(wml_client, prj_info, code_pkg_name)


    # # Optional: test locally
    # payload = {"input_data": [{
    #     "fields": ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"],
    #     "values": [
    #         [5.1, 3.5, 1.4, 0.2],
    #         [4.9, 3.1, 1.4, 0.2],
    #         [5.3, 6.1, 1.4, 0.2]
    #     ]
    # }]}
    #
    # function_result = my_deployable_function(wml_credentials, deployment_info, prj_info, email_setting)(payload)
    # print(function_result)

    # step 3: deploy
    from wml_client_api import deploy
    function_deployment_id = deploy(wml_client, my_deployable_function, deployment_info)


    # to do --- clean
    # remove tar file

    # step 4: run the job
    if test_run:
        deploy_mode = deployment_info['deploy_mode']
        # inputs = [
        #     {"Sepal.Length": 5.1, "Sepal.Width": 3.5, "Petal.Length": 1.4, "Petal.Width": 0.2},
        #     {"Sepal.Length": 4.9, "Sepal.Width": 3.1, "Petal.Length": 1.4, "Petal.Width": 0.2},
        #     {"Sepal.Length": 5.3, "Sepal.Width": 6.1, "Petal.Length": 1.4, "Petal.Width": 0.2},
        # ]
        # payload = {"input_data": [{"values": [{"inputs": inputs}]}]}

        # payload = {"input_data": [{
        #     "fields": ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"],
        #     "values": [
        #         [5.1, 3.5, 1.4, 0.2],
        #         [4.9, 3.1, 1.4, 0.2],
        #         [5.3, 6.1, 1.4, 0.2]
        #     ]
        # }]}

        payload = {"input_data": [{
            "fields": ["de056_ebitda_int_cover", "LGE_14_GWM_ROA2_avg", "de088_sales_growth",
                       "LGE_MDG_3_Liabilities_Assets", "de255_cash_ratio", "Segment_Region", "Segment_Top_Industry"],
            "values": [
                [0.32, 0.32, 0.22, 0.55, 0.44, "NZ", "RetailTrade"],
                [0.56, 0.77, 0.53, 0.88, 0.1, "AU", "WholesaleTrade"]
            ]
        }]}

        # run online application
        if deploy_mode == 'online':
            result = wml_client.deployments.score(function_deployment_id, payload)
            print('result=\n', result)

        # for batch job
        # below code is a reference if you want to schedule job externally using 3rd tool, eg Control M
        else:
            job = wml_client.deployments.create_job(function_deployment_id, meta_props=payload)
            job_id = wml_client.deployments.get_job_uid(job)
            print('\n\rjob_id: "%s" successfully submitted' % job_id)
            wml_client.deployments.get_job_details(job_id)

