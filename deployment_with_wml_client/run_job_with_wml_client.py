# You must deploy your job before you can run your job using below code.
import argparse
import yaml

def get_function_deployment_id(name):
    for function in wml_client.deployments.get_details()["resources"]:

        if name == function["metadata"]["name"]:
            print("\nFound Deployment: ", function["metadata"]["name"])
            return function["metadata"]["id"]
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy Code Packages')

    parser.add_argument('--yaml_file', '-y', type=str,
                        default='configuration_cpd45_dbaccess.yaml')

    args = parser.parse_args()

    yaml_file = args.yaml_file

    # Read YAML file
    print('\n-- Loading configuration yaml file:', yaml_file)
    with open(yaml_file, 'r') as stream:
        configuration = yaml.safe_load(stream)

    # print(configuration)

    wml_credentials = configuration['wml_credentials']
    deployment_info = configuration['deployment_info']

    # step 1: login to wml
    from wml_client_api import wml_login
    wml_client = wml_login(wml_credentials)

    space_id = deployment_info['space_id']
    wml_client.set.default_space(space_id)
    print("\n\rSet space id successfully:", space_id)


    # step 4: run the job
    deploy_mode = deployment_info['deploy_mode']

    # payload = {
    #   "input_data": [
    #     {
    #       "fields": [],
    #       "values": [1] # 1 is a dummy input that needed
    #     }
    #   ]
    # }

    payload = {"input_data": [{
        "fields": ["AGE", "SEXE"],
        "values": [
            [33, "F"],
            [59, "F"],
            [28, "M"]
        ]
    }]}

    deploy_name = deployment_info['code_pkg_name'] + '_deployment'
    # Getting the function_deployment_id using deployment_name
    function_deployment_id = get_function_deployment_id(deploy_name)

    if function_deployment_id:

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

    else:
        print("This deployment name", deploy_name, " could not be found in SpaceID: ", space_id)
        print("Please verify if it has been deployed")

    print("\n### Host: ", wml_credentials['url'], "\n### Space_id: ", space_id, " \n### Function_id: ",
          function_deployment_id)