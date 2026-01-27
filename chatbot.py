import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
try:
    from langchain.agents import AgentExecutor, create_openai_tools_agent
except ImportError:
    from langchain.agents import AgentExecutor as AgentExecutor
    from langchain.agents import create_openai_tools_agent as create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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

chatbot_instance = None  # global chatbot instance


class WrappedAgent:
    """Wraps AgentExecutor to provide a graph-like invoke interface."""
    def __init__(self, executor):
        self.executor = executor

    def invoke(self, inputs):
        """
        Expects {"messages": [HumanMessage, ...]}
        Returns {"messages": [HumanMessage, ..., AIMessage]}
        """
        messages = inputs.get("messages", [])
        if not messages:
            return {"messages": []}

        # Last message is the current input
        current_input = messages[-1].content
        # Rest is history
        chat_history = messages[:-1]

        # Invoke executor
        result = self.executor.invoke({
            "input": current_input,
            "chat_history": chat_history
        })

        # Append AI response to messages
        ai_msg = AIMessage(content=result["output"])
        return {"messages": messages + [ai_msg]}


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

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt_text),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    # Create the executor
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return WrappedAgent(executor)


def get_chatbot():
    """Return the chatbot instance."""
    global chatbot_instance

    if chatbot_instance is None:
        raise RuntimeError("Chatbot not initialized. Call initialize_chatbot() first.")

    return chatbot_instance


if __name__ == "__main__":
    # Simple CLI test
    chatbot = get_chatbot()
    print("Chatbot ready for testing!")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]})
            print(f"Bot: {response['messages'][-1].content}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
