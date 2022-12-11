

from ben_python_common import *
import requests
import json
import urllib.parse

configText = files.readall('configs.json')
configs = json.loads(configText)
assertEq('/mock.zendesk.com', configs['overrideJobStatusUrlPrefix'])

# we support with+without .json suffix on all endpoints,
# so run tests twice, once with this True, and once with it False 
doWithJson = True

#~ host = ''
#~ stateIds = dict(
    #~ admin = 11007294636571,
    #~ user1 = 11007294636571,
    #~ user2 = 11007299217179,
    #~ user3 = 11007314541595,
#~ )
host = f'http://localhost:{configs["portNumber"]}'
stateIds = dict(
    admin=111,
    user1 = None,
    user2 = None,
    user3 = None,
)


def confirmSet(obj, flds):
    for fld in flds:
        assertTrue(fld in obj, f'field {fld} not present')
        assertTrue(obj[fld], f'field {fld} is null/None')

def subInTemplates(s):
    customFlds = configs['customFields']
    lCustomFlds = list(customFlds.keys())
    s = s.replace('%FLDID1%', customFlds[lCustomFlds[0]])
    s = s.replace('%FLDID2%', customFlds[lCustomFlds[1]])
    s = s.replace('%FLDID3%', customFlds[lCustomFlds[2]])
    s = s.replace('%USER1%', str(stateIds["user1"]))
    s = s.replace('%USER2%', str(stateIds["user2"]))
    s = s.replace('%USER3%', str(stateIds["user3"]))
    for i in range(6):
        s = s.replace(f'%TICKET{i+1}%', str(stateIds[f'ticket{i+1}']))

    for obj in configs['customTriggers']:
        if obj['action']=='removeTagWhenPublicCommentPosted':
            s = s.replace('%TAG_REMOVED_BY_TRIGGER%', obj['value'])
        if obj['action']=='openPostWhenPublicCommentContainingTextPosted':
            s = s.replace('%TEXT_NOTICED_BY_TRIGGER%', obj['value'])


    

    return s

def quote(s):
    return urllib.parse.quote(s)

def sendGet(endpoint, encodedQueryString=''):
    return sendImpl('GET', endpoint, encodedQueryString=encodedQueryString)

def sendPost(endpoint, jsonData):
    return sendImpl('POST', endpoint, jsonData=jsonData)

def sendImpl(method, endpoint, jsonData=None, encodedQueryString=''):
    global configs
    if not endpoint.endswith('delete_all'):
        if not doWithJson:
            if endpoint.endswith('.json'):
                endpoint = endpoint.replace('.json', '')
        else:
            if not endpoint.endswith('.json'):
                endpoint += '.json'
    if encodedQueryString:
        encodedQueryString = '?' + encodedQueryString
    if endpoint.startswith('http'):
        fullEndpoint = f'{endpoint}{encodedQueryString}'
    else:
        assertTrue(endpoint.startswith('/api'), endpoint)
        fullEndpoint = f'{host}{endpoint}{encodedQueryString}'

    # would use curl, but want to fail on non-2xx responses
    # and most distros don't have latest curl with --fail-with-body
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'

    if jsonData:
        assertTrue(not jsonData or isinstance(jsonData, str))
        assertTrue(not jsonData or not '%' in jsonData, "missing template?", jsonData.split('%')[1])
        jsonData = stripComments(jsonData)
        try:
            json.loads(jsonData)
        except:
            assertTrue(False, 'looks like the json we are about to send does not parse', jsonData)

    r = doRequest(method, fullEndpoint, headers=headers, data=jsonData)
    if not (r.status_code>=200 and r.status_code<=299):
        trace('was sending,', method, fullEndpoint, jsonData)
        if 'x-zendesk-api-warn' in r.headers:
            trace('x-zendesk-api-warn = ' + r.headers['x-zendesk-api-warn'])
        trace(f"status_code={r.status_code}")
        assertTrue(False, f"status_code={r.status_code}", r.text)
    else:
        return json.loads(r.text)



def sendPostAndGetJob(endpoint, jsonData):
    jobStatus = sendPost(endpoint, jsonData)
    checkJobStatusOk(jobStatus, 'queued')
    response = sendGet(jobStatus['job_status']['url'])
    checkJobStatusOk(response, 'completed')
    return response['job_status']

def stripComments(s):
    lines = s.replace('\r\n', '\n').split('\n')
    lines = jslike.map(lines, lambda line: line.split('###')[0])
    return '\n'.join(lines)
    
def checkJobStatusOk(response, expectedStatus):
    assertEq(expectedStatus, response['job_status']['status'])
    theId = response['job_status']['id']
    assertTrue(configs['overrideJobStatusUrlPrefix'] in response['job_status']['url'])
    assertTrue(response['job_status']['url'].endswith(f'/api/v2/job_statuses/{theId}.json'))
    
    if expectedStatus == 'completed':
        assertTrue(int(response['job_status']['total']) > 0)
        assertTrue(int(response['job_status']['progress']) > 0)
        assertTrue(len(response['job_status']['message']) > 0)

    else:
        assertTrue((response['job_status']['total']) == None)
        assertTrue((response['job_status']['progress']) == None)
        assertTrue((response['job_status']['message']) == None)

def doRequest(method, *args, **kwargs):
    if method.upper() == 'GET':
        return requests.get(*args, **kwargs)
    elif method.upper() == 'PUT':
        return requests.put(*args, **kwargs)
    elif method.upper() == 'DELETE':
        return requests.delete(*args, **kwargs)
    elif method.upper() == 'POST':
        return requests.post(*args, **kwargs)
    else:
        assertTrue(False, "unknown method")


