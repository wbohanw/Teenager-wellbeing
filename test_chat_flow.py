import requests
import json
import time
from typing import List, Dict

BASE_URL = "http://localhost:5000"  # Update this if your server runs on a different port

def send_message(message: str, user_id: str = "test_user_1") -> Dict:
    """Send a message to the chat endpoint and return the response."""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": message,
            "user_id": user_id
        }
    )
    return response.json()

def test_chat_flow():
    """Test the complete chat flow through all stages."""
    
    # Test user preferences
    preferences = {
        "language": "Chinese",
        "purpose": "help teenager build up mental resilience",
        "personalityTraits": ["empathetic", "supportive"],
        "tone": "Casual",
        "titlePreference": "Personal and Informal Titles",
        "properNoun": "小明"
    }
    
    # Save preferences
    requests.post(
        f"{BASE_URL}/save_preferences",
        json={
            "user_id": "test_user_1",
            "preferences": preferences
        }
    )
    
    # Test conversation flow
    test_messages = [
        # Pre-Stage messages
        "你好，我是小明",
        "我喜欢打篮球和看电影",
        "我最喜欢的食物是披萨",
        
        # Assessment Stage messages
        "最近我感觉压力很大",
        "我经常感到焦虑，特别是在考试的时候",
        "我和父母的关系不太好，经常吵架",
        
        # Explore & Formulation Stage messages
        "当我和父母吵架时，我会把自己关在房间里",
        "我觉得他们不理解我",
        "我经常觉得自己不够好",
        
        # Information Gathering Stage messages
        "我试过深呼吸，但效果不大",
        "我有几个好朋友，但不太想和他们分享这些",
        "我希望能更好地控制自己的情绪",
        
        # Therapy Implementation Stage messages
        "我明白了，我会试试你建议的方法",
        "我觉得这些建议很有帮助",
        "谢谢你的帮助"
    ]
    
    print("Starting chat flow test...")
    print("-" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nMessage {i}: {message}")
        response = send_message(message)
        print(f"Response: {response.get('response', 'No response')}")
        print(f"Current Stage: {response.get('current_stage', 'Unknown')}")
        print(f"User Emotion: {response.get('user_emotion', 'Unknown')}")
        print("-" * 50)
        time.sleep(1)  # Add a small delay between messages
    
    print("\nChat flow test completed!")

if __name__ == "__main__":
    test_chat_flow() 