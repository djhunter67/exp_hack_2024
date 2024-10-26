import requests

# Define the base URL and assistant ID
BASE_URL = "https://api.assistant.com/v2"  # Replace with actual URL if different
ASSISTANT_ID = "asst_V1okPJeX2iccB92fsBhzfGXa"  # Replace with your actual assistant ID

# Function to send a query to the assistant
def send_query(assistant_id, query):
    url = f"{BASE_URL}/assistant/{assistant_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # If authentication is required
    }
    payload = {
        # TODO
        # text message from human
        "query": query
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
