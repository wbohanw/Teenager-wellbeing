from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
from CBT_chat import CBTChatbot
import datetime

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

user_sessions = {}

def get_chatbot_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = CBTChatbot(api_key)
    return user_sessions[user_id]


@app.route('/')
def home():
    """
    Home route.
    """
    today = datetime.date.today()
    year = today.strftime("%Y")

    return '@TreePal - Teenage Mental well-being ' + year


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({
            'status': 'error',
            'error': 'Missing required field: message'
        }), 400
        
    user_message = data['message']
    user_id = data.get('user_id', 'default_user')
    
    chatbot = get_chatbot_session(user_id)
    response = chatbot.chat(user_message)
    alert_message = chatbot.alert(user_message)
    
    stage_progress = chatbot.get_stage_progress()
    
    return jsonify({
        'response': response,
        'alert': alert_message if alert_message else None,
        'stage_progress': stage_progress
    })



@app.route('/reset/<user_id>', methods=['POST'])
def reset_session(user_id):
    if user_id in user_sessions:
        del user_sessions[user_id]
        return jsonify({
            'status': 'success',
            'message': f'Session for user {user_id} has been reset'
        })
    else:
        return jsonify({
            'status': 'warning',
            'message': f'No session found for user {user_id}'
        })

@app.route('/status/<user_id>', methods=['GET'])
def get_session_status(user_id):
    if user_id not in user_sessions:
        return jsonify({
            'status': 'error',
            'message': f'No session found for user {user_id}'
        }), 404
    
    chatbot = user_sessions[user_id]
    
    return jsonify({
        'status': 'success',
        'current_stage': chatbot.get_current_stage_name(),
        'stage_progress': chatbot.get_stage_progress(),
        'therapy_type': getattr(chatbot, 'chosen_therapy', None),
        'conversation_length': len(chatbot.conversation_history)
    })

# Status endpoint
@app.route('/gpt/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'online',
        'api_key_configured': bool(os.getenv('OPENAI_API_KEY')),
        'endpoints': {
            'regular_chat': '/gpt/chat',
            'realtime_chat': '/gpt/realtime_chat',
            'regular_test': '/gpt/test',
            'realtime_test': '/gpt/realtime_test'
        }
    })

# Test endpoint for regular GPT
@app.route('/gpt/test', methods=['GET'])
def test_gpt():
    try:
        test_prompt = "Give me a simple suggestion for a teenager who is feeling depressed."

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for teenagers."},
                {"role": "user", "content": test_prompt}
            ],
            temperature=0.1
        )
        
        return jsonify({
            'test_prompt': test_prompt,
            'response': response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)