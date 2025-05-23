from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
from CBT_chat import CBTChatbot
import datetime
import json
from user_preferences import preferences_manager

load_dotenv()
api_key = os.getenv("AIHUBMIX_API_KEY")
# site_url = os.getenv("SITE_URL", "http://localhost:3000")
# site_name = os.getenv("SITE_NAME", "Teenager Wellbeing")

client = OpenAI(
    base_url="https://aihubmix.com/v1",
    api_key=api_key,
)


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
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({
                'status': 'error',
                'error': 'Missing required field: message'
            }), 400
            
        user_message = data['message']
        user_id = data.get('user_id', 'default_user')
        preferences = data.get('preferences', {})
        
        print(f"Received message from user {user_id}: {user_message}")
        
        chatbot = get_chatbot_session(user_id)
        
        # Apply preferences if provided
        if preferences:
            print("\n===== USER PREFERENCES =====")
            print(json.dumps(preferences, indent=4))
            print("=============================\n")
            chatbot.update_preferences(preferences)
            
        try:
            response = chatbot.chat(user_message)
            alert_message = chatbot.alert_agent.analyze_conversation(user_message, chatbot.conversation_history)
            stage_progress = chatbot.get_stage_progress()
            
            print(f"Generated response: {response}")
            
            return jsonify({
                'response': response,
                'alert': alert_message if alert_message else None,
                'user_emotion': chatbot.user_emotion,
                'stage_progress': stage_progress,
                'click': chatbot.click
            })
        except json.JSONDecodeError as e:
            print(f"JSON decode error in chatbot response: {e}")
            return jsonify({
                'status': 'error',
                'error': 'Invalid JSON response from chatbot',
                'details': str(e)
            }), 500
        except Exception as e:
            print(f"Error in chatbot processing: {e}")
            return jsonify({
                'status': 'error',
                'error': 'Error processing chatbot response',
                'details': str(e)
            }), 500
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in chat endpoint: {error_details}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'details': error_details
        }), 500

@app.route('/chat/<message>', methods=['GET'])
def chat_get(message):
    user_id = 'default_user'
    chatbot = get_chatbot_session(user_id)
    response = chatbot.chat(message)
    alert_message = chatbot.alert(message,chatbot.conversation_history)
    stage_progress = chatbot.get_stage_progress()
    
    return jsonify({
        'response': response,
        'user_emotion': chatbot.user_emotion,
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
        'api_key_configured': bool(os.getenv('OPENROUTER_API_KEY')),
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
            model="DeepSeek-V3-0324",
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

@app.route('/preferences', methods=['POST'])
def save_preferences():
    try:
        data = request.json
        user_id = data.get('user_id', 'default_user')
        preferences = data.get('preferences', {})
        
        if not preferences:
            return jsonify({
                'status': 'error',
                'error': 'No preferences provided'
            }), 400
            
        success = preferences_manager.save_preferences(user_id, preferences)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Preferences saved successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'error': 'Failed to save preferences'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/preferences/<user_id>', methods=['GET'])
def get_preferences(user_id):
    try:
        preferences = preferences_manager.get_preferences(user_id)
        
        if preferences is not None:
            return jsonify({
                'status': 'success',
                'preferences': preferences
            })
        else:
            return jsonify({
                'status': 'not_found',
                'message': 'No preferences found for this user'
            }), 404
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)