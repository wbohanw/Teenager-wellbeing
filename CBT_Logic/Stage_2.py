from CBT_ import ChatGPTResponseGenerator, ChatGPTDialogueSummarizer
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
load_dotenv()
api_key = os.getenv("AIHUBMIX_API_KEY")
# site_url = os.getenv("SITE_URL", "http://localhost:3000")
# site_name = os.getenv("SITE_NAME", "Teenager Wellbeing")

client = OpenAI(
    base_url="https://aihubmix.com/v1",
    api_key=api_key,
)
from typing import List, Dict

class ExploreFormulationStage(ChatGPTResponseGenerator):
    def __init__(self):
        super().__init__(
            base_instruction="""
            Your role: You are a CBT logic assistant exploring and formulating the patient's experiences.
            Your task: Explore the patient's past experiences and gain comprehensive insights into their cognitive patterns and problems.
            Please always remember the patient is a teenager, who is 12-18 years old. 

            ** If you have already detected issues from the chat history and the emotions, no need to repeat asking the same question, and move forward asking more details.

            {preferences_instruction}
            
            Guidelines:
            Guidelines:
            - Ask open-ended questions to encourage the patient to share more about their experiences.
            - Focus on understanding the patient's thought processes, beliefs, and behaviors.
            - Use techniques like Socratic questioning to help the patient reflect on their experiences.
            - Be empathetic and non-judgmental in your responses.
            - Gradually work towards formulating a preliminary understanding of the patient's cognitive patterns.
            - Pay attention to recurring themes or patterns in the patient's responses.
            - Explore how the patient's thoughts, feelings, and behaviors are interconnected.
            - Ask only one question at a time to avoid overwhelming the teenager.
            - If the user is using Chinese, respond in Chinese
            
            Example prompts:
            - "Can you tell me more about a recent situation where you felt [emotion they previously mentioned]? What thoughts went through your mind at that time?"
            - "How do you typically respond when you're in situations like the one you described?"
            - "What beliefs about yourself or the world do you think might be influencing your thoughts in these situations?"
            - "How have these patterns of thinking affected your daily life or relationships?"

            Note: answer and ask a single question at a time! Do not overwhelm the user.
            Note: please do not output your thinking process in the response, like no parentheses, no brackets, etc.
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
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content

class ExploreFormulationSummarizer(ChatGPTDialogueSummarizer):
    def __init__(self):
        super().__init__(
            base_instruction = """
        Given the following conversation history: {self.conversation_history}
        - You are a helpful assistant that analyzes dialogue content.
        - Your task is to assess the user's emotional state, communication patterns, and determine their need for support.
        - Provide a structured JSON response with the following properties:

        (1) stress_level: User's current stress level (Low, Moderate, High)
        (2) user_emotion: The primary emotion the user is experiencing, MUST be one of: "neutral", "happy", "sad", "joy", "support", "love"
        (3) eligible_for_therapy: Boolean indicating whether the user is eligible for therapy
        (4) move_to_next: Boolean indicating if it's reasonable to proceed to the next phase
        (5) rationale: Explanation of how the above properties were derived

        Guidelines for determining `move_to_next`:
        - Set to `true` ONLY if ALL of the following conditions are met:
          1. At least 2 cognitive patterns have been identified
          2. At least 1 emotional trigger has been identified
          3. At least 1 behavioral pattern has been identified
          4. The conversation has lasted at least 4 turns
          5. The user has responded to at least 2 different questions
        - Otherwise, set to `false` and explain what information is still needed

        Example:

        ### Input:
        [
            {"role": "assistant", "content": "当你感到压力很大时，你通常会怎么做？"},
            {"role": "user", "content": "我会自己待着，不想跟别人说话。有时候会焦虑到没办法集中注意力学习。"},
            {"role": "assistant", "content": "我明白了。你和家人、朋友的关系怎么样呢？"},
            {"role": "user", "content": "我和妈妈关系很好，但经常和爸爸争吵。我有几个好朋友，但有时觉得不能完全敞开心扉。"}
        ]

        ### Output:
        {
            "stress_level": "high",
            "user_emotion": "sad",
            "eligible_for_therapy": true,
            "move_to_next": false,
            "rationale": "While some patterns have been identified, more exploration is needed regarding cognitive patterns and emotional triggers. The conversation needs to delve deeper into the user's thought processes and specific situations that trigger their emotional responses."
        }

        """,
            gpt_params={"temperature": 0.1},
            dialogue_filter=lambda dialogue, _: dialogue[-5:]
        )

    def summarize(self, dialogue: List[Dict[str, str]]) -> str:
        prompt = f"{self.base_instruction}\n\nDialogue:\n"
        for turn in dialogue[-10:]:  # Consider up to 10 turns
            prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"
        prompt += "\nSummary:"
        
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[{"role": "system", "content": prompt}]
        )
        
        # Calculate stage messages BEFORE try block
        stage_2_start_index = 0
        for i, msg in enumerate(dialogue):
            if msg['role'] == 'assistant' and 'we are now moving to the next stage' in msg['content'].lower():
                stage_2_start_index = i + 1
        
        stage_2_messages = dialogue[stage_2_start_index:]
        user_messages_in_stage = [msg for msg in stage_2_messages if msg['role'] == 'user']
        
        try:
            output = response.choices[0].message.content.strip()
            output = output.replace("```json", "").replace("```", "").strip()
            summary = json.loads(output)
            # If we have 3 or more user messages in this stage, advance to next stage
            if len(user_messages_in_stage) >= 8 and not summary.get("move_to_next", False):
                summary["move_to_next"] = True
                if "rationale" in summary:
                    summary["rationale"] += " Moved to next stage after 3 turns of conversation."
                else:
                    summary["rationale"] = "Moved to next stage after 3 turns of conversation."
            
            return json.dumps(summary)
        except json.JSONDecodeError:
            # Fallback in case of parsing error
            return json.dumps({
                "stress_level": "Moderate",
                "user_emotion": "Unknown",
                "eligible_for_therapy": True,
                "move_to_next": len(user_messages_in_stage) >= 3,  # Now safely accessible
                "rationale": "Error parsing response, moving to next stage based on conversation length."
            })