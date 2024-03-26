# this is python code example to test your deployed R script/model API
import requests, json
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
        headers = {"Authorization": "Bearer " + r.json()['token'], "content-type": "application/json"}
        return True, headers, ""
    else:
        return False, None, r.text


cpd_url = 'https://cpd-cpd4-main-pi1003.apps-int.pi1003.cpaas.anz'
username = input("Enter your username: ")

import getpass
password = getpass.getpass("Enter your password: ")


auth_ok, headers, error_msg = get_user_token(cpd_url, username, password)

if not auth_ok:
    print("-- Failed authentication to", cpd_url)
else:
    print("-- Successfully authenticated to", cpd_url)

    # Modify below accordingly:
    # online API endpoint
    endpoint = "https://cpd-cpd4-main-pi1003.apps-int.pi1003.cpaas.anz/ml/v4/deployments/r_randy_online_api/predictions?version=2021-05-01"

    # self defined input JSON example
    # inputs = [
    #     {"Sepal.Length": 5.1, "Sepal.Width": 3.5, "Petal.Length": 1.4, "Petal.Width": 0.2},
    #     {"Sepal.Length": 4.9, "Sepal.Width": 3.1, "Petal.Length": 1.4, "Petal.Width": 0.2},
    #     {"Sepal.Length": 5.3, "Sepal.Width": 6.1, "Petal.Length": 1.4, "Petal.Width": 0.2},
    # ]
    #
    # payload = {"input_data": [{"values": [{"inputs": inputs}]}]}

    # CPD compliant input JSON example
    payload = {"input_data": [{
        "fields": ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"],
        "values": [
            [5.1, 3.5, 1.4, 0.2],
            [4.9, 3.1, 1.4, 0.2],
            [5.3, 6.1, 1.4, 0.2]
        ]
    }]}

    response = requests.post(url=endpoint, headers=headers,json=payload, verify=False).json()
    # response["predictions"][0]["out"]

    print(response)