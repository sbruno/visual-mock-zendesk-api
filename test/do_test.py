
from ben_python_common import *
import json

configText = files.readall('configs.json')
configs = json.loads(configText)

# replace these as needed
user1 = 11007294636571
user2 = 11007299217179
user3 = 11007314541595

'''
Can place this in persistedGlobalState.json
"11007294636571": {
   "id": 11007294636571,
   "created_at": "2022-06-06T20:37:23.284Z",
   "email": "utest1@a.com",
   "name": "utest1"
},
"11007299217179": {
   "id": 11007299217179,
   "created_at": "2022-06-06T20:37:23.284Z",
   "email": "utest2@a.com",
   "name": "utest2"
},
"11007314541595": {
   "id": 11007314541595,
   "created_at": "2022-06-06T20:37:23.284Z",
   "email": "utest3@a.com",
   "name": "utest3"
},
'''

def go():
    
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


def sendPost(endpoint, jsonData):
    jsonDataS = json.dumps(jsonData)
    assertTrue(not '%' in jsonDataS, "missing template?", jsonDataS)
    global configs
    args = []
    args.push('curl')
    args.push('-d')
    args.push(jsonDataS)
    args.extend(f'-H|Content-Type: application/json|-X|POST|localhost:{configs["customFields"]}{endpoint}'.split('|'))
    trace('Running,' args)
    files.run(args)

go()
