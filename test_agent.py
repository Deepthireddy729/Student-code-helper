import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

load_dotenv()

def test_agent():
    api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)
    
    def my_tool(query: str) -> str:
        """A simple tool."""
        return f"Tool result for {query}"
        
    tools = [my_tool]
    
    agent = create_agent(model=llm, tools=tools, system_prompt="You are a helper.")
    
    print("Invoking agent...")
    try:
        response = agent.invoke({"messages": [HumanMessage(content="Hello")]})
        print("Response:", response)
    except Exception as e:
        print("Error during invoke:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent()
