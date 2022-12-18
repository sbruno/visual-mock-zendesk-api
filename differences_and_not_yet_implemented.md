

* Global
    * in visual-mock-zendesk-api, the ending .json is optional for all endpoints, e.g. `/api/v2/search` and `api/v2/search.json` are equivalent, this might not be the case in actual-zendesk.
    * errors will likely return different responses / different status codes as compared with actual-zendesk. visual-mock-zendesk-api has generally only currently implemented the cases that are not error cases.
    * pagination is not yet implemented, either cursor or page-level
    * rate-limit response-codes and headers are not yet implemented
    * several properties are not implemented. see schema.js
    * in general, if extra properties or unsupported properties are included on a ticket or comment, they are silently ignored (in actual-zendesk a warning header is sent back)
    * in both visual-mock-zendesk and actual-zendesk string ids are supported, sending in `id: "123"` will work, although it is technically more correct to use integer ids.
* Tickets
    * in visual-mock-zendesk ticket ids are randomly chosen, in actual-zendesk, they are always increasing.
    * in visual-mock-zendesk retrieving a ticket, the ticket has a comment_ids property, this doesn't exist in actual-zendesk.
    * fail-if-last-updated-sooner-than is a good tool for protecting against race conditions, but it isn't implemented yet.
    * Short syntax for comments when importing tickets,
        * visual-mock-zendesk allows some shorter syntax `comment: 'x'` that sometimes isn't supported by actual-zendesk 
        * I encourage you to simply send the full structure (`comments: [ {body: 'x', author_id:1} ]`) which works in all cases
    * Complexity of author_id when importing tickets,
        * if the author_id is missing for a comment, what should the author be set to?
        * visual-mock-zendesk does implement what appears to be actual-zendesk's non-trivial behavior, but it is safer to always provide a author_id for each comment and a requester_id for each ticket.
    * Comment-ordering
        * I recommend setting a created_at in comments when importing a ticket, otherwise actual-zendesk might place the comments in the wrong order.
* Custom Fields and Tags
    * Custom fields and tags functionality is fairly complete.
    * Only text custom fields are supported. Note that other types are often tied to a text field, for example a dropdown custom field is backed by another text field, making them less useful because they clutter up the space.
    * The tags/set_tags property when updating tickets is not ideal because of the potential race conditions if another process is setting tags at the same time. this race conditition can be avoided with either fail-if-last-updated-sooner-than, or the add_tags / remove_tags property. (These are only available on the batch apis, but it might be worth using the batch apis for features like this even though they involve more calls). The documentation says that add_tags / remove_tags only work for the `update_many.json?id=1` syntax (not very useful because it applies the same change to all the ids). In practice add_tags / remove_tags does work for the better `update_many.json` syntax where ticket ids are specified in a tickets array, so visual-mock-zendesk follows this.
* Comments
    * in visual-mock-zendesk, body, plain_body, and html_body are all the same. in actual-zendesk they can be different.
    * One pitfall of actual-zendesk: in some configurations like a small nonprod zendesk instance, retrieving a ticket retrieves its comment contents. In larger instances though, the comments aren't there and you have to explicitly call `/comments` to get them. visual-mock-zendesk-api follows this second behavior for safer behavior.
    * Attachments are not yet supported. It would be straightforward to add a button in the ui that added a hard-coded attachment to a comment.
    * Comments have an updated_at, which isn't there in actual-zendesk
* Statuses for batch calls
    * in visual-mock-zendesk status ids are numeric, in actual-zendesk, they might contain alphanumeric chars.
    * in visual-mock-zendesk, jobs complete instantly. in actual-zendesk, there is a status=pending period.
    * in visual-mock-zendesk, job statuses expire on app restart (note that saving any js file in the source code can trigger a restart). in actual-zendesk, they expire after a defined amount of time.
    * Remember to refer to the index property when looking at the results because in actual-zendesk the order will be different. 
    * When getting job results, the different batch endpoints all have slightly different-looking output. in visual-mock-zendesk we sometimes return a superset of what happens in actual-zendesk, 
        * in actual-zendesk the ticket import job returns the account id (undocumented), this is ommitted in visual-mock-zendesk-api




