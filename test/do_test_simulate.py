
'''
in reality imports/tickets doesn't accept comment:"abc"
x-zendesk-api-warn = {:allowed_parameters=>{:controller=>"tickets", :action=>"create_many", :unpermitted_keys=>[], :invalid_values=>["tickets.2.comment"]}}
x-zendesk-api-warn = {:allowed_parameters=>{:controller=>"tickets", :action=>"create_many", :unpermitted_keys=>[], :invalid_values=>["tickets.1.comment", "tickets.2.comment"]}}


uh-oh, setting a description creates a first comment
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
    "id": "V3-5868cd149f195c95c54fa9db56c1501f",
    "message": null,
    "progress": null,
    "results": null,
    "status": "queued",
    "total": null,
    "url": "https://exampleendpoint.zendesk.com/api/v2/job_statuses/V3-5868cd149f195c95c54fa9db56c1501f.json"
  }
}

    ''',
    
    '''
{"job_status":{"id":"V3-5868cd149f195c95c54fa9db56c1501f","url":"https://exampleendpoint.zendesk.com/api/v2/job_statuses/V3-5868cd149f195c95c54fa9db56c1501f.json","total":6,"progress":6,"status":"completed","message":"Completed at 2022-12-10 02:49:49 +0000","results":[
{"index":0,"id":11,"account_id":15745908}
,{"index":1,"id":13,"account_id":15745908}
,{"index":2,"id":10,"account_id":15745908}
,{"index":3,"id":14,"account_id":15745908}
,{"index":4,"id":9,"account_id":15745908}
,{"index":5,"id":12,"account_id":15745908}
]}
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
      "description": "descr1",
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
      "id": 11,
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
      "updated_at": "2022-12-10T02:49:47Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/11.json",
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
      "created_at": "2022-12-10T02:49:47Z",
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
      "description": "descr3",
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
      "id": 10,
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
      "updated_at": "2022-12-10T02:49:47Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/10.json",
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
      "description": "descr2",
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
      "id": 13,
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
      "updated_at": "2022-12-10T02:49:47Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/13.json",
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
      "created_at": "2022-12-10T02:49:47Z",
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
      "description": "descr3",
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
      "id": 10,
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
      "updated_at": "2022-12-10T02:49:47Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/10.json",
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
      "created_at": "2022-12-10T02:49:47Z",
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
      "description": "descr5",
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
      "id": 9,
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
      "updated_at": "2022-12-10T02:49:47Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/9.json",
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
      "description": "descr2",
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
      "id": 13,
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
      "updated_at": "2022-12-10T02:49:47Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/13.json",
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
      "created_at": "2022-12-10T02:49:48Z",
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
      "description": "descr6",
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
      "id": 12,
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
      "updated_at": "2022-12-10T02:49:48Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/12.json",
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
      "created_at": "2022-12-10T02:49:49Z",
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
      "description": "descr4",
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
      "id": 14,
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
      "updated_at": "2022-12-10T02:49:49Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/14.json",
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
      "description": "descr1",
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
      "id": 11,
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
      "updated_at": "2022-12-10T02:49:47Z",
      "url": "https://exampleendpoint.zendesk.com/api/v2/tickets/11.json",
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
      "audit_id": 11131363525787,
      "author_id": 11096765374107,
      "body": "descr2",
      "created_at": "2022-01-01T06:38:32Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">descr2</p></div>",
      "id": 11131363525915,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 47.6137,
          "location": "Seattle, WA, United States",
          "longitude": -122.3104
        }
      },
      "plain_body": "descr2",
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
    },
    {
      "attachments": [],
      "audit_id": 11131382976027,
      "author_id": 10981611611675,
      "body": "plainStringComment1",
      "created_at": "2022-12-10T02:49:49Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">plainStringComment1</p></div>",
      "id": 11131431877915,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 47.6137,
          "location": "Seattle, WA, United States",
          "longitude": -122.3104
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
  "count": 2,
  "next_page": null,
  "previous_page": null
}
    ''',
    
    '''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11131367569435,
      "author_id": 10981611611675,
      "body": "descr3",
      "created_at": "2022-12-10T02:49:47Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">descr3</p></div>",
      "id": 11131367569563,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 47.6137,
          "location": "Seattle, WA, United States",
          "longitude": -122.3104
        }
      },
      "plain_body": "descr3",
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
    },
    {
      "attachments": [],
      "audit_id": 11131408968091,
      "author_id": 10981611611675,
      "body": "plainStringComment2",
      "created_at": "2022-12-10T02:49:48Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">plainStringComment2</p></div>",
      "id": 11131382932379,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 47.6137,
          "location": "Seattle, WA, United States",
          "longitude": -122.3104
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
  "count": 2,
  "next_page": null,
  "previous_page": null
}
    ''',
    
    '''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11131408974363,
      "author_id": 11007294636571,
      "body": "descr1",
      "created_at": "2022-01-01T06:38:32Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">descr1</p></div>",
      "id": 11131408974491,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 47.6137,
          "location": "Seattle, WA, United States",
          "longitude": -122.3104
        }
      },
      "plain_body": "descr1",
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
    },
    {
      "attachments": [],
      "audit_id": 11131415850395,
      "author_id": 11007299217179,
      "body": "comment1",
      "created_at": "2022-01-02T06:38:32Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">comment1</p></div>",
      "id": 11131408977563,
      "metadata": {
        "custom": {},
        "system": {}
      },
      "plain_body": "comment1",
      "public": false,
      "type": "Comment",
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
      "attachments": [],
      "audit_id": 11131367590811,
      "author_id": 10981611611675,
      "body": "comment2",
      "created_at": "2022-01-03T06:38:32Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">comment2</p></div>",
      "id": 11131431851931,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 47.6137,
          "location": "Seattle, WA, United States",
          "longitude": -122.3104
        }
      },
      "plain_body": "comment2",
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
  "count": 3,
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