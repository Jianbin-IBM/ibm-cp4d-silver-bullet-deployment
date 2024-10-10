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
                        default='configuration_template.yaml')

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

        def get_date_str():
            from datetime import datetime
            date_str = datetime.now().strftime("%Y-%m-%d")
            return date_str

        date_str = get_date_str()

        assets_dict = get_assets_dict()

        # prj_info = params["prj_info"]
        code_pkg_name = deployment_info['code_pkg_name']
        tar_file_name = code_pkg_name + ".tar.gz"
        wml_client.data_assets.download(assets_dict[tar_file_name], tar_file_name)
        # for f in params["required_files"]: wml_client.data_assets.download(assets_dict[f], f)

        subprocess.run(["tar", "xzf", tar_file_name])

        def score(payload):
            # output = subprocess.run(["python", prj_info['main_file']], capture_output=True, text=True).stdout

            import json
            import ast
            json_string = json.dumps(payload, ensure_ascii=False)
            p = subprocess.run(["python", prj_info['main_file']], capture_output=True, input=json_string,
                               text=True)

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

                try:
                    jsondata = ast.literal_eval(stderr)
                except Exception as e:
                    jsondata = {"info": ["JSON String not found on output: ", stderr]}

                # for online application, we may want to omit the stdout to reduce the unnecessary traffic
                enable_stdout = deployment_info['enable_stdout']
                if enable_stdout:
                    output_json = jsondata
                    jsondata.update({"stdout": stdout})
                else:
                    output_json = jsondata

            deploy_mode = deployment_info['deploy_mode']
            if deploy_mode == 'online':
                return {"predictions": [output_json]}  # work
            else:
                # somehow batchmode will never finish with above formart, but below works
                return {"predictions": [{"values": [output_json]}]}

        return score


    # step 2: upload_code_2_deployment_space
    from wml_client_api import upload_code_2_deployment_space
    code_pkg_name = deployment_info['code_pkg_name']
    upload_code_2_deployment_space(wml_client, prj_info, code_pkg_name)


    # # Optional: test locally
    # payload = {
    #     "input_data": [{
    # #         "fields": ["keywords"],
    #         "values": []
    #     }]
    # }
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
        payload = {
            "input_data": [
                {
                    "fields": [],
                    "values": [1]  # 1 is a dummy input that needed
                }
            ]
        }

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

