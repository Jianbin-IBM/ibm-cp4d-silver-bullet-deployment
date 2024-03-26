# reference:
# https://wml-api-pyclient-dev-v4.mybluemix.net/
# http://ibm-wml-api-pyclient.mybluemix.net/core_api.html#software-specifications


import os
import tarfile
import requests
from ibm_watson_machine_learning import APIClient


def get_assets_dict(wml_client):
    # data = { "query": "*:*" }
    # response = requests.post(wml_client.data_assets._href_definitions.get_search_asset_href(),
    #                          params=wml_client.data_assets._client._params(),
    #                          headers=wml_client.data_assets._client._get_headers(),
    #                          json=data, verify=False)
    # asset_details = wml_client.data_assets._handle_response(200, "list assets", response)["results"]
    # assets_dict = {asset_detail["metadata"]["name"]:asset_detail["metadata"]["asset_id"] for asset_detail in asset_details}
    assets_dict = {x["metadata"]["name"]: x["metadata"]["asset_id"] for x in
                   wml_client.data_assets.get_details()["resources"]}
    return assets_dict


def compress_code(code_dir,code_pkg_name):
    # code_dir_basename = os.path.basename(code_dir)
    tar_file_name = code_pkg_name +".tar.gz"

    # tar czf python_for_13_topics_daily.tar.gz -C ../python_for_13_topics_daily .
    cmd_str = 'tar czf ' + tar_file_name + ' -C ' +code_dir +' .'
    # print(cmd_str)
    os.system(cmd_str)
    print('\n\rCode Package: ', tar_file_name, 'compressed successfully')

    # with tarfile.open(tar_file_name, "w:gz") as tar:
    #     tar.add(code_dir, arcname=os.path.basename(code_dir))
    #     print(tar_file_name,'has been created successfully')

# to do
def clean_tar(code_dir):
    pass

def upload_code_2_deployment_space(wml_client, prj_info, code_pkg_name):

    # step 1: set space id
    # wml_client.set.default_space(space_id)

    # step 2: compress the file
    compress_code(prj_info['code_dir'], code_pkg_name)

    # step 3: upload the file
    assets_dict = get_assets_dict(wml_client)

    # code_dir_basename = os.path.basename(prj_info['code_dir'])
    tar_file_name = code_pkg_name + ".tar.gz"
    required_files = [tar_file_name]

    for f in required_files:
        # delete existing files
        if f in assets_dict: wml_client.data_assets.delete(assets_dict[f])

        # upload files
        print('\n\rStart to upload Code Package: ', tar_file_name)
        wml_client.data_assets.create(name=f, file_path=f)
        print('Code Package: ', tar_file_name, 'uploaded to deployment space successfully')
        
        
def wml_login(wml_credentials):
    url = wml_credentials['url']
    # version = wml_credentials['version']
    wml_client = APIClient(wml_credentials)
    #print("\n\rWML login successfully: CPD URL=",url,', CPD version=', version)
    print("\n\rWML login successfully: CPD URL=", url)

    return wml_client


# hardware spec: refer to:https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/deploy-batch-details.html
# Size 	Hardware definition
# XS 	1 CPU and 4 GB RAM
# S 	2 CPU and 8 GB RAM
# M 	4 CPU and 16 GB RAM
# ML 	4 CPU and 32 GB RAM
# L 	8 CPU and 32 GB RAM
# XL 	16 CPU and 64 GB RAM

def deploy(wml_client, my_deployable_function, deployment_info):

    force_2_update = deployment_info['force_2_update']
    deploy_mode = deployment_info['deploy_mode']
    # space_id = deployment_info['space_id']
    hardware_spec = deployment_info['hardware_spec']
    runtime = deployment_info['runtime']
    num_nodes = deployment_info['num_nodes']

    # step 1: set space id
    # wml_client.set.default_space(space_id)

    # Randy's code
    def get_function_id(name):
        for function in wml_client.repository.get_function_details()["resources"]:
            if name == function["metadata"]["name"]:
                return function["metadata"]["id"]
        return None

    def get_function_deployment_id(name):
        for function in wml_client.deployments.get_details()["resources"]:
            if name == function["metadata"]["name"]:
                return function["metadata"]["id"]
        return None

    code_pkg_name =  deployment_info['code_pkg_name']
    function_name = code_pkg_name + '_func'
    deploy_name = code_pkg_name +'_deployment'

    function_deployment_id = get_function_deployment_id(deploy_name)
    if function_deployment_id:
        if force_2_update:
            wml_client.deployments.delete(function_deployment_id)
        else:
            print(deploy_name, 'has been found in the current deployment space')
            print('By default, we only update the assets without update the deployment')
            print('You can set "force_2_update" to be True in configuration yaml file to force the update')
            return

    function_id = get_function_id(function_name)
    if function_id:
        if force_2_update:
            wml_client.repository.delete(function_id)
        else:
            print(function_name, 'has been found in the current deployment space')
            print('By default, we only update the assets without update the functions')
            print(
                'You can set "force_2_update" to be True in configuration yaml file to force the update')
            return

    meta_props = {
        wml_client.repository.FunctionMetaNames.NAME: function_name,
        wml_client.repository.FunctionMetaNames.SOFTWARE_SPEC_UID: wml_client.software_specifications.get_id_by_name(
            runtime)
    }
    function_details = wml_client.repository.store_function(meta_props=meta_props, function=my_deployable_function)

    if deploy_mode =='online':
        # online
        meta_props = {
            wml_client.deployments.ConfigurationMetaNames.NAME: deploy_name,
            wml_client.deployments.ConfigurationMetaNames.ONLINE: {},
            wml_client.deployments.ConfigurationMetaNames.HARDWARE_SPEC: {"name": hardware_spec},
            wml_client.deployments.ConfigurationMetaNames.SERVING_NAME: deploy_name+"_online"
        }
    else:
        # batch
        meta_props = {
            wml_client.deployments.ConfigurationMetaNames.NAME: deploy_name,
            wml_client.deployments.ConfigurationMetaNames.BATCH: {},
            wml_client.deployments.ConfigurationMetaNames.HARDWARE_SPEC: {
                "name": hardware_spec,
                "num_nodes": num_nodes
            }
        }

    function_uid = wml_client.repository.get_function_uid(function_details)
    function_deployment_details = wml_client.deployments.create(function_uid, meta_props=meta_props)

    function_deployment_id = wml_client.deployments.get_uid(function_deployment_details)
    print('function_deployment_id = "%s"'%function_deployment_id)


    if deploy_mode == 'online':
        function_deployment_endpoint_url = wml_client.deployments.get_scoring_href(function_deployment_details)
        print('Deployment endpoint = ',function_deployment_endpoint_url)


    return function_deployment_id
