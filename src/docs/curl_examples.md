
When sending in requests, remember to use url encoding. For example, in JavaScript this looks like `const endpoint = '/api/v2/users/search?query=email:' + encodeURIComponent(email);`

    1 uri: '/api/v2/users/create_many',
        curl -d '{"users":[{"name":"u1", "email":"a@b.com"}]}' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/users/create_many'
    2 uri: `/api/v2/users/search?query=email:"${encodeURIComponent(zendeskEmail)}"`
        curl 'localhost:8999/api/v2/users/search?query=email:df'
    3 uri: `/api/v2/users/show_many?ids=${ids.join(',')}`
        curl 'localhost:8999/api/v2/users/show_many?ids=65565,990140'
    4 uri: '/api/v2/imports/tickets/create_many'
        curl -d '@./test/curl_import.json' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/imports/tickets/create_many'
    5 uri: `/api/v2/tickets/show_many` 
        curl 'localhost:8999/api/v2/tickets/show_many?ids=187661'
    6 uri: `/api/v2/tickets/:id/comments` 
        curl 'localhost:8999/api/v2/tickets/63849/comments'
    7 uri: '/api/v2/tickets/update_many.json'
        curl -d '@./test/curl_update.json' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/tickets/update_many.json'
    8 uri: `/api/v2/search`
        curl 'http://localhost:8999/api/v2/search.json?query=type:ticket%20-status:closed%20updated%3E2021-11-02%20-tags:lv-has-processed%20-custom_field_1260826564690:%22skipThisTicket%22%20-custom_field_1900006024804:%22FromEmail%22&sort_by=created_at&sort_order=desc'



curl -d '{"users":[{"email":"atestuser@e.com", "name":"user1"}]}' -H "Content-Type: application/json" -X POST http://localhost:8999/api/v2/users/create_many

curl -d '{"tickets":[{"subject": "s1", "comments":[{"body": "atestuser@e.com"}]}]}' -H "Content-Type: application/json" -X POST http://localhost:8999/api/v2/imports/tickets/create_many

curl -d '{"tickets":[{"subject": "subject one", "comments":[{"body": "test one"}]}]}' -H "Content-Type: application/json" -X POST http://localhost:8999/api/v2/imports/tickets/create_many


