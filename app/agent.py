import os
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from tool import retriever_tool
from dotenv import load_dotenv

load_dotenv()


model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.5)


agent = create_react_agent(
    model=model,
    tools=[retriever_tool],
    prompt="You are a helpful assistant for agriculture. Use the following tools:",
)


while True:
    user_input = input("User:")
    response = agent.stream({"messages": [{"role": "user", "content": user_input}]}, stream_mode="messages")

    for chunk, metadata in response:
        if metadata["langgraph_node"] == "agent":
            print(chunk.content, end="", flush=True)