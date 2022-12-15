
from ben_python_common import *
import requests
import json
import urllib.parse

from do_test_helpers import *



def go1UsersCreateMany():
    #~ if not getInputBool('OK to run this test, which will reset all tickets+users?'):
        #~ assertTrue(False, 'cancelling test')
    
    ############## Reset state ###################
    sendPost('/api/delete_all', {})

    ############## Invalid input ###################
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

    testBatchResults(result, hasSuccess=True, action='create', status='Created')
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
    expectedAction = lambda i: 'update' if i==0 else 'create'
    expectedStatus = lambda i: 'Updated' if i==0 else 'Created'
    testBatchResults(result, hasSuccess=True, action=expectedAction, status=expectedStatus)
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

    # note that if comment isn't set, zendesk api will ask for a 'description',
    # this is misleading because a description passed in will also create a first comment.
    s = r'''{
    "tickets": [
      {
        "subject": "ticket1",
        "created_at": "2022-01-01T06:38:32.399Z",
        "requester_id": %USER1%,
        "status": "pending", ### note ids are sometimes quoted, sometimes not, need to support both
        "custom_fields": [{"id":"%FLDID1%", "value":"fldval1"}, {"id":%FLDID2%, "value":"fldval2"}],
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
        "created_at": "2022-01-01T06:38:32.399Z",
        "requester": {"name":"utest4inline", "email": "utest4inline@a.com"}, ### inline user creation
        "tags": ["tag1", "tag2"],
        "comment": {"body": "plainStringComment1"} ### comment syntax shortcut, comment not comments
        ### status default to open
        ### comments default to public=true
      },
      {
        "comment": "plainStringComment2", ### comment syntax shortcut, string data type
        "tags": ["tag1", "tag2", "%TAG_REMOVED_BY_TRIGGER%"] ### we'll remove it
      },
      {
        "requester_id": %USER2%,
        "submitter_id": %USER3%,
        "comments": [{"body": "testAuthorId1"}]
      },
      {
        "comments": [{"body": "testAuthorId2", "author_id": "%USER1%"}, {"body": "testAuthorId3"}]
      },
      {
        "requester_id": %USER1%,
        "comments": [{"body": "testAuthorIdUpdate", "author_id": "%USER2%"}],
        "tags": ["%TAG_REMOVED_BY_TRIGGER%"] ### we won't remove it because we'll add a private comment
      }
    ]
  }'''

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
    allIds = ','.join(str(stateIds[f'ticket{i}']) for i in range(1,7))
    result = sendGet('/api/v2/tickets/show_many', f'ids={allIds}')
    t1, t2, t3, t4, t5, t6 = result['tickets']
    assertEq(6, len(result['tickets']))
    for i in range(6):
        stateIds[f'lastUpdateTicket{i+1}'] = result['tickets'][i]['updated_at']
        confirmSet(result['tickets'][i], 'id|created_at|updated_at|description'.split('|'))
    

    expectedCustomFlds = [{'id': int(subInTemplates('%FLDID1%')), 'value': 'fldval1'}, {'id': int(subInTemplates('%FLDID2%')), 'value': 'fldval2'}]
    assertEq(stateIds["ticket1"], t1['id'])
    assertEq('ticket1', t1['subject'])
    assertEq('ticket1', t1['raw_subject'])
    assertEq('pending', t1['status'])
    assertEq(stateIds["user1"], t1['requester_id'])
    assertEq(stateIds["user1"], t1['submitter_id'])
    assertEq(stateIds["admin"], t1['assignee_id'])
    assertTagsEq(["tag1", "tag2"], t1['tags'])
    assertCustomFieldsEq(expectedCustomFlds,  t1['custom_fields'])
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
    assertTagsEq(["tag1", "tag2"], t2['tags'])
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
    assertTagsEq(["tag1", "tag2", subInTemplates('%TAG_REMOVED_BY_TRIGGER%')], t3['tags'])
    assertEq([], t3['custom_fields'])
    assertEq([], t3['fields'])
    assertEq(True, t3['is_public'])
    assertEq(1, len(t3['comment_ids']))

    assertEq(stateIds["ticket6"], t6['id'])
    assertEq('(no subject given)', t6['subject'])
    assertEq('(no subject given)', t6['raw_subject'])
    assertEq('open', t6['status'])
    assertEq(stateIds["user1"], t6['requester_id'])
    assertEq(stateIds["user1"], t6['submitter_id'])
    assertEq(stateIds["admin"], t6['assignee_id'])
    assertTagsEq([subInTemplates('%TAG_REMOVED_BY_TRIGGER%')], t6['tags'])
    assertEq([], t6['custom_fields'])
    assertEq([], t6['fields'])
    assertEq(True, t6['is_public'])
    assertEq(1, len(t6['comment_ids']))



