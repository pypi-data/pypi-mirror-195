__version__ = '0.1.0'

import requests
import json
import sseclient

class StreamBot:
    def __init__(self, api_key, bot_name, openai_url = 'https://api.openai.com/v1/chat/completions'):
        self.api_key = api_key
        self.bot_name = bot_name
        self.openai_url = openai_url

    def chat(self, messages):
        reqBody = {
          "model": "gpt-3.5-turbo-0301",
          "messages": messages,
          "stream": True
      }
        reqHeaders = {
            'Accept': 'text/event-stream',
            'Authorization': 'Bearer ' + self.api_key
        }
        try:
            # Fire off conversation message array to OpenAI  
            response = requests.post(self.openai_url, stream=True, headers=reqHeaders, json=reqBody)
            # Using the Server Sent Events library to support "Stream" of tokens to simulate the AI typing out
            client = sseclient.SSEClient(response)
            # Array to capture the tokens since `response` will no longer be consumable
            response_text = []
            print(self.bot_name + ": ")
            for event in client.events():
                try:
                    # Wrapped in try because json.loads fails due to `choices` not being present in last event
                    data = json.loads(event.data)['choices'][0]
                    # In first event, `delta` doesn't exist, so we check if the ['delta']['content'] keys are present
                    # Also check for ['finish_reason'] to break on last message
                    if 'delta' in data and 'content' in data['delta'] and data['finish_reason'] != 'stop':
                        response_text.append(data['delta']['content'])
                        print(data['delta']['content'], end="", flush=True)
                except json.decoder.JSONDecodeError:
                    pass
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
          
        return "".join(response_text)
