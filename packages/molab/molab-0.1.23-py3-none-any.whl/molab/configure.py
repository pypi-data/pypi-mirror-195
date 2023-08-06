import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from loguru import logger
import requests
import pkgutil
import time
from .helpers import _get_morpheus_license_from_cypher

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def setup_aio(node_ip,account_name,user_name,password,email,license):
    logger.info(f'Begin attempt to set up Morpheus AIO')
    try:
        ping = ""
        timeout = 1
        while "MORPHEUS PING" not in ping:
            logger.info(f'Timeout count now at {timeout}')
            try:
                ping = _get_appliance_node_status(node_ip)
                if "Morpheus is Loading..." in ping:
                    logger.info(f'{ping} checking again in 60 seconds')
                    time.sleep(60)
                    timeout = timeout + 1
                elif "404" in str(ping):
                    logger.info(f'Encountered a 404. Assuming it is still initializing. Waiting 60 seconds to check again.')
                    time.sleep(60)
                    timeout = timeout + 1
                elif "Could not reach node:" in ping:
                    logger.info(f'Unable to reach the node. Assuming it is still initializing. Waiting 60 seconds to check again.')
                    time.sleep(60)
                    timeout = timeout + 1
                elif timeout >= 45:
                    return("Timout waiting for the system to come up")
            except Exception as e:
                logger.error(f'Unhandled exception occurred')
                return(e)
        try:
            logger.info(f'Attempting to configure with the follow configuration:')
            _apply_morpheus_setup_config(node_ip,account_name,user_name,password,email)
        except Exception as e:
            logger.error(f'Unhandled exception: {e}')
            return(e)
        try:
            token = _get_morpheus_api_token(node_ip,user_name,password)
        except Exception as e:
            logger.error(f'Unhandled exception: {e}')
            return(e)
        try:
            _apply_morpheus_license(node_ip,token,license)
        except Exception as e:
            logger.error(f'Unhandled exception: {e}')
            return(e)
    except Exception as e:
        logger.error(f'Unhandled exception occurred: {e}')


def setup_three_node():
    pass

def _apply_morpheus_setup_config(node_ip,account_name,user_name,password,email):
    logger.info("Begin attempt to configure Morpheus")
    url = f'https://{node_ip}'
    endpoint = "/api/setup/init"
    headers={'Content-Type': 'application/json',"Accept":"application/json"}
    body={"applianceUrl": url, "applianceName": account_name, "accountName": account_name, "username": user_name, "password": password, "email": email, "firstName": user_name }
    try:
        logger.info(f'Attempting to perform first time setup on node {node_ip}')
        resp = requests.post(f'{url}{endpoint}',headers=headers,verify=False,data=json.dumps(body))
    except Exception as e:
        logger.error(f'Something went wrong: {e}')
    if "200" in str(resp):
        logger.info(f'Initial configuration of Morpheus successful')
    else:
        logger.error(f'It appears something went wrong')
    return(resp)

def _get_appliance_node_status(node_ip):
    headers = {'Content-Type': 'application/json'}
    url = f'https://{node_ip}'
    endpoint = "/ping"
    try:
        logger.info(f'Checking for Morpheus UI to be up: {node_ip}')
        resp = requests.get(f'{url}{endpoint}',headers=headers,verify=False)
    except Exception as e:
        logger.error(f'Could not reach node: {node_ip}')
        return(f'Could not reach node: {node_ip}')
    if "MORPHEUS PING" in str(resp.text):
        out = resp.text
        logger.info(f'Looks like the Morpehus UI is up: {out}')
    elif "Morpheus is Loading..." in str(resp.text):
        out = "Morpheus is Loading..."
    else:
        out = resp
    return(out)

