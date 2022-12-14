
'''
in reality imports/tickets doesn't accept comment:"abc"
x-zendesk-api-warn = {:allowed_parameters=>{:controller=>"tickets", :action=>"create_many", :unpermitted_keys=>[], :invalid_values=>["tickets.2.comment"]}}
x-zendesk-api-warn = {:allowed_parameters=>{:controller=>"tickets", :action=>"create_many", :unpermitted_keys=>[], :invalid_values=>["tickets.1.comment", "tickets.2.comment"]}}

How to set this up
1) run tests and log each send() call, logging endpoint and body and saving to a text file
2) in that text file, replace the generated ids with real ids.
# use the calls to users/show_many to see what the test user ids are, then search/replace with real ids
# use the calls to tickets/create_many to see what the test custom flds are, then search/replace with real custom flds
#~ admin = 10981611611675,
#~ user1 = 11007294636571,
#~ user2 = 11007299217179,
#~ user3 = 11007314541595,
#~ fld1=10993199398427,
#~ fld2=10993238892315,
#~ fld3=11130845293467,

'''

def getSimulated():
    simulatedResponses = [
    '''
    Error: cannot pass in id
    ''',
    
    '''
    Error: missing email
    ''',
    
    '''
{
  "job_status": {
    "id": "111e0b044094f0c67893ac9fe64f1a99",
    "progress": null, "total": null, "message": null, "status": "completed",
    "url": "https://example.zendesk.com/api/v2/job_statuses/111e0b0467893ac9fe64f1a99.json"
  }
}
    ''',
    
    # some guesswork here since trial responds with 403 on the call
    '''
{
  "job_status": {
    "id": "111e0b044094f0c67893ac9fe64f1a99",
    "message": "Completed at 2018-03-08 10:07:04 +0000",
    "progress": 2,
    "results": [
      {
        "action": "create",
        "id": 11007294636571,
        "status": "Created",
        "success": true
      },
      {
        "action": "create",
        "id": 11007299217179,
        "status": "Created",
        "success": true
      }
    ],
    "status": "completed",
    "total": 2,
    "url": "https://example.zendesk.com/api/v2/job_statuses/111e0b0467893ac9fe64f1a99.json"
  }
}
    ''',

    '''
{
  "job_status": {
    "id": "222e0b044094f0c67893ac9fe64f1a99",
    "progress": null, "total": null, "message": null, "status": "completed",
    "url": "https://example.zendesk.com/api/v2/job_statuses/222e0b0467893ac9fe64f1a99.json"
  }
}
    ''',
    
    # some guesswork here since trial responds with 403 on the call
    # but shouldn't be risky to accept existing IDs
    '''
{
  "job_status": {
    "id": "222e0b044094f0c67893ac9fe64f1a99",
    "message": "Completed at 2018-03-08 10:07:04 +0000",
    "progress": 2,
    "results": [
      {
        "action": "update",
        "id": 11007294636571,
        "status": "Updated",
        "success": true
      },
      {
        "action": "create",
        "id": 11007314541595,
        "status": "Created",
        "success": true
      }
    ],
    "status": "completed",
    "total": 2,
    "url": "https://example.zendesk.com/api/v2/job_statuses/222e0b0467893ac9fe64f1a99.json"
  }
}
    ''',
    
    '''
{
  "count": 0,
  "next_page": null,
  "previous_page": null,
  "users": []
}
    ''',
    
    '''
{
  "count": 1,
  "next_page": null,
  "previous_page": null,
  "users": [
    {
      "active": true,
      "alias": "",
      "created_at": "2022-12-06T22:52:42Z",
      "custom_role_id": null,
      "default_group_id": null,
      "details": "",
      "email": "utest3@a.com",
      "external_id": null,
      "iana_time_zone": "America/Los_Angeles",
      "id": 11007314541595,
      "last_login_at": null,
      "locale": "en-US",
      "locale_id": 1,
      "moderator": false,
      "name": "utest3",
      "notes": "",
      "only_private_comments": false,
      "organization_id": null,
      "phone": null,
      "photo": null,
      "report_csv": false,
      "restricted_agent": true,
      "role": "end-user",
      "role_type": null,
      "shared": false,
      "shared_agent": false,
      "shared_phone_number": null,
      "signature": null,
      "suspended": false,
      "tags": [],
      "ticket_restriction": "requested",
      "time_zone": "America/Los_Angeles",
      "two_factor_auth_enabled": false,
      "updated_at": "2022-12-06T23:50:21Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/users/11007314541595.json",
      "user_fields": {},
      "verified": false
    }
  ]
}
    ''',
    
    '''
{
  "count": 0,
  "next_page": null,
  "previous_page": null,
  "users": []
}

    ''',
    
    '''
{
  "count": 1,
  "next_page": null,
  "previous_page": null,
  "users": [
    {
      "active": true,
      "alias": null,
      "created_at": "2022-12-06T22:52:17Z",
      "custom_role_id": null,
      "default_group_id": null,
      "details": null,
      "email": "utest1@a.com",
      "external_id": null,
      "iana_time_zone": "America/Los_Angeles",
      "id": 11007294636571,
      "last_login_at": null,
      "locale": "en-US",
      "locale_id": 1,
      "moderator": false,
      "name": "utest1",
      "notes": null,
      "only_private_comments": false,
      "organization_id": null,
      "phone": null,
      "photo": null,
      "report_csv": false,
      "restricted_agent": true,
      "role": "end-user",
      "role_type": null,
      "shared": false,
      "shared_agent": false,
      "shared_phone_number": null,
      "signature": null,
      "suspended": false,
      "tags": [],
      "ticket_restriction": "requested",
      "time_zone": "America/Los_Angeles",
      "two_factor_auth_enabled": false,
      "updated_at": "2022-12-06T22:52:17Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/users/11007294636571.json",
      "user_fields": {},
      "verified": false
    }
  ]
}
    ''',
    
    '''
{
  "count": 2,
  "next_page": null,
  "previous_page": null,
  "users": [
    {
      "active": true,
      "alias": null,
      "created_at": "2022-12-06T22:52:30Z",
      "custom_role_id": null,
      "default_group_id": null,
      "details": null,
      "email": "utest2@a.com",
      "external_id": null,
      "iana_time_zone": "America/Los_Angeles",
      "id": 11007299217179,
      "last_login_at": null,
      "locale": "en-US",
      "locale_id": 1,
      "moderator": false,
      "name": "utest2",
      "notes": null,
      "only_private_comments": false,
      "organization_id": null,
      "phone": null,
      "photo": null,
      "report_csv": false,
      "restricted_agent": true,
      "role": "end-user",
      "role_type": null,
      "shared": false,
      "shared_agent": false,
      "shared_phone_number": null,
      "signature": null,
      "suspended": false,
      "tags": [],
      "ticket_restriction": "requested",
      "time_zone": "America/Los_Angeles",
      "two_factor_auth_enabled": false,
      "updated_at": "2022-12-06T22:52:30Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/users/11007299217179.json",
      "user_fields": {},
      "verified": false
    },
    {
      "active": true,
      "alias": "",
      "created_at": "2022-12-06T22:52:42Z",
      "custom_role_id": null,
      "default_group_id": null,
      "details": "",
      "email": "utest3@a.com",
      "external_id": null,
      "iana_time_zone": "America/Los_Angeles",
      "id": 11007314541595,
      "last_login_at": null,
      "locale": "en-US",
      "locale_id": 1,
      "moderator": false,
      "name": "utest3",
      "notes": "",
      "only_private_comments": false,
      "organization_id": null,
      "phone": null,
      "photo": null,
      "report_csv": false,
      "restricted_agent": true,
      "role": "end-user",
      "role_type": null,
      "shared": false,
      "shared_agent": false,
      "shared_phone_number": null,
      "signature": null,
      "suspended": false,
      "tags": [],
      "ticket_restriction": "requested",
      "time_zone": "America/Los_Angeles",
      "two_factor_auth_enabled": false,
      "updated_at": "2022-12-06T23:50:21Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/users/11007314541595.json",
      "user_fields": {},
      "verified": false
    }
  ]
}
    ''',
    
    '''
{
  "job_status": {
    "id": "V3-ca23937b26f18d8b32a6f592b863b6bc",
    "message": null,
    "progress": null,
    "results": null,
    "status": "queued",
    "total": null,
    "url": "https://exampleendpoint.zendesk.com/api/v2/job_statuses/V3-ca23937b26f18d8b32a6f592b863b6bc.json"
  }
}


    ''',
    
    '''
{"job_status":{"id":"V3-ca23937b26f18d8b32a6f592b863b6bc","url":"https://exampleendpoint.zendesk.com/api/v2/job_statuses/V3-ca23937b26f18d8b32a6f592b863b6bc.json","total":6,"progress":6,"status":"completed","message":"Completed at 2022-12-11 21:00:36 +0000","results":[
{"index":0,"id":20,"account_id":15745908},
{"index":1,"id":18,"account_id":15745908},
{"index":2,"id":16,"account_id":15745908},
{"index":3,"id":19,"account_id":15745908},
{"index":4,"id":15,"account_id":15745908},
{"index":5,"id":17,"account_id":15745908}]}}
    ''',
    
   
    
    '''
{
  "count": 1,
  "next_page": null,
  "previous_page": null,
  "users": [
    {
      "active": true,
      "alias": null,
      "created_at": "2022-12-10T02:49:49Z",
      "custom_role_id": null,
      "default_group_id": null,
      "details": null,
      "email": "utest4inline@a.com",
      "external_id": null,
      "iana_time_zone": "America/Los_Angeles",
      "id": 11096765374107,
      "last_login_at": null,
      "locale": "en-US",
      "locale_id": 1,
      "moderator": false,
      "name": "utest4inline",
      "notes": null,
      "only_private_comments": false,
      "organization_id": null,
      "phone": null,
      "photo": null,
      "report_csv": false,
      "restricted_agent": true,
      "role": "end-user",
      "role_type": null,
      "shared": false,
      "shared_agent": false,
      "shared_phone_number": null,
      "signature": null,
      "suspended": false,
      "tags": [],
      "ticket_restriction": "requested",
      "time_zone": "America/Los_Angeles",
      "two_factor_auth_enabled": false,
      "updated_at": "2022-12-10T02:49:49Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/users/11096765374107.json",
      "user_fields": {},
      "verified": false
    }
  ]
}
    ''',
    
    '''
{
  "count": 0,
  "next_page": null,
  "previous_page": null,
  "tickets": []
}
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    '''
    xxxxxx
    ''',
    
    
    
    
    
    
    
    
    
    ]