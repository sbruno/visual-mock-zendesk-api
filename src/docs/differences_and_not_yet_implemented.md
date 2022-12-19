
I've written some known minor behavior differences. Someday maybe these can all be fixed such that visual-mock-zendesk-api acts the same as actual-zendesk. I've also included complexities in the api.


* General
    * In visual-mock-zendesk-api, the ending .json is optional for all endpoints, e.g. `/api/v2/search` and `/api/v2/search.json` are equivalent, this might not be the case in actual-zendesk.
    * Errors will likely return different responses / different status codes as compared with actual-zendesk. visual-mock-zendesk-api has generally only currently implemented the cases that are not error cases.
    * Pagination is not yet implemented, either cursor or page-level
    * Rate-limit response-codes and headers are not yet implemented
    * Rarely-used properties are not implemented. See schema.js
    * In general, if extra properties or unsupported properties are included on a ticket or comment, they are silently ignored (in actual-zendesk a warning header is sent back)
    * In both visual-mock-zendesk and actual-zendesk string ids are supported, sending in `id: "123"` will work, although it is more correct to use integer ids.
    * In visual-mock-zendesk, we let you create the same user again. if you ask visual-mock-zendesk to create a user that already exists we might silently return the existing user, even if actual-zendesk might error.
    * In visual-mock-zendesk, we don't look at any headers for any credentials or to know who the current admin is. there is one hard-coded admin user who is always assumed to be the current admin. Future feature could be to read credentials in an authentication header and use the email provided there as the admin.
* Ticket show
    * In both visual-mock-zendesk and actual-zendesk, `show?ids=1,2,3` might return results in a different order than the order you had in your query, like 3,2,1. The mock intentionally returns results out-of-order to match actual-zendesk.
    * In visual-mock-zendesk retrieving a ticket, the ticket has a comment_ids property, this doesn't exist in actual-zendesk.
* Ticket update
    * fail-if-last-updated-sooner-than (safe_update) is a good tool for protecting against race conditions, but it isn't implemented yet.
    * We don't support the `update_many.json?ids=1,2,3` syntax.
    * I encourage you to simply send `author_id` for each comment which works in all cases. In visual-mock-zendesk, if posting a new comment and the author_id is missing, we fall back to the requester, which is likely the behavior of actual-zendesk. Unclear what happens if the requester_id is being updated at the same time.
* Ticket import
    * In both visual-mock-zendesk and actual-zendesk, there is slight distinction between imports/tickets/create_many and tickets/create_many,
        * imports can set a created_at on the comments
        * triggers are not run during imports
    * In visual-mock-zendesk ticket ids are randomly chosen, in actual-zendesk, they are always increasing.
    * Short syntax for comments when importing tickets,
        * I encourage you to simply send the full structure `comments: [ {body: 'a', author_id:1} ]` which works in all cases
        * visual-mock-zendesk allows a shorter syntax like `comment: 'a'` that sometimes isn't supported by actual-zendesk 
    * Complexity of missing author_id or missing requester_id when importing tickets,
        * I encourage you to simply send `author_id` for each comment and `requester_id` for each ticket though which works in all cases
        * If the author_id is missing for a comment, what should the author be set to?
        * visual-mock-zendesk follows actual-zendesk's non-trivial behavior for these edge cases but it is best not to rely on it
    * Comment-ordering
        * I recommend setting a created_at in comments when importing a ticket with >1 comment, otherwise actual-zendesk might place the comments in the wrong order.
    * Inline user creation
        * In both visual-mock-zendesk and actual-zendesk,
        * Some ticket apis, especially the batch ones,
        * let you create a new user inline, for example instead of writing
        * `requester_id: 234`, writing `requester: { name: 'name', email: 'example@example.com'}`
        * Not really documented and users/create_many is a better approach.
    * Default values
        * in visual-mock-zendesk, if certain fields like subject and description are missing there will be a fallback value like '(no subject)'. In actual-zendesk there isn't a default value like this.
    * Description
        * In visual-mock-zendesk, setting the description property acts like a typical property, like subject. In actual-zendesk, setting the description property has odd behavior, like creating a comment on the ticket. I recommend not setting description, it's not needed. 
