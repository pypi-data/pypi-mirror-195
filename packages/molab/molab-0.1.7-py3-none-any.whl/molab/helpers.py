import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time
from morpheuscypher import Cypher

def _get_instance_ids_from_names(url,headers,names:list):
    session = FuturesSession()
    endpoint = "/api/instances"
    ids = []
    futures=[session.get(f'{url}{endpoint}?name={n}',headers=headers,verify=False) for n in names]
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            i = resp.json()["instances"][0]
            ids.append(i["id"])
    return(ids)

def get_aio_external_ips(url,headers,ids:list):
    session = FuturesSession()
    endpoint = "/api/instances"
    ips = []
    futures=[session.get(f'{url}{endpoint}{i}',headers=headers,verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result()   
        if "200" in str(resp):
            for node in resp["instance"]["containerDetails"]:
                if "single-node" in node["externalHostname"]:
                    ips.append(node["ip"])
    return(ips)

def _get_morpheus_license_from_cypher(url,token,cypher_name):
    logger.info(f'Begin get_morpheus_license_from_cypher')
    c = Cypher(url=url,token=token,ssl_verify=False)
    out = c.get(cypher_name)
    return(out)

def sleep(time):
    logger.info(f'Sleeping for {time}')
    time.sleep(time)