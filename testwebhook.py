import requests
import json

# Define your test webhook URL
WEBHOOK_URL = 'https://yoururl/llm-integration'  # Update this to your correct URL if hosted elsewhere

# Define the valid API key (ensure this matches your environment variable)
VALID_API_KEY = 'lkasdfklj'

# Define the invalid API key for testing unauthorized requests
INVALID_API_KEY = 'invalid-api-key'

# Sample data to send to the webhook (this mimics Dialogflow's payload)
payload = {
    "responseId": "sample-response-id",
    "queryResult": {
        "queryText": "What is GFN ?",
        "parameters": {},
        "allRequiredParamsPresent": True,
        "fulfillmentText": "",
        "intent": {
            "name": "projects/project-id/agent/intents/sample-intent-id",
            "displayName": "Tell a joke"
        },
        "intentDetectionConfidence": 0.9,
        "languageCode": "en"
    }
}

# Headers with valid API key
headers_with_valid_key = {
    'Content-Type': 'application/json',
    'X-API-Key': VALID_API_KEY
}

# Headers with invalid API key
headers_with_invalid_key = {
    'Content-Type': 'application/json',
    'X-API-Key': INVALID_API_KEY
}

def test_valid_request():
    """ Test the webhook with a valid API key """
    response = requests.post(WEBHOOK_URL, headers=headers_with_valid_key, data=json.dumps(payload))
    print(f"Test Valid Request - Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_invalid_request():
    """ Test the webhook with an invalid API key """
    response = requests.post(WEBHOOK_URL, headers=headers_with_invalid_key, data=json.dumps(payload))
    print(f"Test Invalid Request - Status Code: {response.status_code}")
    if response.status_code == 401:
        print("Unauthorized: Invalid API Key")
    else:
        print(f"Response: {response.text}")

def test_missing_api_key():
    """ Test the webhook with a missing API key """
    response = requests.post(WEBHOOK_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
    print(f"Test Missing API Key - Status Code: {response.status_code}")
    if response.status_code == 401:
        print("Unauthorized: Missing API Key")
    else:
        print(f"Response: {response.text}")

def test_invalid_payload():
    """ Test the webhook with an invalid payload """
    invalid_payload = {
        "invalidField": "This is invalid data"
    }
    response = requests.post(WEBHOOK_URL, headers=headers_with_valid_key, data=json.dumps(invalid_payload))
    print(f"Test Invalid Payload - Status Code: {response.status_code}")
    print(f"Response: {response.text}")

# Run the tests
if __name__ == '__main__':
    print("Running Webhook Tests...\n")
    
    test_valid_request()      # Test with valid API key and correct payload
    test_invalid_request()    # Test with invalid API key
    test_missing_api_key()    # Test with no API key
    test_invalid_payload()    # Test with incorrect payload
