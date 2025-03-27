import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"  # Change this if your backend is hosted elsewhere

# Function to create a new conversation
def create_conversation(name):
    response = requests.post(f"{API_URL}/conversations/", json={"name": name})
    return response.json()

# Function to send a message
def send_message(conversation_id, message_content):
    response = requests.post(f"{API_URL}/messages/", json={
        "conversation_id": conversation_id,
        "content": message_content
    })
    return response.json()

# Function to get conversations
def get_conversations():
    response = requests.get(f"{API_URL}/conversations/")
    return response.json()

# Function to get messages from a specific conversation
def get_messages(conversation_id):
    response = requests.get(f"{API_URL}/messages/{conversation_id}")
    return response.json()

# Function to summarize conversation
def summarize_conversation(conversation_id):
    response = requests.get(f"{API_URL}/summarize/{conversation_id}")
    return response.text

# Streamlit UI
st.title("Chat Application")

# Display all existing conversations
conversations = get_conversations()
st.subheader("Conversations")
conversation_names = [conv['name'] for conv in conversations]
conversation_ids = [conv['id'] for conv in conversations]
selected_conversation_id = st.selectbox("Select a conversation", conversation_ids, format_func=lambda x: conversation_names[conversation_ids.index(x)])

# Display messages in selected conversation
if selected_conversation_id:
    messages = get_messages(selected_conversation_id)
    st.write("Messages:")
    for msg in messages:
        st.write(f"Message: {msg['content']}")

    # Summarize the conversation
    if st.button("Summarize Conversation"):
        summary = summarize_conversation(selected_conversation_id)
        st.subheader("Summary")
        st.write(summary)

# Allow sending a message
message_content = st.text_area("Type a message")
if st.button("Send Message"):
    if selected_conversation_id and message_content:
        send_message(selected_conversation_id, message_content)
        st.success("Message sent!")
    else:
        st.error("Please select a conversation and enter a message.")

# Create a new conversation
st.subheader("Create a New Conversation")
new_conversation_name = st.text_input("Conversation name")
if st.button("Create Conversation"):
    if new_conversation_name:
        new_conversation = create_conversation(new_conversation_name)
        st.success(f"New conversation '{new_conversation['name']}' created!")
    else:
        st.error("Please enter a conversation name.")
