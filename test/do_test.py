
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
    ############## No results ###################
    result = sendGet('/api/v2/users/search', 'query=email:utest444@a.com')
    assertEq(0, result['count'])
    assertEq(0, len(result['users']))

    ############## One result ###################
    result = sendGet('/api/v2/users/search', 'query=email:utest3@a.com')
    assertEq(1, result['count'])
    assertEq(1, len(result['users']))
    assertTrue(int(result['users'][0]['id']) > 0)
    assertEq('utest3', result['users'][0]['name'])
    assertEq('utest3@a.com', result['users'][0]['email'])

    
def go3UsersShowMany():
    ############## No results ###################
    result = sendGet('/api/v2/users/show_many', f'ids=999')
    assertEq(0, len(result['users']))

    ############## One result ###################
    result = sendGet('/api/v2/users/show_many', f'ids={stateIds["user1"]}')
    assertEq(1, len(result['users']))
    assertEq(stateIds["user1"], result['users'][0]['id'])
    assertEq('utest1', result['users'][0]['name'])
    assertEq('utest1@a.com', result['users'][0]['email'])

    ############## Many results, skip missing ###################
    result = sendGet('/api/v2/users/show_many', f'ids={stateIds["user2"]},999,{stateIds["user3"]}')
    assertEq(2, len(result['users']))
    assertEq(stateIds["user2"], result['users'][0]['id'])
    assertEq('utest2', result['users'][0]['name'])
    assertEq('utest2@a.com', result['users'][0]['email'])
    assertEq(stateIds["user3"], result['users'][1]['id'])
    assertEq('utest3', result['users'][1]['name'])
    assertEq('utest3@a.com', result['users'][1]['email'])
    

def go4TicketsCreateMany():
    # author defaults
    #     requester set, author set (comment1)
    #     requester set, author not set but prev is (comment2)
    #     requester set, author not set (testAuthorId1)
    #     requester not set, author set  (testAuthorId2)
    #     requester not set, author not set but prev is (testAuthorId3)
    #     requester not set, author not set (plainStringComment2)
    s = r'''{
    "tickets": [
      {
        "subject": "ticket1",
        "description": "descr1",
        "created_at": "2022-01-01T06:38:32.399Z",
        "requester_id": %USER1%,
        "status": "pending", ### note ids are sometimes quoted, sometimes not, need to support both
        "custom_fields": [{"id":"345", "value":"fldval1"}, {"id":%FLDID%, "value":"fldval2"}],
        "tags": ["tag1", "tag2"],
        "comments": [
          {
            "created_at": "2022-01-02T06:38:32.399Z",
            "body": "comment1",
            "public": false,
            "author_id": %USER2%
          },
          {
            "created_at": "2022-01-03T06:38:32.399Z",
            "body": "comment2",
            "public": true
          }
        ]
      }, {
        "subject": "ticket2",
        "description": "descr2",
        "created_at": "2022-01-01T06:38:32.399Z",
        "requester": {"name":"utest4inline", "email": "utest4inline@a.com"}, ### inline user creation
        "tags": ["tag1", "tag2"],
        "comment": {"body": "plainStringComment1"} ### comment syntax shortcut, comment not comments
        ### status default to open
        ### comments default to public=true
      },
      {
        "description": "descr3", ### create a ticket with no subject and no requester
        "comment": "plainStringComment2" ### comment syntax shortcut, string data type
        "tags": ["tag1", "tag2"],
      },
      {
        "description": "descr4",
        "requester_id": %USER2%,
        "submitter_id": %USER3%,
        "comments": [{"body": "testAuthorId1"}]
      },
      {
        "description": "descr5",
        "comments": [{"body": "testAuthorId2", "author_id": "%USER1%"}, {"body": "testAuthorId3"}]
      },
      {
        "description": "descr6",
        "requester_id": %USER1%,
        "comments": [{"body": "testAuthorIdUpdate", "author_id": "%USER2%"}]
      }
    ]
  }
  '''
    s = subInTemplates(s)
    result = sendPostAndGetJob('/api/v2/imports/tickets/create_many', s)
    assertEq(6, len(result['results']))
    for i in range(6):
        assertEq(i, result['results'][i]['index'])
        stateIds[f'ticket{i+1}'] = int(result['results'][i]['id'])
        assertEq(True, result['results'][i]['success'])

    ############## Confirm inline user got created ###################
    result = sendGet('/api/v2/users/search', 'query=email:utest4inline@a.com')
    assertEq(1, result['count'])
    assertEq(1, len(result['users']))
    assertTrue(int(result['users'][0]['id']) > 0)
    assertEq('utest4inline', result['users'][0]['name'])
    assertEq('utest4inline@a.com', result['users'][0]['email'])
    stateIds['user4inline'] = int(result['users'][0]['id'])


