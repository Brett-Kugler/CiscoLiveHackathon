import requests
import json
import logging
import xml
from requests.auth import HTTPBasicAuth
import sys
import time
from collections import OrderedDict

def doRequestsDebug():
    # These two lines enable debugging at httplib level (requests->urllib3->httplib)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    import httplib
    httplib.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig() 
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


#------------------------------------------- main ------------------------------------------------

if name == "__main__":
    # Enable or Disable this call for requests debug
    doRequestsDebug()

    restURL = 'https://10.10.20.121:8081/api/v0'

    authToken = ''
    userCatalogOptions = []

    if len(sys.argv) < 3:
        print 'Usage: python CiscoLiveHackathon.py <username> <password>'
        sys.exit(0)
    else:
        user = sys.argv[1]
        password = sys.argv[2]

    # Authenticate to APIC EM
    resp=getInfoRequest(restURL+'/login',auth=HTTPBasicAuth(user, password))
    if resp != None:
        if 'X-SDS-AUTH-TOKEN' in resp.headers:
            authToken = resp.headers['X-SDS-AUTH-TOKEN']

            headers={'X-SDS-AUTH-TOKEN':authToken, 'Accept':'application/json'}
        

    else:
        print 'Failed authorization to', restURL


# Handy functions
#print json.dumps(resp.json(), indent=4, separators=(',', ': '))
#print sys.exc_info()[0]
