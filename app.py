from flask import Flask, request, jsonify, abort
import openai
import requests
import logging
from logging.handlers import RotatingFileHandler
import os

# Load environment variables (you can set these in your environment)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define your API key for authentication from environment
API_KEY = os.getenv('FLASK_SECRET_API_KEY')

# Flask app setup
app = Flask(__name__)

# Configure logging to a file with rotation
handler = RotatingFileHandler('llm_integration_webhook.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Function to check the API key
def check_api_key():
    api_key = request.headers.get('X-API-Key')
    return api_key == API_KEY

@app.route('/llm-integration', methods=['POST'])
def webhook():
    # Log the incoming request
    app.logger.info("Received a request from Dialogflow")

    # Check for API key before processing the request
    if not check_api_key():
        app.logger.error("Unauthorized access attempt due to invalid API key")
        abort(401, description="Unauthorized access: Invalid API key")

    # Extract the query text from Dialogflow's request
    req = request.get_json(silent=True, force=True)

    if req is None or 'queryResult' not in req:
        app.logger.error("Invalid request payload: missing 'queryResult'")
        abort(400, description="Invalid request payload")

    query = req.get('queryResult', {}).get('queryText', '')
    
    if not query:
        app.logger.error("Query text is missing from the request")
        abort(400, description="Query text is missing")

    # Log the query text
    app.logger.info(f"Received query: {query}")

    # Call GPT-3.5 Turbo API to get a response
    try:
        openai_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=100
        )
        
        # Extract the model's response
        response_text = openai_response.choices[0].message.content.strip()
        
        # Log the OpenAI response
        app.logger.info(f"OpenAI response: {response_text}")
        
    except Exception as e:
        # Log any errors that occur during the OpenAI request
        app.logger.error(f"Error when calling OpenAI API: {str(e)}")
        response_text = "There was an error processing your request."
    
    # Prepare the response for Dialogflow
    return jsonify({
        "fulfillmentText": response_text
    })

if __name__ == '__main__':
    # Load Flask host and port from environment variables
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app.run(host=host, port=port, debug=True)