def go5TicketsShowMany():
    ############## No results ###################
    result = sendGet('/api/v2/tickets/show_many', f'ids=999')
    assertEq(0, len(result['tickets']))

    ############## One result ###################
    result = sendGet('/api/v2/tickets/show_many', f'ids={stateIds["ticket1"]}')
    assertEq(1, len(result['tickets']))
    assertEq(stateIds["ticket1"], result['tickets'][0]['id'])
    assertEq('ticket1', result['tickets'][0]['subject'])

    ############## Many results, skip missing ###################
    result = sendGet('/api/v2/tickets/show_many', f'ids={stateIds["ticket2"]},999,{stateIds["ticket3"]}')
    assertEq(2, len(result['tickets']))
    assertEq(stateIds["ticket2"], result['tickets'][0]['id'])
    assertEq('ticket2', result['tickets'][0]['subject'])
    assertEq(stateIds["ticket3"], result['tickets'][1]['id'])
    assertEq('(no subject given)', result['tickets'][1]['subject'])

    ############## Thoroughly check data ###################
    result = sendGet('/api/v2/tickets/show_many', f'ids={stateIds["ticket1"]},{stateIds["ticket2"]},{stateIds["ticket3"]}')
    assertEq(3, len(result['tickets']))
    t1, t2, t3 = result['tickets']
    confirmSet(t1, 'id|created_at|updated_at|description'.split('|'))
    confirmSet(t2, 'id|created_at|updated_at|description'.split('|'))
    confirmSet(t3, 'id|created_at|updated_at|description'.split('|'))

    assertEq(stateIds["ticket1"], t1['id'])
    assertEq('ticket1', t1['subject'])
    assertEq('ticket1', t1['raw_subject'])
    assertEq('pending', t1['status'])
    assertEq(stateIds["user1"], t1['requester_id'])
    assertEq(stateIds["user1"], t1['submitter_id'])
    assertEq(stateIds["admin"], t1['assignee_id'])
    assertEq([], t1['tags'])
    assertEq([{'id': '345', 'value': 'fldval1'}, {'id': 1900006025624, 'value': 'fldval2'}], t1['custom_fields'])
    assertEq([], t1['fields'])
    assertEq(True, t1['is_public'])
    assertEq(2, len(t1['comment_ids']))

    assertEq(stateIds["ticket2"], t2['id'])
    assertEq('ticket2', t2['subject'])
    assertEq('ticket2', t2['raw_subject'])
    assertEq('open', t2['status'])
    assertEq(stateIds["user4inline"], t2['requester_id'])
    assertEq(stateIds["user4inline"], t2['submitter_id'])
    assertEq(stateIds["admin"], t2['assignee_id'])
    assertEq(["tag1", "tag2"], t2['tags'])
    assertEq([], t2['custom_fields'])
    assertEq([], t2['fields'])
    assertEq(True, t2['is_public'])
    assertEq(1, len(t2['comment_ids']))

    assertEq(stateIds["ticket3"], t3['id'])
    assertEq('(no subject given)', t3['subject'])
    assertEq('(no subject given)', t3['raw_subject'])
    assertEq('open', t3['status'])
    assertEq(stateIds["admin"], t3['requester_id'])
    assertEq(stateIds["admin"], t3['submitter_id'])
    assertEq(stateIds["admin"], t3['assignee_id'])
    assertEq([], t3['tags'])
    assertEq([], t3['custom_fields'])
    assertEq([], t3['fields'])
    assertEq(True, t3['is_public'])
    assertEq(1, len(t3['comment_ids']))


