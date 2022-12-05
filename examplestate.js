

{
    mockZendeskState: {
        users: {
            "1234": {
                id: 1234,
                created_at: '123',
                email: 'abc@test.com',
                name: 'test name',
            }
        },
        tickets: {
            '98778': {
                id: 1234,
                created_at: '123',
                modified_at: '456',
                subject: 'abc',
                raw_subject: 'abc',
                status: 'Open',
                requester_id: '1234',
                submitter_id: '34534',
                tags: ['tag-to-replace-ready'],
                is_public: true,
                custom_fields: {}, // we just store what they send us
                fields: {}, // we just store what they send us
                // send back the comment_count
                comments: ['345345']
                }
            }
        },
        comments: {
            '345345': {
            id: '345345',
            created_at: '123',
            modified_at: '456',
            body: 'ab',
            html_body: 'ab',
            plain_body: 'ab',
            public: true,
            author_id: 234,
            attachments: [{
                id: 23423423,
                content_type: 'image/png',
                // send back the content_url: 'http://localhost:2343/56',
            }
            }
        }
        ]

    }
}

moderator:false