def _get_morpheus_api_token(url,user_name,password):
    if 'https://' not in url:
        url = f'https://{url}'
    endpoint = "/oauth/token?grant_type=password&scope=write&client_id=morph-api"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {"username": user_name, "password": password}
    try:
        logger.info(f'Attempting to get API token')
        resp = requests.post(f'{url}{endpoint}',headers=headers,verify=False,data=body)
    except Exception as e:
        logger.info(f'Something went wrong')
    if "200" in str(resp):
        logger.info("Token acquired")
        token = resp.json()["access_token"]
        return(token)
    elif "400" in str(resp):
        logger.error('Bad credentials')
        return(resp)
    else:
        return(resp)
    
def _apply_morpheus_license(url,token,license):
    headers={'Content-Type': 'application/json',"Accept":"application/json", "Authorization": "BEARER " + token}
    if 'https://' not in url:
        url = f'https://{url}'
    endpoint = "/api/license"
    body = {"license": license}
    try:
        logger.info(f'Attempting to apply the license')
        resp = requests.post(f'{url}{endpoint}',headers=headers,verify=False,data=json.dumps(body))
    except Exception as e:
        logger.error(f'Something went wrong')
    if "200" in str(resp):
        logger.info("License successfully applied")
        return(resp)
    elif "\"success\":false," in str(resp.text):
        logger.error(resp.json()["msg"])
    elif "\"error\":" in str(resp.text):
        logger.error(resp.json()["error_description"])
    return(resp)

def _get_morpheus_setup_status(url):
    # Returns True if the platform is setup. Otherwise returns False.
    if 'https://' not in url:
        url = f'https://{url}'
    endpoint = "/api/ping"
    headers = {'Content-Type': 'application/json'}
    try:
        logger.info(f'Checking the setup status of node: {url}')
        resp = requests.get(f'{url}{endpoint}',headers=headers, verify=False)
    except Exception as e:
        logger.error(f'Could not reach node: {url}')
    if "\'setupNeeded\': True," in resp:
        return(False)
    else:
        return(True)
    
def get_aio_external_ips(url,headers,ids:list):
    session = FuturesSession()
    endpoint = "/api/instances"
    ips = []
    futures=[session.get(f'{url}{endpoint}/{i}',headers=headers,verify=False) for i in ids]
    logger.info(f'Checking for AIO nodes')
    for future in as_completed(futures):
        resp = future.result()
        if "404" in str(resp):
            logger.error(f'Returned 404')
            return(resp)  
        elif "400" in str(resp):
            logger.error(f'Returned 400')
            return(resp) 
        elif "200" in str(resp):
            for node in resp.json()["instance"]["containerDetails"]:
                if "single-node" in node["externalHostname"]:
                    logger.info(f'Found AIO node IP of : {node["ip"]}')
                    ips.append(node["ip"])
    return(ips)

