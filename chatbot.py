"""
Student Helper Chatbot - Main Application
A LangChain-powered chatbot with tool calling capabilities to help students learn.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

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


class StudentHelperChatbot:
    """Student Helper Chatbot with LangChain tool calling."""
    
    def __init__(self):
        """Initialize the chatbot with LLM, tools, and agent."""
        
        # Check for API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "Groq API key not found! Please set GROQ_API_KEY in your .env file"
            )
        
        # Initialize the LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=api_key
        )
        
        # Define all available tools
        self.tools = [
            concept_explainer_tool,
            code_writer_tool,
            code_explainer_tool,
            math_solver_tool,
            study_tips_tool,
            resource_finder_tool
        ]
        
        # Create the system prompt
        self.system_prompt = """You are a friendly and helpful Student Helper AI assistant. 
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

        from langchain.agents import create_agent
        
        # Create the agent graph
        self.graph = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )
        
        # Maintain chat history
        self.chat_history = []
    
    def chat(self, user_input: str) -> str:
        """
        Process user input and return the chatbot's response.
        
        Args:
            user_input: The student's question or message
            
        Returns:
            The chatbot's response
        """
        try:
            # Add user message to history
            self.chat_history.append(HumanMessage(content=user_input))
            
            # Invoke the graph
            response = self.graph.invoke({"messages": self.chat_history})
            
            # Extract the last message (the AI's response)
            ai_message = response["messages"][-1]
            bot_response = ai_message.content
            
            # Add AI response to history
            self.chat_history.append(ai_message)
            
            return bot_response
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try rephrasing your question!"
    
    def run(self):
        """Run the interactive chatbot in the terminal."""
        print("=" * 70)
        print("STUDENT HELPER CHATBOT")
        print("=" * 70)
        print("\nHello! I'm your Student Helper AI. I can help you with:")
        print("  • Explaining complex concepts")
        print("  • Writing and explaining code")
        print("  • Solving math problems")
        print("  • Study tips and strategies")
        print("  • Finding learning resources")
        print("\nType 'quit' or 'exit' to end the conversation.")
        print("=" * 70)
        print()
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nGood luck with your studies! Feel free to come back anytime!")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Get chatbot response
            print("\nAssistant: ", end="", flush=True)
            response = self.chat(user_input)
            print(response)
            print("\n" + "-" * 70 + "\n")


def main():
    """Main entry point for the chatbot."""
    try:
        chatbot = StudentHelperChatbot()
        chatbot.run()
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your Groq API key to the .env file")
        print("3. Run the chatbot again")
    except KeyboardInterrupt:
        print("\n\nGoodbye! Happy studying!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
