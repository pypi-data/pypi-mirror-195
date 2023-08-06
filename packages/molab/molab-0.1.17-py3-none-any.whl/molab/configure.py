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
    resource_list = ["elastic_ips","instances"]
    data = []
    futures=[session.get(f'{url}{endpoint}/{i}/state',headers=headers,verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result()
        instance_data = []
        if "200" in str(resp):
            logger.info(f'Parsing instance state: {resp.json()["workloads"]["refId"]}')
            for i in resp.json()["output"]["outputs"]:
                logger.info(f'Parsing the terraform resources')
                if i["name"] in resource_list:
                    logger.info(f'Found {i["name"]}')
                else:
                    logger.info(f'{i["name"]} not found in resource_list. Skipping it')          
    return(resp)