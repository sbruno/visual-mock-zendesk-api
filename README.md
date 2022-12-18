

## tests

To run tests,

```
cd path/to/visual-mock-zendesk-api
npm start
(in another console)
cd path/to/visual-mock-zendesk-api
cd test
python3 run_test.py

```

Can edit test_helpers.py and flip hitEndpointEndingWithJson and replayRecordedResponses to check tests pass with those flipped as well.

For simplicity we have one hard-coded admin user.
Future feature could be to read credentials in an authentication header

Zendesk is a trademark of Zendesk, Inc.

References:
https://regbrain.com/article/bootstrap-express
https://www.edureka.co/blog/rest-api-with-node-js/
