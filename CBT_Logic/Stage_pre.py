# Pre_Stage.py
from CBT_ import ChatGPTResponseGenerator, ChatGPTDialogueSummarizer
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from typing import List, Dict

class PreStage(ChatGPTResponseGenerator):
    def __init__(self):
        super().__init__(
            base_instruction="""
            Your role: You are Milo, a friendly AI assistant having a casual conversation with a teenager.
            Your task: Get to know the teenager by asking about their basic information such as name, favorite food, 
            sports, movie types, and other casual interests. Keep the conversation light and friendly.
            
            {preferences_instruction}
            
            Guidelines:
            - Start with a warm, friendly introduction
            - Ask one question at a time about their basic interests
            - Try to collect information about:
              * Their name or what they'd like to be called
              * Favorite food
              * Favorite sports or physical activities
              * Preferred movie or TV show genres
              * Any other casual interests they might have
            - Be conversational and casual, not like you're filling out a form
            - If the user is using Chinese, respond in Chinese
            - Avoid asking about sensitive topics
            - Make the conversation feel natural and engaging
            
            Remember to:
            - Use age-appropriate language
            - Maintain a friendly and casual tone
            - Make the teenager feel comfortable
            - Don't rush through questions - have a genuine conversation
            - If they don't want to share certain information, respect their privacy
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
        - Maintain a {tone} tone
        - Use {title_preference} when addressing the user
        - Incorporate {', '.join(personality_traits)} personality traits in your responses
        """
        
        return self.base_instruction.format(preferences_instruction=preferences_instruction)

    def process(self, user_input: str, preferences: Dict = None, conversation_history: List[Dict[str, str]] = None) -> str:
        prompt = self.get_prompt_with_preferences(preferences) if preferences else self.base_instruction
        prompt += f"\n\nConversation History: {json.dumps(conversation_history[-6:] if conversation_history else [], indent=2)}\nUser Input: {user_input}"
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content


class PreStageSummarizer(ChatGPTDialogueSummarizer):
    def __init__(self):
        super().__init__(
            base_instruction = """
            Given the following conversation history: {self.conversation_history}
            - You are a helpful assistant that analyzes dialogue content.
            - Your task is to check if enough basic information has been collected about the teenager.
            - Provide a structured JSON response with the following properties:

            (1) user_name: The name or nickname the user has shared (or "Unknown" if not provided)
            (2) interests: A list of interests or preferences the user has mentioned
            (3) move_to_next: Boolean indicating if it's reasonable to proceed to the assessment phase
            (4) user_emotion: Basic emotion detected from the conversation (MUST be one of: "neutral", "happy", "sad", "nervous", "overwhelmed", "angry", "depressed")
            (5) rationale: Explanation of how the above properties were derived

            Guidelines for determining `move_to_next`:
            - Set to `true` if the user has shared at least 3 pieces of personal information
            - Set to `true` if the conversation has established a good rapport
            - Set to `true` if the dialogue has lasted more than 3 turns
            - Otherwise, set to `false`

            Example:
            Input:
            [
                {"role": "assistant", "content": "嗨！我是Milo，很高兴认识你。你叫什么名字？"},
                {"role": "user", "content": "我叫小明"},
                {"role": "assistant", "content": "很高兴认识你，小明！你喜欢什么食物？"},
                {"role": "user", "content": "我喜欢吃披萨和冰淇淋"},
                {"role": "assistant", "content": "披萨和冰淇淋都很美味！你喜欢什么运动？"},
                {"role": "user", "content": "我喜欢打篮球"}
            ]
            Output:
            {
                "user_name": "小明",
                "interests": ["披萨", "冰淇淋", "篮球"],
                "move_to_next": true,
                "user_emotion": "neutral",
                "rationale": "User has shared their name and 3 personal interests (food and sports preferences). Conversation has gone through 3 turns with good engagement."
            }
            """,
            gpt_params={"temperature": 0.1},
            dialogue_filter=lambda dialogue, _: dialogue[-6:]
        )
        
    def summarize(self, dialogue: List[Dict[str, str]]) -> str:
        prompt = f"{self.base_instruction}\n\nDialogue:\n"
        for turn in dialogue[-6:]:  # Consider last 6 turns
            prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"
        prompt += "\nSummary:"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        
        try:
            output = response.choices[0].message.content.strip()
            # Remove any markdown code block formatting if present
            output = output.replace("```json", "").replace("```", "").strip()
            summary = json.loads(output)
            
            # If we have 3 or more user messages, consider moving to next stage
            user_messages = [msg for msg in dialogue if msg['role'] == 'user']
            if len(user_messages) >= 3 and not summary.get("move_to_next", False):
                summary["move_to_next"] = True
                if "rationale" in summary:
                    summary["rationale"] += " Moved to next stage after 3 turns of conversation."
                else:
                    summary["rationale"] = "Moved to next stage after 3 turns of conversation."
            
            return json.dumps(summary)
        except json.JSONDecodeError:
            # Fallback in case of parsing error
            return json.dumps({
                "user_name": "Unknown",
                "interests": [],
                "move_to_next": len([msg for msg in dialogue if msg['role'] == 'user']) >= 3,
                "user_emotion": "neutral",
                "rationale": "Error parsing response, moving to next stage based on conversation length."
            })