import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_chatbot
from langchain_core.messages import HumanMessage, AIMessage

# Initialize Flask app
# Serve static files from the 'static' folder at the root path
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)  # Enable CORS for frontend access

memory_store = {}  # session memory


@app.route("/")
def home():
    """Home endpoint - Serves the frontend UI."""
    return app.send_static_file('index.html')


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages from the frontend."""
    try:
        # ✅ API KEY CHECK
        if not os.getenv("GROQ_API_KEY"):
            return jsonify({
                "error": "GROQ_API_KEY is missing. Please set it in Vercel environment variables."
            }), 500

        data = request.json
        user_message = data.get("message", "")
        session_id = data.get("session_id", "default")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # ✅ Session memory
        history = memory_store.get(session_id, [])
        # We only need to pass history to the chatbot; it will handle the new message if we include it
        history.append(HumanMessage(content=user_message))

        # ✅ Lazy chatbot init
        chatbot = get_chatbot()

        # ✅ Invoke chatbot (returns full message list in "messages" key)
        response = chatbot.invoke({"messages": history})

        # Extra memory update
        memory_store[session_id] = response["messages"]
        
        ai_message_text = response["messages"][-1].content

        return jsonify({
            "response": ai_message_text,
            "session_id": session_id,
            "reply": ai_message_text  # Including both keys for compatibility
        })

    except Exception as e:
        import traceback
        traceback.print_exc()

        error_msg = str(e)
        if "API key" in error_msg.lower():
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
