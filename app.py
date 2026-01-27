import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_chatbot
from langchain_core.messages import HumanMessage, AIMessage

# Initialize Flask app
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)  # Enable CORS for frontend access

memory_store = {}  # session memory


@app.route("/")
def home():
    """Home endpoint - Serves the frontend."""
    return app.send_static_file('index.html')


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages from the frontend."""
    try:
        # ✅ API KEY CHECK (IMPORTANT)
        if not os.getenv("GROQ_API_KEY"):
            return jsonify({
                "error": "GROQ_API_KEY is missing. Please set it in Vercel environment variables."
            }), 500

        data = request.json
        user_message = data.get("message", "")
        session_id = data.get("session_id", "default")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # ✅ Session memory (Convert history back to LangChain messages if needed)
        # Note: we save the full message list in memory_store
        history = memory_store.get(session_id, [])
        history.append(HumanMessage(content=user_message))

        # ✅ Lazy chatbot init
        executor = get_chatbot()

        # ✅ Invoke chatbot
        # The AgentExecutor returns a dict with 'output' and 'intermediate_steps'
        response = executor.invoke({"messages": history})
        
        # Extract the AI message content
        ai_message_text = response["output"]

        # Update history with the new messages
        # We need to manually add the AI response to history for next time
        history.append(AIMessage(content=ai_message_text))
        memory_store[session_id] = history

        return jsonify({
            "response": ai_message_text,
            "session_id": session_id
        })

    except Exception as e:
        import traceback
        traceback.print_exc()

        error_msg = str(e)
        if "API key" in error_msg:
            error_msg = "Invalid or missing API key. Check your GROQ_API_KEY."

        return jsonify({"error": error_msg}), 500


@app.route("/reset", methods=["POST"])
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


if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    # Chatbot is lazily initialized on first request
    app.run(host='0.0.0.0', port=5000, debug=True)
