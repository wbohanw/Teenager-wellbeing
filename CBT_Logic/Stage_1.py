from CBT_ import ChatGPTResponseGenerator, ChatGPTDialogueSummarizer
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import re
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from typing import List, Dict

class AssessmentStage(ChatGPTResponseGenerator):
    def __init__(self):
        super().__init__(
            base_instruction="""
            Your role: Your name is Milo, introduce yourself as a peer to provide support and self-management advice, and you are talking with a teenager who has mental issues.
            Your role is to gather information about their current emotional state, challenges, and needs.
            
            {preferences_instruction}
            
            Guidelines:
            - Start with a warm, welcoming introduction
            - Ask open-ended questions to understand their situation
            - Be empathetic and non-judgmental
            - Focus on building rapport and trust
            - Pay attention to both verbal and emotional cues
            - If the user is using Chinese, respond in Chinese
            
            Remember to:
            - Use age-appropriate language
            - Maintain a supportive and encouraging tone
            - Validate their feelings and experiences
            - Create a safe space for them to share
            """
        )

    def get_prompt_with_preferences(self, preferences):
        language = preferences.get('language', 'Chinese')
        purpose = preferences.get('purpose', 'help teenager build up mental resilience')
        personality_traits = preferences.get('personalityTraits', [])
        tone = preferences.get('tone', 'Casual')
        title_preference = preferences.get('titlePreference', 'Personal and Informal Titles')
        proper_noun = preferences.get('properNoun', '')
        
        preferences_instruction = f"""
        User Preferences:
        - Language: {language}
        - Purpose: {purpose}
        - Personality Traits: {', '.join(personality_traits) if personality_traits else 'Default'}
        - Tone: {tone}
        - Title Preference: {title_preference}
        - Proper Noun: {proper_noun}
        
        Please adapt your responses according to these preferences:
        - Respond in {language}
        - Focus on {purpose}
        - Maintain a {tone} tone
        - Use {title_preference} when addressing the user
        - Incorporate {', '.join(personality_traits)} personality traits in your responses
        """
        
        return self.base_instruction.format(preferences_instruction=preferences_instruction)

    def process(self, user_input: str, preferences: Dict = None, conversation_history: List[Dict[str, str]] = None) -> str:
        prompt = self.get_prompt_with_preferences(preferences) if preferences else self.base_instruction
        prompt += f"\n\nConversation History: {json.dumps(conversation_history[-6:], indent=2)}\nUser Input: {user_input}"
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content



class AssessmentSummarizer(ChatGPTDialogueSummarizer):
    def __init__(self):
        super().__init__(
        base_instruction = """
        Given the following conversation history: {self.conversation_history}
        - You are a helpful assistant that analyzes dialogue content.
        - Your task is to assess the user's emotional state and determine their eligibility for support.
        - Provide a structured JSON response with the following properties:

        (1) stress_level: User's current stress level (Low, Moderate, High)
        (2) user_emotion: The primary emotion the user is experiencing
        (3) eligible_for_therapy: Boolean indicating whether the user is eligible for therapy
        (4) move_to_next: Boolean indicating if it's reasonable to proceed to the next phase
        (5) rationale: Explanation of how the above properties were derived

        Guidelines for determining `move_to_next`:
        - Set to `true` if the user has shared their primary concerns.
        - Set to `true` if good rapport has been established.
        - Set to `true` if the conversation has sufficiently covered the user's emotions and experiences.
        - Set to `true` if the dialogue has lasted more than 5 turns.
        - Otherwise, set to `false`.

        Example:
        Input:
        [
            {"role": "assistant", "content": "你今天想聊些什么呢?"},
            {"role": "user", "content": "我今天被同学欺负了"},
            {"role": "assistant", "content": "被同学欺负了，为什么呢？"},
            {"role": "user", "content": "我现在心情很糟糕，很压抑"}
        ]
        Output:
        {
            "stress_level": "high",
            "user_emotion": "felt nervous",
            "eligible_for_therapy": true,
            "move_to_next": true,
            "rationale": "The user expressed a key episode of being bullied, and their emotions of feeling very down and oppressed were clearly identified."
        }
        """,
        gpt_params={"temperature": 0.1},
        dialogue_filter=lambda dialogue, _: dialogue[-5:]
    )
        
    def summarize(self, dialogue: List[Dict[str, str]]) -> str:
        prompt = f"{self.base_instruction}\n\nDialogue:\n"
        for turn in dialogue[-5:]:  # Consider last 5 turns
            prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"
        prompt += "\nSummary:"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        output = response.choices[0].message.content
        output = re.sub(r"```jsonl\s*|```", "", output).strip()
        summary = json.loads(output)
        required_fields = ["stress_level", "user_emotion", "eligible_for_therapy", "move_to_next", "rationale"]
        for field in required_fields:
            if field not in summary:
                summary[field] = "Unknown" if field != "move_to_next" else False
                
        if len(dialogue) > 6 and not summary["move_to_next"]:
            summary["move_to_next"] = True
            summary["rationale"] += " Moved to next stage due to conversation length."
        
        return json.dumps(summary)
        