def go6TicketsShowComments():
    ############## No results ###################
    assertException(lambda: sendGet(f'/api/v2/tickets/999/comments'), Exception)

    ############## Result w 1 comment ###################
    result2 = sendGet(f'/api/v2/tickets/{stateIds["ticket2"]}/comments')
    assertEq(1, result2['count'])
    assertEq(1, len(result2['comments']))
    
    ############## Other result w 1 comment ###################
    result3 = sendGet(f'/api/v2/tickets/{stateIds["ticket3"]}/comments')
    assertEq(1, result3['count'])
    assertEq(1, len(result3['comments']))

    ############## Result w 2 comments ###################
    result1 = sendGet(f'/api/v2/tickets/{stateIds["ticket1"]}/comments')
    assertEq(2, result1['count'])
    assertEq(2, len(result1['comments']))

    ############## Test ticket contents ###################
    testComment(result2['comments'][0], authorId=stateIds['user4inline'], text='plainStringComment1')
    testComment(result3['comments'][0], authorId=stateIds['admin'], text='plainStringComment2')
    testComment(result1['comments'][0], authorId=stateIds['user2'], text='comment1', public=False)
    testComment(result1['comments'][1], authorId=stateIds['user1'], text='comment2')

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
    s = r'''{
    "tickets": [
      {
        "id": %TICKET1%,
        "status": "solved", ### will be overridden by trigger
        "requester_id": %USER2%,
        "submitter_id": %USER1%,
        "tags": ["tag2", "tag3", "tag2"], ### replace existing tags, remove dupes 
        "custom_fields": [{"id": %FLDID3%, "value":"fldval3_b"}, {"id": %FLDID2%, "value":"fldval2_b"}], ### this merges in
        "comment": {"body": "a %TEXT_NOTICED_BY_TRIGGER% b"} ### comment without an author id, requester is being changed
        ### trigger openPostWhenPublicCommentContainingTextPosted should fire
      },
      {
        "id": "%TICKET2%", ### support quoted ids
        "status": "solved",
        "additional_tags": ["tag2", "tag3", "tag2"], ### merge existing tags, remove dupes 
        "custom_fields": [{"id": "%FLDID2%", "value":"new"}] ### setting new flds, and quoted ids should work
      },
      {
        "id": %TICKET3%,
        "remove_tags": ["tag2", "tag3", "tag2"], ### remove existing tags
        "comment": {"body": "addedCommentOn3", "author_id":%USER1%} ### comment with an author id
      },
      {
        "id": %TICKET6%,
        ### adding a private comment, so removeTagWhenPublicCommentPosted trigger should not fire
        "comment": {"body": "addedCommentOn6", "public": false} ### comment without an author id, where prev comment != requesterid != admin
      }
    ]
  }'''

    s = subInTemplates(s)
    result = sendPostAndGetJob('/api/v2/tickets/update_many', s)
    assertEq(4, len(result['results']))
    assertEq(stateIds[f'ticket1'], result['results'][0]['id'])
    assertEq(stateIds[f'ticket2'], result['results'][1]['id'])
    assertEq(stateIds[f'ticket3'], result['results'][2]['id'])
    assertEq(stateIds[f'ticket6'], result['results'][3]['id'])
    for i, item in enumerate(result['results']):
        assertEq(i, item['index'])
        assertEq('update', item['action'])
        assertEq('Updated', item['status'])
        assertEq(True, item['success'])


    allIds = ','.join(str(stateIds[f'ticket{i}']) for i in range(1,7))
    afterMods = sendGet('/api/v2/tickets/show_many', f'ids={allIds}')
    t1, t2, t3, t4, t5, t6 = afterMods['tickets']
    assertEq(6, len(afterMods['tickets']))

    ### confirm last_updated was bumped
    for i in range(1, 7):
        assertEq(stateIds[f'ticket{i}'], afterMods['tickets'][i-1]['id'])
        modded = str(i) in '1,2,3,6'.split(',')
        wasUpdateBumped = stateIds[f'lastUpdateTicket{i}'] != afterMods['tickets'][i-1]['updated_at']
        assertEq(modded, wasUpdateBumped)

    ### test the assertCustomFieldsEq helper
    assertCustomFieldsEq([{'id':1, 'value':'a'}, {'id':2, 'value':'b'}], [{'id':1, 'value':'a'}, {'id':2, 'value':'b'}])
    assertCustomFieldsEq([{'id':1, 'value':'a'}, {'id':2, 'value':'b'}], [{'id':2, 'value':'b'}, {'id':1, 'value':'a'}])
    assertException(lambda: assertCustomFieldsEq([{'id':1, 'value':'a'}, {'id':2, 'value':'b'}], [{'id':2, 'value':'b'}, {'id':1, 'value':'c'}]), Exception)

    ### test ticket 1
    assertEq(stateIds["ticket1"], t1['id'])
    assertEq('ticket1', t1['subject'])
    assertEq('ticket1', t1['raw_subject'])
    assertEq('open', t1['status']) # set by trigger
    assertEq(stateIds["user2"], t1['requester_id'])
    assertEq(stateIds["user1"], t1['submitter_id'])
    assertEq(stateIds["admin"], t1['assignee_id'])
    assertTagsEq(["tag2", "tag3"], t1['tags']) # tags were modified
    expectedCustomFlds = [{'id': int(subInTemplates('%FLDID1%')), 'value': 'fldval1'}, 
        {'id': int(subInTemplates('%FLDID2%')), 'value': 'fldval2_b'}, 
        {'id': int(subInTemplates('%FLDID3%')), 'value': 'fldval3_b'}]
    assertCustomFieldsEq(expectedCustomFlds, 
        t1['custom_fields'])
    assertEq([], t1['fields'])
    assertEq(True, t1['is_public'])
    assertEq(3, len(t1['comment_ids']))
    comments1 = sendGet(f'/api/v2/tickets/{t1["id"]}/comments')['comments']
    assertEq(3, len(comments1))
    testComment(comments1[0], authorId=stateIds['user2'], text='comment1', public=False)
    testComment(comments1[1], authorId=stateIds['user1'], text='comment2')
    testComment(comments1[2], authorId=stateIds['user2'], text=subInTemplates('a %TEXT_NOTICED_BY_TRIGGER% b'))

    ### test ticket 2
    assertEq(stateIds["ticket2"], t2['id'])
    assertEq('ticket2', t2['subject'])
    assertEq('ticket2', t2['raw_subject'])
    assertEq('solved', t2['status'])
    assertEq(stateIds["user4inline"], t2['requester_id'])
    assertEq(stateIds["user4inline"], t2['submitter_id'])
    assertEq(stateIds["admin"], t2['assignee_id'])
    assertTagsEq(["tag1", "tag2", "tag3"], t2['tags'])
    expectedCustomFlds =  [{'id': int(subInTemplates('%FLDID2%')), 'value': 'new'}]
    assertCustomFieldsEq(expectedCustomFlds, 
        t2['custom_fields'])
    assertEq([], t2['fields'])
    assertEq(True, t2['is_public'])
    assertEq(1, len(t2['comment_ids']))
    comments2 = sendGet(f'/api/v2/tickets/{t2["id"]}/comments')['comments']
    assertEq(1, len(comments2))
    testComment(comments2[0], authorId=stateIds['user4inline'], text='plainStringComment1')

    ### test ticket 3
    assertEq(stateIds["ticket3"], t3['id'])
    assertEq('(no subject given)', t3['subject'])
    assertEq('(no subject given)', t3['raw_subject'])
    assertEq('open', t3['status'])
    assertEq(stateIds["admin"], t3['requester_id'])
    assertEq(stateIds["admin"], t3['submitter_id'])
    assertEq(stateIds["admin"], t3['assignee_id'])
    assertTagsEq(["tag1"], t3['tags']) # removed by remove_tags and by trigger
    assertEq([], t3['custom_fields'])
    assertEq([], t3['fields'])
    assertEq(True, t3['is_public'])
    assertEq(2, len(t3['comment_ids']))
    comments3 = sendGet(f'/api/v2/tickets/{t3["id"]}/comments')['comments']
    assertEq(2, len(comments3))
    testComment(comments3[0], authorId=stateIds['admin'], text='plainStringComment2')
    testComment(comments3[1], authorId=stateIds['user1'], text='addedCommentOn3')

    ### test ticket 6
    assertEq(stateIds["ticket6"], t6['id'])
    assertEq('(no subject given)', t6['subject'])
    assertEq('(no subject given)', t6['raw_subject'])
    assertEq('open', t6['status'])
    assertEq(stateIds["user1"], t6['requester_id'])
    assertEq(stateIds["user1"], t6['submitter_id'])
    assertEq(stateIds["admin"], t6['assignee_id'])
    assertTagsEq([subInTemplates('%TAG_REMOVED_BY_TRIGGER%')], t6['tags']) # trigger won't fire because it's a private post
    assertEq([], t6['custom_fields'])
    assertEq([], t6['fields'])
    assertEq(True, t6['is_public'])
    assertEq(2, len(t6['comment_ids']))
    comments6 = sendGet(f'/api/v2/tickets/{t6["id"]}/comments')['comments']
    assertEq(2, len(comments6))
    testComment(comments6[0], authorId=stateIds['user2'], text='testAuthorIdUpdate')
    testComment(comments6[1], authorId=stateIds['user1'], text='addedCommentOn6', public=False)
    