* Custom Fields and Tags
    * Custom fields and tags functionality is fairly complete.
    * The `tags` property when updating tickets is not ideal to add or remove a tag because of the potential race conditions if another process is setting tags at the same time. This race conditition can be avoided with either safe_update, or the add_tags / remove_tags property. (These are only available on the batch apis, but it might be worth using the batch apis for features like this even though they involve more calls). The documentation says that add_tags / remove_tags only work for the `update_many.json?ids=1` syntax (not a useful endpoint because it applies the same change to all the tickets). In practice add_tags / remove_tags does work for all ticket update_many endpoints, so visual-mock-zendesk follows this.
    * In visual-mock-zendesk, if you create a ticket and don't specify a value for one of the custom fields, it won't be there on the ticket. in visual-mock-zendesk, if you create a ticket and don't specify a value for one of the custom fields, it will be there on the ticket with value null. In practice, doesn't really make a difference.
    * We don't support someone trying to do more than one of tags, add_tags, and remove_tags on the same ticket at the same time, which doesn't make sense.
    * In both visual-mock-zendesk and actual-zendesk, updates to custom fields merge. So if current is {fld1:a} and you set customfields to {fld2:b}, the result is {fld1:a, fld2:b}
* Comments
    * In visual-mock-zendesk, body, plain_body, and html_body are all the same. in actual-zendesk they can be different.
    * One pitfall of actual-zendesk: in some configurations like a small nonprod zendesk instance, retrieving a ticket retrieves its comment contents. In larger instances though, the comments aren't there and you have to explicitly call `/comments` to get them. visual-mock-zendesk-api follows this second behavior for safer behavior.
    * Attachments are not yet supported. It would be straightforward to add a button in the ui that added a hard-coded attachment to a comment.
    * Comments have an updated_at, which isn't there in actual-zendesk
* Users
    * In visual-mock-zendesk, user objects are essentially just an email address and a name. In actual-zendesk, there are many other features, and even features like user-custom-fields
    * In users create_many, visual-mock-zendesk returns success:true and action:updated if a user already exists with a given email. Would be good to check the behavior of actual-zendesk to ensure it matches. 
* Statuses for batch calls
    * In visual-mock-zendesk status ids are numeric, in actual-zendesk, they might contain alphanumeric chars.
    * In visual-mock-zendesk, jobs complete instantly. in actual-zendesk, there is a status=pending period.
    * In visual-mock-zendesk, job statuses expire on app restart (note that saving any js file in the source code can trigger a restart). in actual-zendesk, they expire after a defined amount of time.
    * Remember to refer to the index property when looking at the results from a batch job, because the order might not be guarenteed.
    * When getting job results, the different batch endpoints all have slightly different-looking output. in visual-mock-zendesk we currently return a superset of what happens in actual-zendesk, like getting an extra 'success: true' property that isn't there in actual-zendesk.
    * In actual-zendesk the ticket import job returns something called the account id (undocumented), this is not there in visual-mock-zendesk-api
* Searching for tickets
    * Remember to correctly url-encode what you send, see curl_examples.md.
    * The way Zendesk's search api works is this:
    * if you specify `tags:a tags:b` this means to search for
    * tags:a OR tags:b
    * (tickets with a, tickets with b, and tickets with both are included)
    * 
    * and you can say `-tags:a` to exclude tickets with the a tag.
    * 
    * We don't currently support something like tags:a -tags:b
    * We don't currently support saying `tags:"a b"` to require both a AND b
    * And we don't currently support the interesting clause custom_field:a which looks for a in all custom fields
    * We only support searching by `tags`, `status`, and `custom_field_x` where x is a custom fld id
    * We do support specifying sort_by and sort_order
    * We don't yet support using quotes to search for a string that contains spaces
    * We don't yet support searching the ticket content/comments
    * We don't limit/paginate the output. The search api limit of # of returned results is actually an issue sometimes, if you are writing an app that uses search, I recommend to order by created_at desc so that recent ones can be looked at first.
    * Lots of interesting features, see this, https://support.zendesk.com/hc/en-us/articles/4408886879258 and https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/
* Triggers
    * Two types of triggers are supported.
    * To simulate a trigger like "Conditions: All of the following: When 'Comment' is 'Public' | Action: Remove tag"
        * in configs.json, add {"action": "removeTagWhenPublicCommentPosted", "value":"(tag)"}
    * To simulate a trigger like "Conditions: All of the following: When 'Comment' is 'Public', When 'Text' Contains String 'x' | Action: Set Ticket Status = Open"
        * in configs.json, add {"action": "openPostWhenPublicCommentContainingTextPosted", "value": "x"}
    * These will fire when tickets are updated (they'd run on ticket creation too but the only ticket creation we support is batch import which does not run triggers).
* Zendesk custom apps
    * In visual-mock-zendesk, we don't support Zendesk custom apps





