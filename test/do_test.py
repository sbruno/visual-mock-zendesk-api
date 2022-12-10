
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
    #~ user1 = 11007294636571,
    #~ user2 = 11007299217179,
    #~ user3 = 11007314541595,
#~ )
host = f'http://localhost:{configs["portNumber"]}'
stateIds = dict(
    user1 = None,
    user2 = None,
    user3 = None,
)


def go1UsersCreateMany():
    #~ if not getInputBool('OK to run this test, which will reset all tickets+users?'):
        #~ assertTrue(False, 'cancelling test')
    
    ############## Reset state ###################
    sendPost('/api/delete_all', {})

    ############## Errors ###################
    # cannot set id
    s = r'''{"users": [
{
   "id": 567,
   "email": "utest1@a.com",
   "name": "utest1"
}]}'''
    assertException(lambda: sendPost('/api/v2/users/create_many', s), Exception)

    # email is required
    s = r'''{"users": [
{
   "name": "utest1"
}]}'''
    assertException(lambda: sendPost('/api/v2/users/create_many', s), Exception)

    
    ############## Successes ###################
    template = r'''{"users": [
{
   "email": "utest1@a.com",
   "name": "utest1"
},
{
   "email": "utest2@a.com",
   "name": "utest2"
}]}
    '''
    result = sendPostAndGetJob('/api/v2/users/create_many', jsonData=template)
    assertEq(2, len(result['results']))

    assertEq(0, result['results'][0]['index'])
    assertEq('create', result['results'][0]['action'])
    assertEq('Created', result['results'][0]['status'])
    assertEq(True, result['results'][0]['success'])
    assertTrue(int(result['results'][0]['id']) > 0)
    assertEq(1, result['results'][1]['index'])
    assertEq('create', result['results'][1]['action'])
    assertEq('Created', result['results'][1]['status'])
    assertEq(True, result['results'][1]['success'])
    assertTrue(int(result['results'][1]['id']) > 0)

    stateIds['user1'] = int(result['results'][0]['id'])
    stateIds['user2'] = int(result['results'][1]['id'])

    ############## Successes and already exists ###################
    template = r'''{"users": [
{
   "email": "utest1@a.com",
   "name": "utest1"
},
{
   "email": "utest3@a.com",
   "name": "utest3"
}]}
    '''
    result = sendPostAndGetJob('/api/v2/users/create_many', template)
    assertEq(2, len(result['results']))

    assertEq(0, result['results'][0]['index'])
    assertEq('update', result['results'][0]['action'])
    assertEq('Updated', result['results'][0]['status'])
    assertEq(True, result['results'][0]['success'])
    assertEq(stateIds['user1'], int(result['results'][0]['id']))
    assertEq(1, result['results'][1]['index'])
    assertEq('create', result['results'][1]['action'])
    assertEq('Created', result['results'][1]['status'])
    assertEq(True, result['results'][1]['success'])
    assertTrue(int(result['results'][1]['id']) > 0)

    stateIds['user3'] = int(result['results'][1]['id'])

def go2UsersSearch():
    ############## One result ###################
    result = sendGet('/api/v2/users/search', 'query=email:utest3@a.com')
    assertEq(1, result['count'])
    assertEq(1, len(result['users']))
    assertTrue(int(result['users'][0]['id']) > 0)
    assertEq('utest3', result['users'][0]['name'])
    assertEq('utest3@a.com', result['users'][0]['email'])

    ############## No results ###################
    result = sendGet('/api/v2/users/search', 'query=email:utest444@a.com')
    assertEq(0, result['count'])
    assertEq(0, len(result['users']))
    
def go3UsersShowMany():
    ############## One result ###################
    result = sendGet('/api/v2/users/show_many', f'ids={stateIds["user1"]}')
    assertEq(1, len(result['users']))
    assertEq(stateIds["user1"], result['users'][0]['id'])
    assertEq('utest1', result['users'][0]['name'])
    assertEq('utest1@a.com', result['users'][0]['email'])
    ############## Many results ###################
    result = sendGet('/api/v2/users/show_many', f'ids={stateIds["user2"]},999,{stateIds["user3"]}')
    assertEq(2, len(result['users']))
    assertEq(stateIds["user2"], result['users'][0]['id'])
    assertEq('utest2', result['users'][0]['name'])
    assertEq('utest2@a.com', result['users'][0]['email'])
    assertEq(stateIds["user3"], result['users'][1]['id'])
    assertEq('utest3', result['users'][1]['name'])
    assertEq('utest3@a.com', result['users'][1]['email'])
    ############## No results ###################
    result = sendGet('/api/v2/users/show_many', f'ids=999')
    assertEq(0, len(result['users']))