def go8Search():
    s = r'''{
    "tickets": [
      {
        ### create ticket: open/no tag/no fld1/no fld2/fld3=target = isThere 
        "created_at": "2022-04-01T06:38:32.399Z",
        "subject": "t1",
        "status": "open",
        "custom_fields": [
            {"id":%FLDID3%, "value":"includeTicketsWhereFld3SaysThis"}
        ],
        "tags": [],
        "comment": {"body": "t1"}
      },
      {
        ### create ticket: no conditions match = filtered out  
        "created_at": "2022-04-02T06:38:32.399Z",
        "subject": "t2",
        "status": "closed",
        "custom_fields": [
            {"id":%FLDID1%, "value":"skipTicketsWhereFld1SaysThis"},
            {"id":%FLDID2%, "value":"skipTicketsWhereFld2SaysThis"},
            {"id":%FLDID3%, "value":"notTheLookedForValue"}
        ],
        "tags": ["%TAG_REMOVED_BY_TRIGGER%"],
        "comment": {"body": "t2"}
      },
      {
        ### create ticket: closed(wrong)/no tag/fld1=different/fld2=different/fld3=target = filtered out 
        "created_at": "2022-04-03T06:38:32.399Z",
        "subject": "t3",
        "status": "closed",
        "custom_fields": [
            {"id":%FLDID1%, "value":"differentVal1"},
            {"id":%FLDID2%, "value":"differentVal2"},
            {"id":%FLDID3%, "value":"includeTicketsWhereFld3SaysThis"}
        ],
        "tags": ["searchTag1", "searchTag2"],
        "comment": {"body": "t3"}
      },
      {
        ### create ticket: open/tag(wrong)/fld1=different/fld2=different/fld3=target = filtered out  
        "created_at": "2022-04-04T06:38:32.399Z",
        "subject": "t4",
        "status": "open",
        "custom_fields": [
            {"id":%FLDID1%, "value":"differentVal1"},
            {"id":%FLDID2%, "value":"differentVal2"},
            {"id":%FLDID3%, "value":"includeTicketsWhereFld3SaysThis"}
        ],
        "tags": ["searchTag1", "searchTag2", "%TAG_REMOVED_BY_TRIGGER%"],
        "comment": {"body": "t4"}
      },
      {
        ### create ticket: open/no tag/fld1=skip/fld2=different/fld3=target = filtered out  
        "created_at": "2022-04-05T06:38:32.399Z",
        "subject": "t5",
        "status": "open",
        "custom_fields": [
            {"id":%FLDID1%, "value":"skipTicketsWhereFld1SaysThis"},
            {"id":%FLDID2%, "value":"differentVal2"},
            {"id":%FLDID3%, "value":"includeTicketsWhereFld3SaysThis"}
        ],
        "tags": ["searchTag1", "searchTag2"],
        "comment": {"body": "t5"}
      },
      {
        ### create ticket: open/no tag/fld1=different/fld2=skip/fld3=target = filtered out  
        "created_at": "2022-04-06T06:38:32.399Z",
        "subject": "t6",
        "status": "open",
        "custom_fields": [
            {"id":%FLDID1%, "value":"differentVal1"},
            {"id":%FLDID2%, "value":"skipTicketsWhereFld2SaysThis"},
            {"id":%FLDID3%, "value":"includeTicketsWhereFld3SaysThis"}
        ],
        "tags": ["searchTag1", "searchTag2"],
        "comment": {"body": "t6"}
      },
      {
        ### create ticket: open/no tag/fld1=different/fld2=different/fld3=other(wrong) = filtered out  
        "created_at": "2022-04-07T06:38:32.399Z",
        "subject": "t7",
        "status": "open",
        "custom_fields": [
            {"id":%FLDID1%, "value":"differentVal1"},
            {"id":%FLDID2%, "value":"differentVal2"},
            {"id":%FLDID3%, "value":"notTheLookedForValue"}
        ],
        "tags": ["searchTag1", "searchTag2"],
        "comment": {"body": "t7"}
      }
    ]
    }'''
    s = subInTemplates(s)
    result = sendPostAndGetJob('/api/v2/imports/tickets/create_many', s)
    assertEq(7, len(result['results']))
    for i in range(7):
        assertEq(i, result['results'][i]['index'])
        stateIds[f'ticketTestSearch{i+1}'] = int(result['results'][i]['id'])
        assertEq(True, result['results'][i]['success'])
    
    s = r'''{
    "tickets": [
     {
        ### create ticket: open/no tag/fld1=different/fld2=different/fld3=target = isThere 
        "created_at": "2022-04-08T06:38:32.399Z",
        "subject": "t8",
        "status": "open",
        "custom_fields": [
            {"id":%FLDID1%, "value":"differentVal1"},
            {"id":%FLDID2%, "value":"differentVal2"},
            {"id":%FLDID3%, "value":"includeTicketsWhereFld3SaysThis"}
        ],
        "tags": ["searchTag1"],
        "comment": {"body": "t8"}
      }
    ]
    }'''
    s = subInTemplates(s)
    result = sendPostAndGetJob('/api/v2/imports/tickets/create_many', s)
    assertEq(1, len(result['results']))
    for i in range(1):
        assertEq(i, result['results'][i]['index'])
        stateIds[f'ticketTestSearch8'] = int(result['results'][i]['id'])
        assertEq(True, result['results'][i]['success'])

    ####### simple search ################
    clauses = [f'custom_field_%FLDID3%:notTheLookedForValue']
    q = f'query=' + quote(subInTemplates(" ".join(clauses))) + '&sort_by=created_at&sort_order=asc'
    result = sendGet('/api/v2/search', q)
    assertEq(2, result['count'])
    assertEq(stateIds['ticketTestSearch2'], result['results'][0]['id'])
    assertEq(stateIds['ticketTestSearch7'], result['results'][1]['id'])
    
    ####### tags search ################
    clauses = [f'tags:searchTag1', f'tags:searchTag2']
    q = f'query=' + quote(subInTemplates(" ".join(clauses))) + '&sort_by=created_at&sort_order=asc'
    result = sendGet('/api/v2/search', q)
    assertEq(6, result['count'])
    assertEq(stateIds['ticketTestSearch3'], result['results'][0]['id'])
    assertEq(stateIds['ticketTestSearch4'], result['results'][1]['id'])
    assertEq(stateIds['ticketTestSearch5'], result['results'][2]['id'])
    assertEq(stateIds['ticketTestSearch6'], result['results'][3]['id'])
    assertEq(stateIds['ticketTestSearch7'], result['results'][4]['id'])
    assertEq(stateIds['ticketTestSearch8'], result['results'][5]['id'])
    
    ####### complex search ################
    clauses = ['-status:closed', 
        '-tags:%TAG_REMOVED_BY_TRIGGER%', 
        '-custom_field_%FLDID1%:skipTicketsWhereFld1SaysThis', 
        '-custom_field_%FLDID2%:skipTicketsWhereFld2SaysThis', 
        'custom_field_%FLDID3%:includeTicketsWhereFld3SaysThis', 
        ]
    q = f'query=' + quote(subInTemplates(" ".join(clauses))) + '&sort_by=created_at&sort_order=desc'
    result = sendGet('/api/v2/search', q)
    assertEq(2, result['count'])
    assertEq(stateIds['ticketTestSearch8'], result['results'][0]['id'])
    assertEq(stateIds['ticketTestSearch1'], result['results'][1]['id'])


def go():
    setupStateIds()
    go1UsersCreateMany()
    trace('yay')
    return
    go2UsersSearch()
    go3UsersShowMany()
    go4TicketsCreateMany()
    go5TicketsShowMany()
    go6TicketsShowComments()
    go7TicketsUpdateMany()
    go8Search()
    trace('\n\nall tests complete')



#~ doTest1()
go()
#~ sendGet('/api/v2/users/show_many', 'ids=11007314541595')
