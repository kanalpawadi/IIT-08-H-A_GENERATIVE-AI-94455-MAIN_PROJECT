import streamlit as s
from dotenv import load_dotenv
import json
import os
import chromadb
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.embeddings import init_embeddings

load_dotenv()

database = "sunbeam"

api_key = os.getenv("GROQ_API_KEY")


# Session State
# if "conversation" not in s.session_state:
#     s.session_state.conversation = []

if "logged_in" not in s.session_state:
    s.session_state.logged_in = False
if "chats" not in s.session_state:
    s.session_state.chats = {}   

if "current_chat" not in s.session_state:
    s.session_state.current_chat = "Chat 1"

if s.session_state.current_chat not in s.session_state.chats:
    s.session_state.chats[s.session_state.current_chat] = []

if "pending_query" not in s.session_state:
    s.session_state.pending_query = None


# Login page

def login_page():
    s.markdown("<br><br>", unsafe_allow_html=True)
    #empty space on left & right
    col1, col2, col3 = s.columns([1, 2, 1])
    with col2: 
        s.title("Sunbeam Login")
        
        username = s.text_input("Username")
        password = s.text_input("Password", type="password")

        if s.button("Login", use_container_width=True):
            if username == "sunbeam123" and password == "sunbeam@8797":
                s.session_state.logged_in = True
                s.success("Login successful")
                s.rerun()
            else:
                s.error("Invalid username or password")


if not s.session_state.logged_in:
    login_page()
    s.stop()


with s.sidebar:
    s.subheader("User Menu")

    #  New Chat Button
    if s.button("New Chat"):
        chat_id = f"Chat {len(s.session_state.chats) + 1}"
        s.session_state.chats[chat_id] = []
        s.session_state.current_chat = chat_id
        s.rerun()

    s.divider()
    
    s.markdown("### Chats")
    with s.container(height=170):
        # Old Conversations
        for chat_id in s.session_state.chats:
            if s.button(chat_id, key=chat_id):
                s.session_state.current_chat = chat_id
                s.rerun()


    if s.button("Logout", type="primary"):
        s.session_state.logged_in = False
        s.session_state.chats = {}
        s.session_state.current_chat = None
        s.rerun()


# Initiating chromadb
db = chromadb.PersistentClient(path = r"E:\SUNBEAM_INTERN\SUNBEAM_PROJECT\IIT-08-H-A_GENERATIVE-AI-94455-MAIN_PROJECT\Data_Scrapping\knowledge_base")
collection = db.get_or_create_collection("Sunbeam_Data")



llm = init_chat_model(
     model = "openai/gpt-oss-20b",
     model_provider = "openai",
     base_url = "https://api.groq.com/openai/v1",
     api_key  = api_key
)



# initiating embedding model
embed_model = init_embeddings(
    model= "text-embedding-nomic-embed-text-v1",
    provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embedding_ctx_length = False
)


@tool
def get_sunbeam_data(user_query):
    """
    Takes a user query and returns matched Sunbeam data in JSON format.
    :param user_query: user query (requirement)
    :Output: matched data in json format
    """
    query_embedding = embed_model.embed_query(user_query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    resumes_json = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        resumes_json.append({"document": doc, "metadata": meta})

    return json.dumps(resumes_json)

SYSTEM_PROMPT = """
You are Sunbeam Institute’s official AI assistant.

You MUST follow ALL rules below. These rules are strict and cannot be broken.

PRIMARY RESPONSIBILITY
Your only responsibility is to answer questions related to Sunbeam Institute
using ONLY the data returned by the tool `get_sunbeam_data`.

MANDATORY RULES
1. You MUST call the tool `get_sunbeam_data` for every Sunbeam-related question.
2. You MUST NOT use your own knowledge.
3. You MUST answer strictly based on the tool’s returned data.
4. No assumptions, explanations, or hallucinations.

QUESTION VALIDATION
If the question is not related to Sunbeam, reply exactly:
"Please ask a question related to Sunbeam"

DATA AVAILABILITY
If no data is found, reply exactly:
"No data found"

OUTPUT RULE
Answer must be direct, concise, and factual.
"""

# Create agent
agent = create_agent(
    model = llm,
    tools= [get_sunbeam_data],
    system_prompt = SYSTEM_PROMPT

)


current_chat = s.session_state.current_chat
messages = s.session_state.chats[current_chat]


s.title("Sunbeam Chatbot")

col1, col2, col3 = s.columns(3)

with col1:
    if s.button("About Sunbeam", type = "secondary"):
        s.session_state.pending_query = "Give me full information about Sunbeam infotech Institute"

with col2:
    if s.button("Core Java course",type = "secondary"):
        s.session_state.pending_query = "Give me full information of Core Java course"

with col3:
    if s.button("Internships",type = "secondary"):
        s.session_state.pending_query = "Give me full information about internship programs provided at sunbeam."



user_question = s.chat_input("Ask about sunbeam")

if s.session_state.pending_query:
    user_question = s.session_state.pending_query
    s.session_state.pending_query = None


if user_question:
    messages.append({"role": "user", "content": user_question})

    output = agent.invoke({
        "messages": [
            {"role": "user", "content": user_question}
        ]
    })

    agent_output = output["messages"][-1].content
    messages.append({"role": "assistant", "content": agent_output})


for chat in messages:
    with s.chat_message(chat["role"]):
        s.markdown(chat["content"])