#!/usr/bin/python3

import requests
import json
import sys


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

URL_TOWER = "http://localhost:80"
TOKEN_TOWER = "AaIy8KidheueeHxlzWajbPibNLIbyJ"

def update_cred_id(cred_id, cred_name, cred_password):
    #inputs = {'artifactory_user': cred_name, 'artifactory_password': cred_password}
    inputs = {'username': cred_name, 'password': cred_password}
    try:
        payload = {'inputs': inputs }
        result_api = requests.patch(URL_TOWER+'/api/v2/credentials/'+str(cred_id)+'/',
                                    verify=False,
                                    data=json.dumps(payload),
                                    headers={'Authorization': 'Bearer '+TOKEN_TOWER,
                                            'content-type': 'application/json'})
    except Exception as fail:
        print(Colors.FAIL+"Failed to update : "+str(cred_id)+Colors.ENDC)
        sys.exit(1)
    else:
        print(Colors.OKGREEN+str(json.loads(result_api.text))+Colors.ENDC)


try:
    f = open('dump_cred.txt', 'r') 

    for line in f:
        decoup_line = line.split("|")
        login = decoup_line[0].strip()
        password = decoup_line[1].strip()
        decoup_login = login.split("-") 
        project_id = decoup_login[1]

        print(Colors.OKBLUE+"update de ca-"+project_id+Colors.ENDC)

        # verif presence du credential
        try:
            RESULT_API = requests.get(URL_TOWER+'/api/v2/credentials/?name__icontains=ca-'+project_id,
                                        verify=False,
                                        headers={'Authorization': 'Bearer '+TOKEN_TOWER,
                                                'content-type': 'application/json'})
        except Exception as FAIL:
            print(Colors.FAIL+"Failed to read credentials RET_CODE: "+str(FAIL)+Colors.ENDC)
            sys.exit(1)
        else:
            if json.loads(RESULT_API.text)["count"] == 0:
                print (Colors.FAIL+"Pas de credential trouve pour ca-"+project_id+Colors.ENDC)
            else:
                for un_cred in json.loads(RESULT_API.text)["results"]:
                    cred_id = un_cred["id"]
                    update_cred_id(cred_id, login, password) 

        
finally:
    f.close()
