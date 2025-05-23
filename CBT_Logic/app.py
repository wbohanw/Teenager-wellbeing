from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Optional, Any, Union
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
from CBT_chat import CBTChatbot
import datetime
import json
import traceback
from user_preferences import preferences_manager

# Load environment variables
load_dotenv()
api_key = os.getenv("AIHUBMIX_API_KEY")

# OpenAI client
client = OpenAI(
    base_url="https://aihubmix.com/v1",
    api_key=api_key,
)

# Initialize FastAPI app
app = FastAPI(title="Teenager Wellbeing API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User sessions store
user_sessions = {}

# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    preferences: Dict[str, Any] = {}

class PreferencesRequest(BaseModel):
    user_id: str = "default_user"
    preferences: Dict[str, Any]

class ErrorResponse(BaseModel):
    status: str = "error"
    error: str
    details: Optional[str] = None

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str

class ChatResponse(BaseModel):
    response: str
    alert: Optional[str] = None
    user_emotion: Optional[str] = None
    stage_progress: Optional[Dict[str, Any]] = None
    click: Optional[Any] = None

class PreferencesResponse(BaseModel):
    status: str = "success"
    preferences: Dict[str, Any]

class StatusResponse(BaseModel):
    status: str
    current_stage: Optional[str] = None
    stage_progress: Optional[Dict[str, Any]] = None
    therapy_type: Optional[str] = None
    conversation_length: Optional[int] = None

# Helper function to get chatbot session
def get_chatbot_session(user_id: str):
    if user_id not in user_sessions:
        user_sessions[user_id] = CBTChatbot(api_key)
    return user_sessions[user_id]

# Routes
@app.get("/")
def home():
    """Home route."""
    today = datetime.date.today()
    year = today.strftime("%Y")
    return f"@TreePal - Teenage Mental well-being {year}"

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        user_message = request.message
        user_id = request.user_id
        preferences = request.preferences
        
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
            
            return {
                'response': response,
                'alert': alert_message if alert_message else None,
                'user_emotion': chatbot.user_emotion,
                'stage_progress': stage_progress,
                'click': chatbot.click
            }
        except json.JSONDecodeError as e:
            print(f"JSON decode error in chatbot response: {e}")
            raise HTTPException(status_code=500, detail=f"Invalid JSON response from chatbot: {str(e)}")
        except Exception as e:
            print(f"Error in chatbot processing: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing chatbot response: {str(e)}")
            
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error in chat endpoint: {error_details}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/{message}", response_model=ChatResponse)
async def chat_get(message: str):
    user_id = 'default_user'
    chatbot = get_chatbot_session(user_id)
    response = chatbot.chat(message)
    alert_message = chatbot.alert(message, chatbot.conversation_history)
    stage_progress = chatbot.get_stage_progress()
    
    return {
        'response': response,
        'user_emotion': chatbot.user_emotion,
        'alert': alert_message if alert_message else None,
        'stage_progress': stage_progress
    }

@app.post("/reset/{user_id}", response_model=SuccessResponse)
async def reset_session(user_id: str):
    if user_id in user_sessions:
        del user_sessions[user_id]
        return {"status": "success", "message": f"Session for user {user_id} has been reset"}
    else:
        return {"status": "warning", "message": f"No session found for user {user_id}"}

@app.get("/status/{user_id}", response_model=StatusResponse)
async def get_session_status(user_id: str):
    if user_id not in user_sessions:
        raise HTTPException(status_code=404, detail=f"No session found for user {user_id}")
    
    chatbot = user_sessions[user_id]
    
    return {
        "status": "success",
        "current_stage": chatbot.get_current_stage_name(),
        "stage_progress": chatbot.get_stage_progress(),
        "therapy_type": getattr(chatbot, "chosen_therapy", None),
        "conversation_length": len(chatbot.conversation_history)
    }

@app.get("/gpt/status")
async def status():
    return {
        "status": "online",
        "api_key_configured": bool(os.getenv("OPENROUTER_API_KEY")),
        "endpoints": {
            "regular_chat": "/gpt/chat",
            "realtime_chat": "/gpt/realtime_chat",
            "regular_test": "/gpt/test",
            "realtime_test": "/gpt/realtime_test"
        }
    }

@app.get("/gpt/test")
async def test_gpt():
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
        
        return {
            "test_prompt": test_prompt,
            "response": response.choices[0].message.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/preferences", response_model=SuccessResponse)
async def save_preferences(request: PreferencesRequest):
    try:
        user_id = request.user_id
        preferences = request.preferences
        
        if not preferences:
            raise HTTPException(status_code=400, detail="No preferences provided")
            
        success = preferences_manager.save_preferences(user_id, preferences)
        
        if success:
            return {"status": "success", "message": "Preferences saved successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to save preferences")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/preferences/{user_id}", response_model=PreferencesResponse)
async def get_preferences(user_id: str):
    try:
        preferences = preferences_manager.get_preferences(user_id)
        
        if preferences is not None:
            return {
                "status": "success",
                "preferences": preferences
            }
        else:
            raise HTTPException(status_code=404, detail="No preferences found for this user")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application with Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)