
from ben_python_common import *
import json
import urllib.parse

configText = files.readall('configs.json')
configs = json.loads(configText)

# we support with+without .json suffix on all endpoints,
# so run tests twice, once with this True, and once with it False 
doWithJson = True

host = ''
#~ stateIds = dict(
    #~ user1 = 11007294636571,
    #~ user2 = 11007299217179,
    #~ user3 = 11007314541595,
#~ )
host = f'localhost:{configs["portNumber"]}'
stateIds = dict(
    user1 = None,
    user2 = None,
    user3 = None,
)


def go1UsersCreateMany():
    if not getInputBool('OK to run this test, which will reset all tickets+users?'):
        assertTrue(False, 'cancelling test')
    
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
    assertException(lambda: sendPost('/api/users/create_many', s), Exception)

    # email is required
    s = r'''{"users": [
{
   "name": "utest1"
}]}'''
    assertException(lambda: sendPost('/api/users/create_many', s), Exception)

    
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
    result = sendPostAndGetJob('/api/users/create_many', template)
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
    result = sendPostAndGetJob('/api/users/create_many', template)
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
    pass
def go3UsersShowMany():
    pass
def go4TicketsCreateMany():
    pass
def go5TicketsUpdateMany():
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
    return
    
    template = r'''{
    "tickets": [
      {
        "subject": "ticket1",
        "created_at": "2022-01-01T06:38:32.399Z",
        "requester_id": %USER1%,
        "custom_fields": [{"id":345, "value":"fldval1"}, {"id":%FLDID%, "value":"fldval2"}],
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
      }
    ]
  }
  '''
    customFlds = configs['customFields']
    firstCustomFld = list(customFlds.keys())[0]
    s = template.replace('%FLDID%', customFlds[firstCustomFld])
    s = template.replace('%USER1%', user1)
    sendPost()

def quote(s):
    return urllib.parse.quote(s)

def sendGet(endpoint, encodedQueryString=None):
    args = []
    args.append('curl')
    args.append('--fail-with-body')
    if encodedQueryString:
        encodedQueryString = '?' + encodedQueryString
    args.append(f'{host}{endpoint}{encodedQueryString}')
    return runAndShow(args)

def runAndShow(args):
    argsWithQuotes = jslike.map(args, lambda s: "'"+s+"'")
    argsWithQuotes[0] = 'curl'
    trace('Running:', '  '.join(argsWithQuotes).replace('\n', ''))
    ret, stdout, stderr = files.run(args)
    trace('||', stdout, '||')
    parsed = json.loads(stdout)
    return parsed


def sendPost(endpoint, jsonData):
    if not endpoint.endswith('delete_all'):
        if not doWithJson:
            if endpoint.endswith('.json'):
                endpoint = endpoint.replace('.json', '')
        else:
            if not endpoint.endswith('.json'):
                endpoint += '.json'

    jsonDataS = json.dumps(jsonData) if isinstance(jsonData, dict) else jsonData
    assertTrue(not '%' in jsonDataS, "missing template?", jsonDataS)
    global configs
    args = []
    args.append('curl')
    args.append('--fail-with-body')
    args.append('-d')
    args.append(jsonDataS)
    args.extend(f'-H|Content-Type: application/json|-X|POST|{host}{endpoint}'.split('|'))
    return runAndShow(args)


def sendPostAndGetJob(endpoint, jsonData):
    jobStatus = sendPost(endpoint, jsonData)
    checkJobStatusOk(jobStatus, 'queued')
    response = sendGet(jobStatus['url'])
    checkJobStatusOk(response, 'completed')
    return response
    
    
def checkJobStatusOk(response, expectedStatus):
    assertEq(expectedStatus, response['job_status']['status'])
    theId = response['job_status']['id']
    theUrl = response['job_status']['url']
    assertTrue(response['url'].endswith('/api/v2/job_statuses/'+theId+'.json'))
    
    if expectedStatus == 'completed':
        assertTrue(int(response['job_status']['total']) > 0)
        assertTrue(int(response['job_status']['progress']) > 0)
        assertTrue(len(response['job_status']['message']) > 0)

    else:
        assertTrue(int(response['job_status']['total']) == None)
        assertTrue(int(response['job_status']['progress']) == None)
        assertTrue(len(response['job_status']['message']) == None)


go()
#~ sendGet('/api/v2/users/show_many', 'ids=11007314541595')
