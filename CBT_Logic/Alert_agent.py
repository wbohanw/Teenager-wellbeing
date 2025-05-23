import openai
from typing import List, Dict
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)
api_key = os.getenv("AIHUBMIX_API_KEY")
# site_url = os.getenv("SITE_URL", "http://localhost:3000")
# site_name = os.getenv("SITE_NAME", "Teenager Wellbeing")

client = OpenAI(
    base_url="https://aihubmix.com/v1",
    api_key=api_key,
)
class AlertAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.self_harm_count = 0
        self.base_instruction = """
        You are an AI assistant tasked with monitoring a conversation for signs of extreme dangerous issues, particularly suicidal ideation or behavior. Analyze the following conversation and determine if there are any concerning signs that require immediate professional intervention.

        If you detect any of the following:
        1. Explicit mentions of suicide or self-harm
        2. Giving away possessions
        3. Talking about being a burden to others
        4. Increased isolation or withdrawal
        5. Extreme mood swings
        6. Talking about having no reason to live

        Then respond with a JSON object in the following format:
        {
            "alert": true,
            "reason": "Brief explanation of the concern"
        }

        If no concerning signs are detected, respond with:
        {
            "alert": false,
            "reason": null
        }
        Note: Be more careful about the emotion, just alert for extreme issues, and do not respond with anything other than the JSON object.
        """

    def analyze_conversation(self, user_input: str, conversation_history: List[Dict[str, str]]) -> Dict:
        conversation_text = "\n".join([f"{turn['role'].capitalize()}: {turn['content']}" for turn in conversation_history])
        prompt = f"{self.base_instruction}\n\nConversation:\n{conversation_text}\n\nAnalysis:\n{user_input}"

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[{"role": "system", "content": prompt}]
        )

        try:
            analysis = json.loads(response.choices[0].message.content)
            if analysis["alert"]:
                self.self_harm_count += 1
            return analysis
        except json.JSONDecodeError:
            return {"concern": False, "reason": None}
        

    def get_alert_message(self) -> str:
            return "I've detected multiple concerning signs in our conversation. As an AI, I'm not equipped to handle severe mental health issues. Please seek immediate help from a qualified mental health professional or contact a suicide prevention hotline. Your life matters, and there are people who can help you through this difficult time."

    def should_alert(self) -> bool:
        return self.self_harm_count >= 3

    def reset_count(self):
        self.self_harm_count = 0