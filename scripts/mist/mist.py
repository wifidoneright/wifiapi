import os,logging,json,urllib3,requests
from pprint import pprint
from os import abort

MISTBASEURL="https://api.gc1.mist.com"
MISTAPIKEY = os.environ.get("MISTAPIKEY")
if MISTAPIKEY == None:
    print("please set environment variable MISTAPIKEY")

class Node():
    def __init__(self,name,mac):
        self.name = name
        self.mac = mac
        self.status = None
        self.error = None
    
        
class Site():
    def __init__(self,name):
        self.name = name
        self.vendorSiteId = None
        self.orgID = None


def prep(nodeJSON, siteName="default"):
    """Instantiate the objects

    Args:
        siteName (str): name of the site
        nodeJSON (dict): list of dict with json data of nodes

    """
    siteObj = Site(siteName)
    nodeObjList = []
    try:
        for node in nodeJSON:
            n=Node(node["name"],node["mac"])
            nodeObjList.append(n)
    except ValueError() as e:
        raise e
    return siteObj,nodeObjList

def name_nodes(siteObj, nodeObjList):
    """Change the name of a node
    
    Arguments:
        siteObj {Site} -- Object of the site information
        nodeObjList {list} -- List of AP objects
        
    Returns: 
        [tuple] -- [lists of success and fail objects]
    """
    successList = []
    failList = []
    payload = []
    successList = []

    for nodeBatch in batch(nodeObjList, 100):
        for nodeObj in nodeBatch:
            payload.append({
                "mac": nodeObj.mac,
                "name": nodeObj.name})
            url = f"/api/v1/sites/{siteObj.vendorSiteId}/devices/import"
            logging.info(f"Naming {nodeObj.name}: {url}")
            respData = send_request( 
                url=url, requestType="POST", payload=json.dumps(payload))

            successList = list(set([*successList, *getSuccessList(respData,nodeObjList)]))
            failList = list(set([*failList, *getErrList(respData,nodeObjList)]))
    return successList, failList

def send_request(url="", requestType="GET", payload=""):
    '''
    This is a function that sets up what is needed to make a call to an API
    '''
    url = MISTBASEURL + url
    # print("Making a call")
    headers = {
        'Authorization': "Token " + MISTAPIKEY,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    try:  # See if you can do the following and do not break if it fails
        response = requests.request(
            requestType, url, headers=headers, verify=False, data=payload)

        if response.status_code == 200:
            #Great! our call is good. We can now do stuff here based on a successfull call
            print('Success! We have heard back from the call')

        elif response.status_code == 404:
            print('Our call returned a 404 error "Not Found."')
        data = json.loads(response.text)
        return data
    except requests.ConnectionError as err:
        logging.error(f"{err}")
        raise e
    except Exception as e:
        logging.error(e)
        abort()



def getSuccessList(respData,nodeObjList):
    """add the successful NodeObjects to a list"""
    successList = []
    if 'updated' in respData.keys():
        successMacList = respData['updated']
        for sucAPMac in successMacList:
            for nodeObj in nodeObjList:
                if str(sucAPMac).lower() == str(nodeObj.mac).lower():
                    successList.append(nodeObj)
    return successList

def getErrList(respData,nodeObjList):
    """add the errored NodeObjects to a list"""
    errorList = []
    if 'errors' in respData.keys():
        # if respData == 404:
        for error in respData['errors']:
            for nodeObj in nodeObjList:
                if nodeObj.mac in error:
                    nodeObj.status = "error"
                    nodeObj.error = f"unable to name"
                    errorList.append(nodeObj)
    return errorList
    
def batch(iterable, n=1):
	l = len(iterable)
	for ndx in range(0, l, n):
		yield iterable[ndx:min(ndx + n, l)]


def name_nodes(siteObj, nodeObjList):
    """Change the name of a node
    
    Arguments:
        siteObj {Site} -- Object of the site information
        nodeObjList {list} -- List of AP objects
        
    Returns: 
        [tuple] -- [lists of success and fail objects]
    """
    successList = []
    failList = []
    payload = []
    successList = []

    for nodeBatch in batch(nodeObjList, 100):
        for nodeObj in nodeBatch:
            payload.append({
                "mac": nodeObj.mac,
                "name": nodeObj.name})
            url = f"/api/v1/sites/{siteObj.vendorSiteId}/devices/import"
            logging.info(f"Naming {nodeObj.name}: {url}")
            respData = send_request(
                url=url, requestType="POST", payload=json.dumps(payload))

            successList = list(
                set([*successList, *getSuccessList(respData, nodeObjList)]))
            failList = list(
                set([*failList, *getErrList(respData, nodeObjList)]))
    return successList, failList

def main():
    nodeJSON=[{"name":"AP0001","mac":"de:ad:be:ef:00:01"}]
    site, nodes = prep(nodeJSON)
    succcesses,failed = name_nodes(site,nodes)
    print("successes")
    pprint(succcesses)
    print()
    print("=========================")
    print("failed")
    pprint(failed)

if __name__ == "__main__":main()