def go6TicketsShowComments():
    ############## No results ###################
    assertException(lambda: sendGet(f'/api/v2/tickets/999/comments'), Exception)

    ############## Result w 1 comment ###################
    result = sendGet(f'/api/v2/tickets/{stateIds["ticket2"]}/comments')
    assertEq(1, result['count'])
    assertEq(1, len(result['comments']))
    c = result['comments'][0]
    confirmSet(c, 'id|created_at|updated_at'.split('|'))
    assertEq('Comment', c['type'])
    assertEq('plainStringComment1', c['body'])
    assertEq('plainStringComment1', c['html_body'])
    assertEq('plainStringComment1', c['plain_body'])
    assertEq(True, c['public'])
    assertEq(stateIds['user4inline'], c['author_id'])
    assertEq([], c['attachments'])
    
    ############## Other result w 1 comment ###################
    result = sendGet(f'/api/v2/tickets/{stateIds["ticket3"]}/comments')
    assertEq(1, result['count'])
    assertEq(1, len(result['comments']))
    c = result['comments'][0]
    confirmSet(c, 'id|created_at|updated_at'.split('|'))
    assertEq('Comment', c['type'])
    assertEq('plainStringComment2', c['body'])
    assertEq('plainStringComment2', c['html_body'])
    assertEq('plainStringComment2', c['plain_body'])
    assertEq(True, c['public'])
    assertEq(stateIds['admin'], c['author_id'])
    assertEq([], c['attachments'])

    ############## Result w 2 comments ###################
    result = sendGet(f'/api/v2/tickets/{stateIds["ticket1"]}/comments')
    assertEq(2, result['count'])
    assertEq(2, len(result['comments']))
    c = result['comments'][0]
    confirmSet(c, 'id|created_at|updated_at'.split('|'))
    assertEq('Comment', c['type'])
    assertEq('comment1', c['body'])
    assertEq('comment1', c['html_body'])
    assertEq('comment1', c['plain_body'])
    assertEq(False, c['public'])
    assertEq(stateIds['user2'], c['author_id'])
    assertEq([], c['attachments'])

    c = result['comments'][1]
    confirmSet(c, 'id|created_at|updated_at'.split('|'))
    assertEq('Comment', c['type'])
    assertEq('comment2', c['body'])
    assertEq('comment2', c['html_body'])
    assertEq('comment2', c['plain_body'])
    assertEq(True, c['public'])
    assertEq(stateIds['user1'], c['author_id'])
    assertEq([], c['attachments'])

    ############## Test default authors ###################
    result1 = sendGet(f'/api/v2/tickets/{stateIds["ticket1"]}/comments')
    result3 = sendGet(f'/api/v2/tickets/{stateIds["ticket3"]}/comments')
    result4 = sendGet(f'/api/v2/tickets/{stateIds["ticket4"]}/comments')
    result5 = sendGet(f'/api/v2/tickets/{stateIds["ticket5"]}/comments')
    #           requester set, author set (comment1)
    assertEq('comment1', result1['comments'][0]['plain_body'])
    assertEq(stateIds['user2'], result1['comments'][0]['author_id'])
    #           requester set, author not set but prev is (comment2)
    assertEq('comment2', result1['comments'][1]['plain_body'])
    assertEq(stateIds['user1'], result1['comments'][1]['author_id'])
    #           requester set, author not set (testAuthorId1)
    assertEq('testAuthorId1', result4['comments'][0]['plain_body'])
    assertEq(stateIds['user2'], result4['comments'][0]['author_id'])
    #           requester not set, author set  (testAuthorId2)
    assertEq('testAuthorId2', result5['comments'][0]['plain_body'])
    assertEq(stateIds['user1'], result5['comments'][0]['author_id'])
    #           requester not set, author not set but prev is (testAuthorId3)
    assertEq('testAuthorId3', result5['comments'][1]['plain_body'])
    assertEq(stateIds['admin'], result5['comments'][1]['author_id'])
    #           requester not set, author not set (plainStringComment2)
    assertEq('plainStringComment2', result3['comments'][0]['plain_body'])
    assertEq(stateIds['admin'], result3['comments'][0]['author_id'])
    # look at tickets
    result = sendGet('/api/v2/tickets/show_many', f'ids={stateIds["ticket3"]},{stateIds["ticket4"]},{stateIds["ticket5"]}')
    assertEq(stateIds['admin'], result['tickets'][0]['requester_id'])
    assertEq(stateIds['admin'], result['tickets'][0]['submitter_id'])
    assertEq(stateIds['user2'], result['tickets'][1]['requester_id'])
    assertEq(stateIds['user3'], result['tickets'][1]['submitter_id'])
    assertEq(stateIds['admin'], result['tickets'][2]['requester_id'])
    assertEq(stateIds['admin'], result['tickets'][2]['submitter_id'])


def go7TicketsUpdateMany():
    # change requesterid and assignerid and status
    # post comment without an author id, where prev comment != requesterid != admin
    # additionaltags should remove duplicates
    # removetags should remove duplicates
    # settags should replace existing and remove duplicates

    # custom fields should merge in changes, not replace
    s = ''' {
    "tickets": [
      {
        "id": %TICKET1%,
        "status": "pending",
        "comment": 
        {
            "body": "add another",
            "public": true,
            "author_id": 111
        },
        "custom_fields" : [{"id":123, "value":"addthis"}, {"id":345, "value":"changethis"}]
      }
    ]
  }
    '''
    s = subInTemplates(s)


    # test if defaults to requester or admin
    # test triggers
    pass

def go8Search():
    pass



def go():
    go1UsersCreateMany()
    go2UsersSearch()
    go3UsersShowMany()
    go4TicketsCreateMany()
    go5TicketsShowMany()
    go6TicketsShowComments()
    go7TicketsUpdateMany()
    go8Search()
    trace('\n\nall tests complete')


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
        assertTrue(not jsonData or not '%' in jsonData, "missing template?", jsonData)
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
