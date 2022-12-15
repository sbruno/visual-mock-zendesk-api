
'''
in reality imports/tickets doesn't accept comment:"abc"
x-zendesk-api-warn = {:allowed_parameters=>{:controller=>"tickets", :action=>"create_many", :unpermitted_keys=>[], :invalid_values=>["tickets.2.comment"]}}
x-zendesk-api-warn = {:allowed_parameters=>{:controller=>"tickets", :action=>"create_many", :unpermitted_keys=>[], :invalid_values=>["tickets.1.comment", "tickets.2.comment"]}}

How to set this up
1) run tests and log each send() call, logging endpoint and body and saving to a text file
2) in that text file, replace the generated ids with real ids.
# use the calls to users/show_many to see what the test user ids are, then search/replace with real ids
# use the calls to tickets/create_many to see what the test custom flds are, then search/replace with real custom flds
# admin = 10981611611675,
# user1 = 11007294636571,
# user2 = 11007299217179,
# user3 = 11007314541595,
# fld1=10993199398427,
# fld2=10993238892315,
# fld3=11130845293467,

'''

simulatedResponses = [
    # /api/delete_all
    '''{}''',
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
    "url": "https://exampleendpoint.zendesk.com/api/v2/job_statuses/111e0b044094f0c67893ac9fe64f1a99.json"
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
    "url": "https://exampleendpoint.zendesk.com/api/v2/job_statuses/111e0b044094f0c67893ac9fe64f1a99.json"
  }
}
    ''',

    '''
{
  "job_status": {
    "id": "222e0b044094f0c67893ac9fe64f1a99",
    "progress": null, "total": null, "message": null, "status": "completed",
    "url": "https://exampleendpoint.zendesk.com/api/v2/job_statuses/222e0b044094f0c67893ac9fe64f1a99.json"
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
    "url": "https://exampleendpoint.zendesk.com/api/v2/job_statuses/222e0b044094f0c67893ac9fe64f1a99.json"
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
    {
  "count": 1,
  "next_page": null,
  "previous_page": null,
  "tickets": [
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-01-01T06:38:32Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": "fldval2"
        },
        {
          "id": 10993199398427,
          "value": "fldval1"
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981550938139,
      "description": "comment1",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": "fldval2"
        },
        {
          "id": 10993199398427,
          "value": "fldval1"
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 20,
      "is_public": true,
      "organization_id": null,
      "priority": null,
      "problem_id": null,
      "raw_subject": "ticket1",
      "recipient": null,
      "requester_id": 11007294636571,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "pending",
      "subject": "ticket1",
      "submitter_id": 11007294636571,
      "tags": [
        "tag1",
        "tag2"
      ],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-12-11T21:00:35Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/20.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ]
}
    ''',
    
    '''
    {
  "count": 2,
  "next_page": null,
  "previous_page": null,
  "tickets": [
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-12-11T21:00:35Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981595891227,
      "description": "plainStringComment2",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 16,
      "is_public": true,
      "organization_id": 10981567145627,
      "priority": null,
      "problem_id": null,
      "raw_subject": null,
      "recipient": null,
      "requester_id": 10981611611675,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "open",
      "subject": null,
      "submitter_id": 10981611611675,
      "tags": [
        "tag-to-replace-has-processed",
        "tag1",
        "tag2"
      ],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-12-11T21:00:35Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/16.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    },
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-01-01T06:38:32Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981595891227,
      "description": "plainStringComment1",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 18,
      "is_public": true,
      "organization_id": null,
      "priority": null,
      "problem_id": null,
      "raw_subject": "ticket2",
      "recipient": null,
      "requester_id": 11096765374107,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "open",
      "subject": "ticket2",
      "submitter_id": 11096765374107,
      "tags": [
        "tag1",
        "tag2"
      ],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-01-01T06:38:32Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/18.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ]
}
    ''',
    
    '''
    {
  "count": 6,
  "next_page": null,
  "previous_page": null,
  "tickets": [
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-01-01T06:38:32Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981595891227,
      "description": "plainStringComment1",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 18,
      "is_public": true,
      "organization_id": null,
      "priority": null,
      "problem_id": null,
      "raw_subject": "ticket2",
      "recipient": null,
      "requester_id": 11096765374107,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "open",
      "subject": "ticket2",
      "submitter_id": 11096765374107,
      "tags": [
        "tag1",
        "tag2"
      ],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-01-01T06:38:32Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/18.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    },
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-12-11T21:00:35Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981595891227,
      "description": "testAuthorIdUpdate",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 17,
      "is_public": true,
      "organization_id": null,
      "priority": null,
      "problem_id": null,
      "raw_subject": null,
      "recipient": null,
      "requester_id": 11007294636571,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "open",
      "subject": null,
      "submitter_id": 11007294636571,
      "tags": [
        "tag-to-replace-has-processed"
      ],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-12-11T21:00:35Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/17.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    },
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-12-11T21:00:35Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981595891227,
      "description": "testAuthorId2",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 15,
      "is_public": true,
      "organization_id": 10981567145627,
      "priority": null,
      "problem_id": null,
      "raw_subject": null,
      "recipient": null,
      "requester_id": 10981611611675,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "open",
      "subject": null,
      "submitter_id": 10981611611675,
      "tags": [],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-12-11T21:00:35Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/15.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    },
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-12-11T21:00:35Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981595891227,
      "description": "plainStringComment2",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 16,
      "is_public": true,
      "organization_id": 10981567145627,
      "priority": null,
      "problem_id": null,
      "raw_subject": null,
      "recipient": null,
      "requester_id": 10981611611675,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "open",
      "subject": null,
      "submitter_id": 10981611611675,
      "tags": [
        "tag-to-replace-has-processed",
        "tag1",
        "tag2"
      ],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-12-11T21:00:35Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/16.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    },
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-12-11T21:00:36Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981595891227,
      "description": "testAuthorId1",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": null
        },
        {
          "id": 10993199398427,
          "value": null
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 19,
      "is_public": true,
      "organization_id": null,
      "priority": null,
      "problem_id": null,
      "raw_subject": null,
      "recipient": null,
      "requester_id": 11007299217179,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "open",
      "subject": null,
      "submitter_id": 11007314541595,
      "tags": [],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-12-11T21:00:36Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/19.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    },
    {
      "allow_attachments": true,
      "allow_channelback": false,
      "assignee_id": 10981611611675,
      "brand_id": 10981621621915,
      "collaborator_ids": [],
      "created_at": "2022-01-01T06:38:32Z",
      "custom_fields": [
        {
          "id": 10993238892315,
          "value": "fldval2"
        },
        {
          "id": 10993199398427,
          "value": "fldval1"
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "custom_status_id": 10981550938139,
      "description": "comment1",
      "due_at": null,
      "email_cc_ids": [],
      "external_id": null,
      "fields": [
        {
          "id": 10993238892315,
          "value": "fldval2"
        },
        {
          "id": 10993199398427,
          "value": "fldval1"
        },
        {
          "id": 11130845293467,
          "value": null
        }
      ],
      "follower_ids": [],
      "followup_ids": [],
      "forum_topic_id": null,
      "group_id": 10981550950427,
      "has_incidents": false,
      "id": 20,
      "is_public": true,
      "organization_id": null,
      "priority": null,
      "problem_id": null,
      "raw_subject": "ticket1",
      "recipient": null,
      "requester_id": 11007294636571,
      "satisfaction_rating": null,
      "sharing_agreement_ids": [],
      "status": "pending",
      "subject": "ticket1",
      "submitter_id": 11007294636571,
      "tags": [
        "tag1",
        "tag2"
      ],
      "ticket_form_id": 10981566968091,
      "type": null,
      "updated_at": "2022-12-11T21:00:35Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/20.json",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ]
}
    ''',
    
    '''
Error: {
  "description": "Not found",
  "error": "RecordNotFound"
}
    ''',
    
    '''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175222974363,
      "author_id": 11096765374107,
      "body": "plainStringComment1",
      "created_at": "2022-12-11T21:00:36Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">plainStringComment1</p></div>",
      "id": 11175222974491,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "plainStringComment1",
      "public": true,
      "type": "Comment",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ],
  "count": 1,
  "next_page": null,
  "previous_page": null
}
    ''',
    
    '''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175237252635,
      "author_id": 10981611611675,
      "body": "plainStringComment2",
      "created_at": "2022-12-11T21:00:35Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">plainStringComment2</p></div>",
      "id": 11175237252763,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "plainStringComment2",
      "public": true,
      "type": "Comment",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ],
  "count": 1,
  "next_page": null,
  "previous_page": null
}
    ''',
    
    '''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175237252635,
      "author_id": 10981611611675,
      "body": "plainStringComment2",
      "created_at": "2022-12-11T21:00:35Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">plainStringComment2</p></div>",
      "id": 11175237252763,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "plainStringComment2",
      "public": true,
      "type": "Comment",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ],
  "count": 1,
  "next_page": null,
  "previous_page": null
}
    ''',
    
    '''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175237252635,
      "author_id": 10981611611675,
      "body": "plainStringComment2",
      "created_at": "2022-12-11T21:00:35Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">plainStringComment2</p></div>",
      "id": 11175237252763,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "plainStringComment2",
      "public": true,
      "type": "Comment",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ],
  "count": 1,
  "next_page": null,
  "previous_page": null
}
    ''',
    
    '''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175237252635,
      "author_id": 10981611611675,
      "body": "plainStringComment2",
      "created_at": "2022-12-11T21:00:35Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">plainStringComment2</p></div>",
      "id": 11175237252763,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "plainStringComment2",
      "public": true,
      "type": "Comment",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ],
  "count": 1,
  "next_page": null,
  "previous_page": null
}
    ''',
    
    '''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175237252635,
      "author_id": 10981611611675,
      "body": "plainStringComment2",
      "created_at": "2022-12-11T21:00:35Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">plainStringComment2</p></div>",
      "id": 11175237252763,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "plainStringComment2",
      "public": true,
      "type": "Comment",
      "via": {
        "channel": "api",
        "source": {
          "from": {},
          "rel": null,
          "to": {}
        }
      }
    }
  ],
  "count": 1,
  "next_page": null,
  "previous_page": null
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
    
    
    
    
    
    
    
    
    
    ]