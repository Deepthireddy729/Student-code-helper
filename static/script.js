// Student Helper Chatbot - Professional Frontend JS

const API_URL = 'http://localhost:5000';
let sessionId = generateSessionId();
let isWaitingForResponse = false;

function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9);
}

const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

userInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 200) + 'px';
});

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);
resetBtn.addEventListener('click', resetConversation);

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text || isWaitingForResponse) return;

    // Clear and state
    userInput.value = '';
    userInput.style.height = 'auto';
    isWaitingForResponse = true;
    sendBtn.disabled = true;

    // Remove welcome screen if it's the first message
    const welcome = document.querySelector('.welcome-screen');
    if (welcome) welcome.remove();

    appendMessage(text, 'user');
    showTypingIndicator();
    scrollToBottom();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, session_id: sessionId })
        });

        const data = await response.json();
        hideTypingIndicator();

        if (response.ok) {
            appendMessage(data.response, 'bot');
        } else {
            appendMessage('Wait, I hit a snag. The AI server returned an error.', 'bot', true);
        }
    } catch (error) {
        hideTypingIndicator();
        appendMessage('Network breakdown. Is the Flask server running on port 5000?', 'bot', true);
    } finally {
        isWaitingForResponse = false;
        sendBtn.disabled = false;
        userInput.focus();
        scrollToBottom();
    }
}

function appendMessage(text, sender, isError = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender} ${isError ? 'error' : ''}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerText = sender === 'user' ? '👤' : '🤖';

    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = parseRichText(text);

    // Copy support for code blocks
    content.querySelectorAll('pre').forEach(block => {
        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.innerText = 'Copy';
        btn.onclick = () => {
            const code = block.querySelector('code').innerText;
            navigator.clipboard.writeText(code);
            btn.innerText = 'Copied!';
            setTimeout(() => btn.innerText = 'Copy', 2000);
        };
        block.appendChild(btn);
    });

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(content);
    chatContainer.appendChild(msgDiv);
}

function parseRichText(text) {
    return text
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

function showTypingIndicator() {
    const div = document.createElement('div');
    div.className = 'message bot typing-message';
    div.id = 'typing-indicator';
    div.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    chatContainer.appendChild(div);
}

function hideTypingIndicator() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

async function resetConversation() {
    if (!confirm('Start a fresh conversation? history will be cleared.')) return;

    try {
        await fetch(`${API_URL}/reset`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId })
        });
    } catch (e) { }

    sessionId = generateSessionId();
    location.reload(); // Simplest way to restore welcome state
}

document.addEventListener('DOMContentLoaded', () => userInput.focus());
