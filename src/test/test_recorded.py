
'''

These are recorded responses from the actual api.

How to set this up
1) run tests and log each send() call, logging endpoint and body and saving to a text file
2) in that text file, replace the generated ids with real ids.
# use the calls to users/show_many to see what the test user ids are, then search/replace with real ids
# use the calls to tickets/create_many to see what the test custom flds are, then search/replace with real custom flds


'''

simulatedResponses = [
    # /api/delete_all
    r'''{}''',
    r'''
    Error: cannot pass in id
    ''',
    
    r'''
    Error: missing email
    ''',
    
    # use r''' instead of ''' so that \" preserves the \
    r'''
{
  "job_status": {
    "id": "111e0b044094f0c67893ac9fe64f1a99",
    "progress": null, "total": null, "message": null, "status": "completed",
    "url": "https://exampleendpoint.zendesk.com/api/v2/job_statuses/111e0b044094f0c67893ac9fe64f1a99.json"
  }
}
    ''',
    
    # some guesswork here since a trial account responds with 403 on the call
    r'''
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

    r'''
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
    r'''
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
    
    r'''
{
  "count": 0,
  "next_page": null,
  "previous_page": null,
  "users": []
}
    ''',
    
    r'''
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
    
    r'''
{
  "count": 0,
  "next_page": null,
  "previous_page": null,
  "users": []
}

    ''',
    
    r'''
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
    
    r'''
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
    
    r'''
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
    
    r'''
{"job_status":{"id":"V3-ca23937b26f18d8b32a6f592b863b6bc","url":"https://exampleendpoint.zendesk.com/api/v2/job_statuses/V3-ca23937b26f18d8b32a6f592b863b6bc.json","total":6,"progress":6,"status":"completed","message":"Completed at 2022-12-11 21:00:36 +0000","results":[
{"index":0,"id":20,"account_id":15745908},
{"index":1,"id":18,"account_id":15745908},
{"index":2,"id":16,"account_id":15745908},
{"index":3,"id":19,"account_id":15745908},
{"index":4,"id":15,"account_id":15745908},
{"index":5,"id":17,"account_id":15745908}]}}
    ''',
    
   
    
    r'''
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
    
    r'''
{
  "count": 0,
  "next_page": null,
  "previous_page": null,
  "tickets": []
}
    ''',
    
    r'''
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
    
    r'''
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
        "tag-to-remove-has-processed",
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
    
    r'''
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
        "tag-to-remove-has-processed"
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
        "tag-to-remove-has-processed",
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
    
    # /api/v2/tickets/999/comments
    r'''
Error: {
  "description": "Not found",
  "error": "RecordNotFound"
}
    ''',
    
    r'''
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
    
    r'''
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
    
    r'''
{
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175237309211,
      "author_id": 11007299217179,
      "body": "comment1",
      "created_at": "2022-01-02T06:38:32Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">comment1</p></div>",
      "id": 11175237309339,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
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
      "audit_id": 11175248028827,
      "author_id": 10981611611675,
      "body": "comment2",
      "created_at": "2022-01-03T06:38:32Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">comment2</p></div>",
      "id": 11175208190363,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
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
  "count": 2,
  "next_page": null,
  "previous_page": null
}
    ''',
    
   
    # second time getting ticket 1
    r'''
    {
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175237309211,
      "author_id": 11007299217179,
      "body": "comment1",
      "created_at": "2022-01-02T06:38:32Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">comment1</p></div>",
      "id": 11175237309339,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
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
      "audit_id": 11175248028827,
      "author_id": 10981611611675,
      "body": "comment2",
      "created_at": "2022-01-03T06:38:32Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">comment2</p></div>",
      "id": 11175208190363,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
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
  "count": 2,
  "next_page": null,
  "previous_page": null
}
    ''',
    
    r'''
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
    
    r'''
    {
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175231713307,
      "author_id": 11007299217179,
      "body": "testAuthorId1",
      "created_at": "2022-12-11T21:00:36Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">testAuthorId1</p></div>",
      "id": 11175231713435,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "testAuthorId1",
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
    
    # rearranged comments now that we know created_at time needs to be set when importing comments
    r'''
    {
  "comments": [
    {
      "attachments": [],
      "audit_id": 11175247939867,
      "author_id": 11007294636571,
      "body": "testAuthorId2",
      "created_at": "2022-12-11T21:00:35Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">testAuthorId2</p></div>",
      "id": 11175247939995,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "testAuthorId2",
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
      "audit_id": 11175231635355,
      "author_id": 10981611611675,
      "body": "testAuthorId3",
      "created_at": "2022-12-11T21:00:35Z",
      "html_body": "<div class=\"zd-comment\" dir=\"auto\"><p dir=\"auto\">testAuthorId3</p></div>",
      "id": 11175208108699,
      "metadata": {
        "custom": {},
        "system": {
          "latitude": 45.4901,
          "location": "Seattle, WA, United States",
          "longitude": -122.3747
        }
      },
      "plain_body": "testAuthorId3",
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
    
    r'''
    {
  "count": 3,
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
        "tag-to-remove-has-processed",
        "tag1",
        "tag2"
      ],
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
    }
  ]
}
    '''
    
]
