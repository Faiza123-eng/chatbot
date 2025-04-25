from flask import Flask, request, jsonify
import uuid
import time

app = Flask(__name__)

# Store session information
sessions = {}

@app.route('/start_session', methods=['POST'])
def start_session():
    """Start a new chat session and return a session ID"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        'created_at': time.time(),
        'history': []
    }
    
    return jsonify({'session_id': session_id, 'status': 'success'})

@app.route('/chat', methods=['POST'])
def chat():
    """Process a chat message and return a response"""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', '')
    history = data.get('history', [])
    
    # Validate session
    if session_id not in sessions:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    # Here you would integrate your Mistral 7B model
    # For now, we'll simulate a response
    response = f"This is a simulated response to: {message}"
    
    # Update session history
    sessions[session_id]['history'] = history + [{'user': message, 'bot': response}]
    
    return jsonify({'response': response, 'status': 'success'})

@app.route('/end_session', methods=['POST'])
def end_session():
    """End a chat session"""
    data = request.json
    session_id = data.get('session_id', '')
    
    if session_id in sessions:
        del sessions[session_id]
        return jsonify({'status': 'success', 'message': 'Session ended'})
    else:
        return jsonify({'status': 'error', 'message': 'Session not found'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
