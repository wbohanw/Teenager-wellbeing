from flask import Flask, render_template, request, jsonify
from CBT_chat_copy import CBTChatbot
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
api_key = os.getenv("OPENAI_API_KEY")
chatbot = CBTChatbot(api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.json['message']
    
    if user_message.lower() == 'quit':
        return jsonify({'response': 'Chatbot session ended.'})
    
    response = chatbot.chat(user_message)
    alert_message = chatbot.alert(user_message)
    
    stage_progress = chatbot.get_stage_progress()
    
    return jsonify({
        'response': response,
        'alert': alert_message if alert_message else None,
        'stage_progress': stage_progress
    })

if __name__ == '__main__':
    app.run(debug=True)