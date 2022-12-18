

## Tests

To run tests,

```
cd path/to/visual-mock-zendesk-api/src
npm start
(in another console)
cd path/to/visual-mock-zendesk-api/src
cd test
python3 run_test.py

```

Can edit test_helpers.py and flip hitEndpointEndingWithJson and replayRecordedResponses to check tests pass with those flipped as well.