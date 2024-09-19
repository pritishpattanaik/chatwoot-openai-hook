# chatwoot-webhook-openai
To integrate Google Dialogflow ES with OpenAI, you can follow these general steps. The integration involves using Dialogflow for NLP tasks and leveraging OpenAI’s models to enhance responses where necessary. Here’s a step-by-step guide:

![image](https://github.com/user-attachments/assets/eeca6fd6-a161-46ae-aaa1-4f1f3e5efa9a)


# Chatwoot OpenAI Integration

This project integrates **Chatwoot** with **OpenAI** to automate customer support responses using AI. By following the steps below, you can set up the integration, automate responses, and enhance your customer support capabilities.

## Step-by-Step Integration Guide

### 1. Set Up OpenAI API
- Sign up for an OpenAI API key from the [OpenAI API website](https://platform.openai.com/).
- Save your API key securely.

### 2. Connect OpenAI with Chatwoot Webhooks
- In your Chatwoot dashboard, navigate to **Settings** > **Automation** > **Webhooks**.
- Create a new webhook and configure it to trigger when a new message is received.
- Write a simple backend service (you can use Flask, FastAPI, or Node.js) to catch the webhook events, process the incoming message, and send it to OpenAI’s API to generate a response.

### 3. Process the Response
- Using the OpenAI API, generate a relevant reply based on the customer’s query.
- Return the response to Chatwoot using their **conversation reply API**. You can format the AI’s response to feel conversational and align with your brand.

### 4. Automating the Reply
- Once the OpenAI-generated message is sent back to Chatwoot, you can automate sending replies based on user queries or allow human agents to review the AI’s response before sending.

---

## Setup

Follow these steps to set up the project on your local environment:

```bash
# Clone the repository
git clone https://github.com/pritishpattanaik/chatwoot-openai-hook.git

# Change directory to the project
cd chatwoot-openai-hook

# Set up a Python virtual environment
python3 -m venv venv

# Install the dependencies
pip install -r requirements.txt

# Copy the .env example and configure your keys
cp .env.example .env

# Edit .env to add your OpenAI API Key and Webhook API Key
# OPENAI_API_KEY=your_openai_api_key
# WEBHOOK_API_KEY=your_webhook_api_key

# Start the server
python3 app.py
```

	•	The webhook will now respond on localhost:5000.
	•	Use a reverse proxy with Nginx to expose the webhook to the internet.

### Nginx Configuration for Custom Webhook

Add the following block to your Chatwoot proxy configuration to pass requests to the webhook:

```
location /llm-integration {
    proxy_pass http://127.0.0.1:5000;  # Assuming webhook runs on port 5000
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
### Testing the Webhook

You can test the webhook using the following Python script:
```python3 testwebhook.py```

Once the test passes successfully, proceed to configure Dialogflow.

Dialogflow Integration
1.	In the Dialogflow console, go to Fulfillment and enable the webhook.
	•	Use your publicly accessible URL.
	•	Set the Headers to: X-API-KEY: <Your Webhook API Key>

  	![image](https://github.com/user-attachments/assets/5e164d67-560f-4a14-96f4-85777701d9cc)

3.	Go to Intent > Default Fallback Intent, and enable fulfillment for that intent.

   ![image](https://github.com/user-attachments/assets/18030a4a-62e2-4ef7-a3b9-57993cee41ac)



4.	Use the test console to validate that your chatbot is responding with AI-generated responses.

    ![image](https://github.com/user-attachments/assets/9f065e2b-69d5-408a-be80-f6c774beb304)

 


