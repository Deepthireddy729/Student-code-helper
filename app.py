"""
Student Helper Chatbot - Flask Backend API
Provides REST API endpoints for the web frontend.
"""

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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

# Initialize Flask app
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)  # Enable CORS for frontend access

# Global chatbot instance
chatbot_graph = None
memory_store = {}


def get_chatbot():
    """Lazily initialize or return the chatbot graph."""
    global chatbot_graph
    if chatbot_graph is None:
        chatbot_graph = initialize_chatbot()
    return chatbot_graph


def initialize_chatbot():
    """Initialize the LangChain chatbot agent graph."""
    global chatbot_graph
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API key not found!")
    
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
    
    system_prompt = """You are a friendly and helpful Student Helper AI assistant. 
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
    chatbot_graph = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    return chatbot_graph


@app.route('/')
def home():
    """Home endpoint - Serves the frontend."""
    return app.send_static_file('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend."""
    try:
        # Check for API key first
        if not os.getenv("GROQ_API_KEY"):
            return jsonify({"error": "GROQ_API_KEY is missing. Please set it in Vercel environment variables."}), 500

        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get or create message history for this session
        if session_id not in memory_store:
            memory_store[session_id] = []
        
        history = memory_store[session_id]
        
        # Add user message to history
        history.append(HumanMessage(content=user_message))
        
        # Get the chatbot (initializes if necessary)
        graph = get_chatbot()
        
        # Get response from chatbot graph
        response = graph.invoke({"messages": history})
        
        # Extract AI message
        ai_message = response["messages"][-1]
        bot_response = ai_message.content
        
        # Add AI response to history
        history.append(ai_message)
        
        return jsonify({
            "response": bot_response,
            "session_id": session_id
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        error_msg = str(e)
        if "API key" in error_msg:
            error_msg = "Invalid or missing API key. Check your GROQ_API_KEY."
        return jsonify({"error": error_msg}), 500


@app.route('/reset', methods=['POST'])
def reset():
    """Reset conversation history for a session."""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in memory_store:
            del memory_store[session_id]
        
        return jsonify({"message": "Conversation history reset successfully"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Initializing Student Helper Chatbot...")
    try:
        get_chatbot()
        print("Chatbot initialized successfully!")
    except Exception as e:
        print(f"Initial initialization failed (this is okay if API key is missing locally): {e}")
    print("\n" + "=" * 70)
    print("Starting Flask server...")
    print("Frontend can connect to: http://localhost:5000")
    print("Direct UI access: http://localhost:5000/static/index.html")
    print("=" * 70 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
