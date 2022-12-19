


When sending in requests, remember to use url encoding. For example, in JavaScript this looks like `const endpoint = '/api/v2/users/search?query=email:' + encodeURIComponent(email);`

```
Curl examples:

1 '/api/v2/users/create_many',

    curl -d '{"users":[{"name":"u1", "email":"a@b.com"}]}' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/users/create_many'

2 `/api/v2/users/search?query=email`

    curl 'localhost:8999/api/v2/users/search?query=email:theemail'
    
3 `/api/v2/users/show_many?ids=`

    curl 'localhost:8999/api/v2/users/show_many?ids=123,456'

4 '/api/v2/imports/tickets/create_many'

    curl -d '{"tickets":[{"subject": "subject one", "comments":[{"body": "test one"}]}]}' -H "Content-Type: application/json" -X POST http://localhost:8999/api/v2/imports/tickets/create_many
    
    curl -d '{"tickets":[{"subject": "subject one", "requester_id": 1234, "comments":[{"body": "test one", "author_id": 4567}]}]}' -H "Content-Type: application/json" -X POST http://localhost:8999/api/v2/imports/tickets/create_many

5 `/api/v2/tickets/show_many` 

    curl 'localhost:8999/api/v2/tickets/show_many?ids=123'

6 `/api/v2/tickets/:id/comments` 

    curl 'localhost:8999/api/v2/tickets/123/comments'

7 '/api/v2/tickets/update_many.json'

    This endpoint can add a comment to a ticket, update ticket properties, or both.

    curl -d '{"tickets":[{"id": 123, "comment":[{"body": "add one"}]}]}' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/tickets/update_many.json'
    
    curl -d '{"tickets":[{"id": 123, "tags":["a"], "custom_fields":[{id:123456, value:"val"}] }' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/tickets/update_many.json'

8 `/api/v2/search`
    simple,
    curl 'http://localhost:8999/api/v2/search.json?query=status:open'
    
    complex,
    curl 'http://localhost:8999/api/v2/search.json?query=type:ticket%20-status:closed%20-custom_field_1260826564690:%22skipThisTicket%22%20-custom_field_1900006024804:%22FromEmail%22&sort_by=created_at&sort_order=desc

```