def get_lab_info(url,headers,ids:list):
    session = FuturesSession()
    endpoint = "/api/instances"
    data = [['Lab Name','External IP','Internal IP','AMI ID','Access Key','Secret Key']]
    futures=[session.get(f'{url}{endpoint}/{i}/state',headers=headers,verify=False) for i in ids]
    lb_endpoint = []
    rds_endpoint = []
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            # logger.info(f'Parsing instance state for instance id: {resp.json()["workloads"][0]["refId"]}')
            # logger.info(f'Parsing the terraform resources')
            instance_data = []
            lab_name = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "lab_name"]
            eip = [i["value"]["value"][0][0]["public_ip"] for i in resp.json()["output"]["outputs"] if i["name"] == "elastic_ips"]
            private_ip = [i["value"]["value"][0][0]["private_ip"] for i in resp.json()["output"]["outputs"] if i["name"] == "elastic_ips"]
            ami_id = [i["value"]["value"][0][0]["ami"] for i in resp.json()["output"]["outputs"] if i["name"] == "instances"]
            state_data = json.loads(resp.json()["stateData"])
            access_key = [i["values"]["id"] for i in state_data["values"]["root_module"]["child_modules"][0]["resources"] if i["type"] == "aws_iam_access_key"]
            secret_key = [i["values"]["secret"] for i in state_data["values"]["root_module"]["child_modules"][0]["resources"] if i["type"] == "aws_iam_access_key"]
            instance_data.extend([lab_name[0],eip[0],private_ip[0],ami_id[0],access_key[0],secret_key[0]])
            try: 
                lb_endpoint = [i["value"]["value"][0]["dns_name"] for i in resp.json()["output"]["outputs"] if i["name"] == "load_balancer"]
                data[0].append('LB Endpoint')
                instance_data.append(lb_endpoint[0])
            except:
                pass
            try:
                rds_endpoint = [i["value"]["value"][0][0]["endpoint"] for i in resp.json()["output"]["outputs"] if i["name"] == "rds"]
                data[0].append('RDS Endpoint')
                instance_data.append(rds_endpoint[0])
            except:
                pass
            try:
                instances = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "instances"]
                app_nodes = instances[0][1]
                app_1_pub = [i["public_ip"] for i in app_nodes if "APP-01" in i["tags_all"]["Name"]]
                data[0].append('App-01 Public IP')
                instance_data.append(app_1_pub[0])
                app_1_priv = [i["private_ip"] for i in app_nodes if "APP-01" in i["tags_all"]["Name"]]
                data[0].append('App-01 Private IP')
                instance_data.append(app_1_priv[0])
                app_2_pub = [i["public_ip"] for i in app_nodes if "APP-02" in i["tags_all"]["Name"]]
                data[0].append('App-02 Public IP')
                instance_data.append(app_2_pub[0])
                app_2_priv = [i["private_ip"] for i in app_nodes if "APP-02" in i["tags_all"]["Name"]]
                data[0].append('App-02 Private IP')
                instance_data.append(app_2_priv[0])
                app_3_pub = [i["public_ip"] for i in app_nodes if "APP-03" in i["tags_all"]["Name"]]
                data[0].append('App-03 Public IP')
                instance_data.append(app_3_pub[0])
                app_3_priv = [i["private_ip"] for i in app_nodes if "APP-03" in i["tags_all"]["Name"]]
                data[0].append('App-03 Private IP')
                instance_data.append(app_3_priv[0])
            except:
                pass
            try:
                instances = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "instances"]
                perc_nodes = instances[0][2]
                perc_1_pub = [i["public_ip"] for i in perc_nodes if "PERC-01" in i["tags_all"]["Name"]]
                data[0].append('Perc-01 Public IP')
                instance_data.append(perc_1_pub[0])
                perc_1_priv = [i["private_ip"] for i in perc_nodes if "PERC-01" in i["tags_all"]["Name"]]
                data[0].append('Perc-01 Private IP')
                instance_data.append(perc_1_priv[0])
                perc_2_pub = [i["public_ip"] for i in perc_nodes if "PERC-02" in i["tags_all"]["Name"]]
                data[0].append('Perc-02 Public IP')
                instance_data.append(perc_2_pub[0])
                perc_2_priv = [i["private_ip"] for i in perc_nodes if "PERC-02" in i["tags_all"]["Name"]]
                data[0].append('Perc-02 Private IP')
                instance_data.append(perc_2_priv[0])
                perc_3_pub = [i["public_ip"] for i in perc_nodes if "PERC-03" in i["tags_all"]["Name"]]
                data[0].append('Perc-03 Public IP')
                instance_data.append(perc_3_pub[0])
                perc_3_priv = [i["private_ip"] for i in perc_nodes if "PERC-03" in i["tags_all"]["Name"]]
                data[0].append('Perc-03 Private IP')
                instance_data.append(perc_3_priv[0])
            except:
                pass
            data.append(instance_data)
    return(data)

def get_lab_instance_ids_from_tag(url,headers,controller_id,tag_name):
    endpoint = "/api/instances"
    resp = requests.get(f'{url}{endpoint}/{controller_id}',headers=headers,verify=False)
    tags = resp.json()["instance"]["tags"]
    for tag in tags:
        if tag["name"] == tag_name:
            ids = tag["value"]
    return(json.loads(ids))