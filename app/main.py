import streamlit as st
import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from tool import retriever_tool

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Agriculture Chatbot", page_icon=":seedling:")

st.title("🌱 Agriculture Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Set up the agent (same as in agent.py)
model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.5
)
agent = create_react_agent(
    model=model,
    tools=[retriever_tool],
    prompt="You are a helpful assistant for agriculture. Use the following tools:",
)

# Display chat history (top of page)
chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        if hasattr(st, "chat_message"):
            # Use chat_message if available (Streamlit >=1.25)
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])
        else:
            # Fallback for older Streamlit versions
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Bot:** {msg['content']}")

# Input at the bottom using a form
with st.form(key="chat_input_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", key="input", placeholder="Ask me anything about agriculture...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip():
        # Add user message to history
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Show loading spinner while generating response
        with st.spinner("Thinking..."):
            response_stream = agent.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                stream_mode="messages"
            )

            bot_response = ""
            for chunk, metadata in response_stream:
                if metadata["langgraph_node"] == "agent":
                    bot_response += chunk.content
            st.session_state["messages"].append({"role": "bot", "content": bot_response})
        st.rerun()