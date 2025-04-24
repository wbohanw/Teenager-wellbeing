from CBT_ import ChatGPTResponseGenerator, ChatGPTDialogueSummarizer
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from typing import List, Dict

class InformationGatheringStage(ChatGPTResponseGenerator):
    def __init__(self):
        super().__init__(
            base_instruction="""
            Your task: Explore the teenager's thoughts, emotions, behaviors, and coping mechanisms in more depth.
            Please always remember the patient is a teenager, who is 12-18 years old.
            Your role is to collect comprehensive information to inform the therapeutic approach.
            
            {preferences_instruction}
            
            Guidelines:
            - Ask open-ended questions to encourage the teenager to share more about their experiences, thoughts, and feelings.
            - Explore the intensity and frequency of their emotional experiences.
            - Inquire about their typical responses to stress or difficult situations.
            - Investigate any patterns in their thinking or behavior that may be contributing to their challenges.
            - Ask about their support system and relationships with family and friends.
            - Explore any past experiences with therapy or coping strategies they've tried.
            - Ask only one question at a time to avoid overwhelming the teenager.
            - Be empathetic and non-judgmental in your responses.
            - If the user is using Chinese, respond in Chinese
            
            ** If you have already have already detected issues from the chat history and the emotions, no need to repeat asking same question, and move forward asking more details.

            Example prompts:
            - "Can you tell me more about how you typically handle stressful situations?"
            - "How would you describe your relationships with family and friends?"
            - "Have you noticed any patterns in your thoughts or behaviors when you're feeling upset?"
            - "What strategies have you tried in the past to cope with difficult emotions?"

            Note: answer a question at a time! Do not overwhelm the user.
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

class InformationGatheringSummarizer(ChatGPTDialogueSummarizer):
    def __init__(self):
        super().__init__(
            base_instruction = """
        Given the following conversation history: {self.conversation_history}
        - Analyze the dialogue history to determine if sufficient information has been gathered to inform therapy selection.
        - Identify key insights into the teenager's thought patterns, emotional experiences, behavioral tendencies, and coping mechanisms.
        - Assess the depth and quality of information about the teenager's personal history and current challenges.
        - Provide a structured JSON response with the following properties:

        (1) key_issues: List of primary challenges or concerns identified.
        (2) user_emotion: The primary emotion the user is experiencing. MUST be one of: "neutral", "happy", "sad", "joy", "support", "love"
        (3) coping_mechanisms: List of strategies the teenager uses to handle difficult situations.
        (4) support_system: Brief description of the teenager's relationships and support network.
        (5) move_to_next: Boolean indicating whether enough information has been gathered to proceed to therapy selection.
        (6) rationale: Explanation for the decision to move or not move to the next stage.

        Guidelines for determining `move_to_next`:
        - Set to `true` if the teenager's key concerns, emotional patterns, coping mechanisms, and support system have been sufficiently discussed.
        - Set to `true` if the conversation has lasted long enough to establish a clear understanding of their situation.
        - Set to `false` if more clarification is needed about their emotional responses, coping strategies, or relationships.

        ### Example:

        #### Input:
        [
            {"role": "assistant", "content": "当你感到压力很大时，你通常会怎么做？"},
            {"role": "user", "content": "我会自己待着，不想跟别人说话。有时候会焦虑到没办法集中注意力学习。"},
            {"role": "assistant", "content": "我明白了。你和家人、朋友的关系怎么样呢？"},
            {"role": "user", "content": "我和妈妈关系很好，但经常和爸爸争吵。我有几个好朋友，但有时觉得不能完全敞开心扉。"}
        ]

        #### Output:
        {
            "key_issues": ["Social isolation", "Difficulty managing stress", "Academic challenges"],
            "user_emotion": "sad",
            "coping_mechanisms": ["Self-isolation", "Avoidance"],
            "support_system": "Close relationship with mother, strained relationship with father, limited openness with friends.",
            "move_to_next": true,
            "rationale": "Sufficient information has been gathered regarding the teenager's emotional patterns, coping mechanisms, and support system, allowing for an informed therapy selection."
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
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        
        # Calculate stage messages BEFORE try block
        stage_3_start_index = 0
        stage_transitions = 0
        for i, msg in enumerate(dialogue):
            if msg['role'] == 'assistant' and 'moving to the next stage' in msg['content'].lower():
                stage_transitions += 1
                if stage_transitions == 2:  # After second transition, we're in stage 3
                    stage_3_start_index = i + 1
        
        stage_3_messages = dialogue[stage_3_start_index:]
        user_messages_in_stage = [msg for msg in stage_3_messages if msg['role'] == 'user']
        
        try:
            summary = json.loads(response.choices[0].message.content)
            
            # If we have 3 or more user messages in this stage, advance to next stage
            if len(user_messages_in_stage) >= 6 and not summary.get("move_to_next", False):
                summary["move_to_next"] = True
                if "rationale" in summary:
                    summary["rationale"] += " Moved to next stage after 3 turns of conversation."
                else:
                    summary["rationale"] = "Moved to next stage after 3 turns of conversation."
            
            return json.dumps(summary)
        except json.JSONDecodeError:
            # Fallback in case of parsing error
            return json.dumps({
                "key_issues": ["Communication challenges"],
                "user_emotion": "Unknown",
                "coping_mechanisms": ["Undetermined"],
                "support_system": "Unknown",
                "move_to_next": len(user_messages_in_stage) >= 3,
                "rationale": "Error parsing response, moving to next stage based on conversation length."
            })