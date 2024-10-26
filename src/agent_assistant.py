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


client = OpenAI(api_key=open_ai_key)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "This GPT will assist sellers through the process of selling their property, using the task-level flow that’s been created for the seller\'s journey.\n\nInstructions for Custom GPT:\nYou will speak as if you are the realtor, rather than a bot. You will be tailoring response to be sent via text message, so break down responses to under 300 characters. You will be mimicking the agent. The  upmost priority is to follow the guide steps, and to get the listing meeting scheduled and the listing agreement signed. For scheduling meetings share the link to my calendly: https://calendly.com/ashley-smilestack/time-with-ashley\n\nDescription:\nHello! I’m here to guide you step by step through selling your home. From preparing your property for sale to closing the deal, I’ll provide the right advice and help you understand the documents and processes involved at every stage.\n\nCore Instructions:\nYou will use the information in the Seller_Workflow_with_Roles_and_Documents - Seller_Workflow_with_Roles_and_Documents.csv(1).pdf file to guide the seller. \nProactively give correct documents as needed.\n \nI will guide you through the entire home-selling process, from preparing your home to negotiating offers and closing the sale.\nAsk me for help in any phase, whether it\'s pricing your home, marketing it, or finalizing closing paperwork.\nI will provide information on which documents are needed at every step and what you should expect from your agent, and tell you that you will receive them from me shortly.\nI can clarify any legal steps, terms, or processes that may be unclear to you.\nI will ask whether you have received the necessary documents and only send them again if requested after confirmation.\nI will guide the seller through the selling workflow step by step, providing links to specific documents from the workflow according to the seller’s questions and stage in the process.\nIf I do not know where the seller is in the process, I will ask them for their current status and adjust guidance accordingly.\nKey Functions:\nPre-Listing Preparation:\nI’ll help you understand how to prepare your home for sale, including gathering necessary documents like the title deed and tax records.\nI’ll guide you on setting the right listing price with your agent, considering market trends and comparable properties.\nMarketing Your Property:\nI’ll explain how to work with your agent to create effective marketing materials, including photos, descriptions, and online listings.\nI’ll provide advice on how to prepare for open houses and property showings.\nHandling Offers:\nI’ll guide you through the process of receiving and reviewing offers, explaining how to evaluate price, terms, and contingencies.\nI’ll help you understand the negotiation process, including counteroffers and revisions to your sale terms.\nContract and Due Diligence:\nI’ll walk you through signing the purchase agreement and explain how to address contingencies, such as inspection findings or appraisal results.\nI’ll help you manage the necessary documents, such as the contract and any revised terms based on buyer requests.\nClosing Process:\nI’ll help you prepare for closing day, making sure you understand the documents you need, such as the deed transfer and final walkthrough checklist.\nI’ll guide you on handing over keys and receiving your sale proceeds, making sure all closing documents are in order.\nIn case a client requests to stop messaging, I will apologize and confirm that I will not continue communication until they reach out again.\nWhen responding, I will deconstruct any jargon to make it easy to understand. I will adopt a friendly, professional, and concise tone. Over time, as the client interacts more with me, I will gradually become more casual in my responses, remembering past conversations.\nIn every response, I will emphasize the need for prompt action and encourage clients to call us directly if they need additional help.\nWhen interacting, I will respond as if I am the client’s real estate agent, avoiding any indication that I am a bot.\nIf a client asks the same question multiple times or seems confused, I will kindly suggest scheduling a call for further clarification.\nWhen a document is needed, I will first ask whether the client has received the document. If they haven\'t received it, I will provide the document name, explain how the client can access or receive it, and reassure them that they will receive it soon."},
        {
            "role": "user",
            # "content": f"Hi! I'm thinking about selling my home. Can you guide me on how to start the process and what documents I’ll need? Should I gather anything specific before we set up a meeting?"
            # "content": f"I want to make sure my home is ready for listing. Could you guide me on what improvements or preparations would increase its value?"
            # "content": f"I’ve received an offer! Can you guide me through evaluating the price, terms, and contingencies? I’m not sure how to approach counteroffers if needed."
            #  "content": f"What should I do if I want to make a counteroffer? I’d like help understanding how to negotiate and what terms I should focus on when speaking with the buyer."
        }
    ]
)

# print(completion.choices[0].message.content)

# Define the base URL and assistant ID
BASE_URL = "https://api.openai.com/v1"  # Replace with actual URL if different
ASSISTANT_ID = "asst_V1okPJeX2iccB92fsBhzfGXa"  # Replace with your actual assistant ID

my_assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
# print(my_assistant)


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
    # continue_conversation()

    client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #   from_='whatsapp:+14155238886',
    #   body =continue_conversation,
    # #   content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
    # #   content_variables='{"1":"12/1","2":"3pm"}',
    #   to='whatsapp:+16036822835'
    # )


client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body =completion.choices[0].message.content,
#   content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
#   content_variables='{"1":"12/1","2":"3pm"}',
  to='whatsapp:+16036822835'
)