def go4TicketsCreateMany():
    # features:
    #       add quotes around lots of the ids , incl custom_fields
    #       create with no subject and no requester
    #       inline user creation
    #       comment shortcuts
    #       status defaults to open
    #       public defaults to true
    s = r'''{
    "tickets": [
      {
        "subject": "ticket1",
        "created_at": "2022-01-01T06:38:32.399Z",
        "requester_id": %USER1%,
        "status": "pending",
        "custom_fields": [{"id":"345", "value":"fldval1"}, {"id":%FLDID%, "value":"fldval2"}],
        "comments": [
          {
            "created_at": "2022-01-02T06:38:32.399Z",
            "body": "comment1",
            "public": false,
            "author_id": %USER1%
          },
          {
            "created_at": "2022-01-03T06:38:32.399Z",
            "body": "comment2",
            "public": true
          }
        ]
      }, {
        "subject": "ticket2",
        "created_at": "2022-01-01T06:38:32.399Z",
        "requester": {"name":"utest4inline", "email": "utest4inline@a.com"},
        "tags": ["tag1", "tag2"],
        "comment": {"body": "plainStringComment1"}
      }, {
        "created_at": "2022-01-01T06:38:32.399Z",
        "comment": "plainStringComment2"
      }
    ]
  }
  '''
    customFlds = configs['customFields']
    firstCustomFld = list(customFlds.keys())[0]
    s = s.replace('%FLDID%', customFlds[firstCustomFld])
    s = s.replace('%USER1%', str(stateIds["user1"]))
    s = s.replace('%USER2%', str(stateIds["user2"]))
    s = s.replace('%USER3%', str(stateIds["user3"]))
    result = sendPostAndGetJob('/api/v2/imports/tickets/create_many', s)
    assertEq(3, len(result['results']))
    assertEq(0, result['results'][0]['index'])
    stateIds['ticket1'] = int(result['results'][0]['id'])
    assertEq(True, result['results'][0]['success'])
    assertEq(1, result['results'][1]['index'])
    stateIds['ticket2'] = int(result['results'][1]['id'])
    assertEq(True, result['results'][1]['success'])
    assertEq(2, result['results'][2]['index'])
    stateIds['ticket3'] = int(result['results'][2]['id'])
    assertEq(True, result['results'][2]['success'])

    ############## Confirm inline user got created ###################
    result = sendGet('/api/v2/users/search', 'query=email:utest4inline@a.com')
    assertEq(1, result['count'])
    assertEq(1, len(result['users']))
    assertTrue(int(result['users'][0]['id']) > 0)
    assertEq('utest4inline', result['users'][0]['name'])
    assertEq('utest4inline@a.com', result['users'][0]['email'])

def go5TicketsUpdateMany():

    # test triggers
    pass
def go6TicketsShowMany():
    pass
def go7TicketsShowComments():
    pass
def go8Search():
    pass


def go():
    go1UsersCreateMany()
    go2UsersSearch()
    go3UsersShowMany()
    go4TicketsCreateMany()
    go5TicketsUpdateMany()
    go6TicketsShowMany()
    go7TicketsShowComments()
    go8Search()
    trace('\n\nall tests complete')


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
        assertTrue(not jsonData or not '%' in jsonData, "missing template?", jsonData)
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

def doTest1():
    #~ payload = '{"users":[{"name":"u1", "email":"a@b.com"}]}'
    payload = ' {"users": [{   "email": "utest1@a.com",   "name": "utest1"},{   "email": "utest2@a.com",   "name": "utest2"}]}'
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    r = doRequest('post', 'http://localhost:8999/api/v2/users/create_many.json', headers=headers, data=payload)
    trace('gottt', r.text)

    #~ r5 = sendImpl('post', '/api/v2/users/create_many.json', payload, None)
    #~ trace(r5)
    trace('r6')
    r6 = sendPost('/api/v2/users/create_many.json', payload)
    trace(r6)
    checkJobStatusOk(r6, 'queued')
    trace('r6b', r6['job_status']['url'])
    response = sendGet(r6['job_status']['url'])
    trace('r6c', response)
    checkJobStatusOk(response, 'completed')
    trace('r6d')
    
    trace('r7')
    output = sendPostAndGetJob('/api/v2/users/create_many.json', payload)
    trace('r7out', output)

#~ doTest1()
go()
#~ sendGet('/api/v2/users/show_many', 'ids=11007314541595')
