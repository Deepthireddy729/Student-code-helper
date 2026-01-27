import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub

# Import all tools
from tools import (
    concept_explainer_tool,
    code_writer_tool,
    code_explainer_tool,
    math_solver_tool,
    study_tips_tool,
    resource_finder_tool
)

# Load environment variables
load_dotenv()

chatbot_graph = None  # global chatbot instance


def initialize_chatbot():
    """Initialize the LangChain chatbot agent."""
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing!")

    # Initialize the LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=api_key
    )

    # Define all available tools
    tools = [
        concept_explainer_tool,
        code_writer_tool,
        code_explainer_tool,
        math_solver_tool,
        study_tips_tool,
        resource_finder_tool
    ]

    # Create the system prompt
    system_prompt_text = """You are a friendly and helpful Student Helper AI assistant. 
Your goal is to help students learn and understand concepts effectively.

You have access to several specialized tools:
- concept_explainer_tool: For explaining complex concepts in simple terms
- code_writer_tool: For writing code based on requirements
- code_explainer_tool: For explaining existing code
- math_solver_tool: For solving mathematical problems with steps
- study_tips_tool: For providing study strategies and tips
- resource_finder_tool: For suggesting learning resources

When a student asks a question:
1. Understand what they need help with
2. Choose the most appropriate tool(s) to help them
3. Provide clear, encouraging, and educational responses
4. If they just want to chat or ask simple questions, respond directly without using tools

Be patient, encouraging, and remember that your goal is to help them LEARN, not just give answers!"""

    # Get the prompt from hub or create one
    # For simplicity and reliability on Vercel, we'll use a fixed prompt template
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt_text),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    # Create the executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


def get_chatbot():
    """Lazily initialize or return the chatbot graph."""
    global chatbot_graph
    
    if chatbot_graph is None:
        print("⚙️ Initializing chatbot...")
        chatbot_graph = initialize_chatbot()
        print("✅ Chatbot initialized")
        
    return chatbot_graph


if __name__ == "__main__":
    # Simple CLI test
    executor = get_chatbot()
    print("Chatbot ready for testing!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response = executor.invoke({"messages": [HumanMessage(content=user_input)]})
        print(f"Bot: {response['output']}")
