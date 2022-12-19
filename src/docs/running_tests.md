

## Tests

To run tests, (the current directory must be as shown below)

```
cd path/to/visual-mock-zendesk-api/src
npm start

(in another console)
cd path/to/visual-mock-zendesk-api/src
cd test
python3 -m pip install requests
python3 run_test.py

```

You can edit test_helpers.py and flip hitEndpointEndingWithJson and replayRecordedResponses. The tests should pass with any combination of those settings being True/False.
