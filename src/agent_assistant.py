from dotenv import load_dotenv
from openai import OpenAI
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env file

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
open_ai_key = os.getenv("OPEN_AI_KEY")

client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body ='HELLO WORLD',
#   content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
#   content_variables='{"1":"12/1","2":"3pm"}',
  to='whatsapp:+16036822835'
)


client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)

# Define the base URL and assistant ID
BASE_URL = "https://api.openai.com/v1"  # Replace with actual URL if different
ASSISTANT_ID = "asst_V1okPJeX2iccB92fsBhzfGXa"  # Replace with your actual assistant ID

my_assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
print(my_assistant)


# Function to send a query to the assistant
def send_query(assistant_id, query):
    url = f"{BASE_URL}/assistants/{assistant_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {open_ai_key}"  # If authentication is required
    }
    payload = {
        # TODO
        # text message from human
        "query": "HELLO WORLD"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from assistant")
        elif response.status_code == 404:
            return "Assistant not found"
        elif response.status_code == 400:
            return "Bad request: Invalid input"
        else:
            return f"Unexpected error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

# Function to continue a conversation loop
def continue_conversation():
    print("Starting conversation with the assistant. Type 'exit' to end.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "Goodbye.":
            print("Conversation ended.")
            break

        assistant_response = send_query(ASSISTANT_ID, user_input)
        print(f"Assistant: {assistant_response}")

# Start the conversation
if __name__ == "__main__":
    continue_conversation()
 
# seller_assistant = client.beta.assistants.create(
#   instructions="You are a weather bot. Use the provided functions to answer questions.",
#   model="gpt-4o",
#   tools=[
#     {
#       "type": "function",
#       "function": {
#         "name": "get_current_temperature",
#         "description": "Get the current temperature for a specific location",
#         "parameters": {
#           "type": "object",
#           "properties": {
#             "location": {
#               "type": "string",
#               "description": "The city and state, e.g., San Francisco, CA"
#             },
#             "unit": {
#               "type": "string",
#               "enum": ["Celsius", "Fahrenheit"],
#               "description": "The temperature unit to use. Infer this from the user's location."
#             }
#           },
#           "required": ["location", "unit"]
#         }
#       }
#     },
#     {
#       "type": "function",
#       "function": {
#         "name": "get_rain_probability",
#         "description": "Get the probability of rain for a specific location",
#         "parameters": {
#           "type": "object",
#           "properties": {
#             "location": {
#               "type": "string",
#               "description": "The city and state, e.g., San Francisco, CA"
#             }
#           },
#           "required": ["location"]
#         }
#       }
#     }
#   ]
# )

# thread = client.beta.threads.create()
# message = client.beta.threads.messages.create(
#   thread_id=thread.id,
#   role="user",
#   content="What's the weather in San Francisco today and the likelihood it'll rain?",
# )

# run = client.beta.threads.runs.create_and_poll(
#   thread_id=thread.id,
#   assistant_id= seller_assistant.id,
# )
 
# if run.status == 'completed':
#   messages = client.beta.threads.messages.list(
#     thread_id=thread.id
#   )
#   print(messages)
# else:
#   print(run.status)
 
# # Define the list to store tool outputs
# tool_outputs = []
 
# # Loop through each tool in the required action section
# for tool in run.required_action.submit_tool_outputs.tool_calls:
#   if tool.function.name == "get_current_temperature":
#     tool_outputs.append({
#       "tool_call_id": tool.id,
#       "output": "57"
#     })
#   elif tool.function.name == "get_rain_probability":
#     tool_outputs.append({
#       "tool_call_id": tool.id,
#       "output": "0.06"
#     })
 
# # Submit all tool outputs at once after collecting them in a list
# if tool_outputs:
#   try:
#     run = client.beta.threads.runs.submit_tool_outputs_and_poll(
#       thread_id=thread.id,
#       run_id=run.id,
#       tool_outputs=tool_outputs
#     )
#     print("Tool outputs submitted successfully.")
#   except Exception as e:
#     print("Failed to submit tool outputs:", e)
# else:
#   print("No tool outputs to submit.")
 
# if run.status == 'completed':
#   messages = client.beta.threads.messages.list(
#     thread_id=thread.id
#   )
#   print(messages)
# else:
#   print(run.status)
