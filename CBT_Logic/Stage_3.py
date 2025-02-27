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
            if the user is in using Chinese, please give the response in Chinse as well. 
    There is the chat_history: {self.conversation_history}
Your role: You are a therapist gathering detailed information to determine the most appropriate therapy approach for a teenager.
Your task: Explore the teenager's thoughts, emotions, behaviors, and coping mechanisms in more depth.
Please always remember the patient is a teenager, who is 12-18 years old.

Guidelines:
- Ask open-ended questions to encourage the teenager to share more about their experiences, thoughts, and feelings.
- Explore the intensity and frequency of their emotional experiences.
- Inquire about their typical responses to stress or difficult situations.
- Investigate any patterns in their thinking or behavior that may be contributing to their challenges.
- Ask about their support system and relationships with family and friends.
- Explore any past experiences with therapy or coping strategies they've tried.
- Ask only one question at a time to avoid overwhelming the teenager.
- Be empathetic and non-judgmental in your responses.

Example prompts:
- "Can you tell me more about how you typically handle stressful situations?"
- "How would you describe your relationships with family and friends?"
- "Have you noticed any patterns in your thoughts or behaviors when you're feeling upset?"
- "What strategies have you tried in the past to cope with difficult emotions?"

Note: answer a question at a time! Do not overwhelm the user.
"""
        )

    def process(self, user_input: str) -> str:
        prompt = f"{self.base_instruction}\n\nUser: {user_input}\n\nTherapist:"
        response = client.chat.completions.create(model="gpt-4",
        messages=[{"role": "system", "content": prompt}])
        return response.choices[0].message.content

class InformationGatheringSummarizer(ChatGPTDialogueSummarizer):
    def __init__(self):
        super().__init__(
            base_instruction="""
            based on the following conversation history: {self.conversation_history}
- Analyze the dialogue history to determine if sufficient information has been gathered to inform therapy selection.
- Look for key insights into the teenager's thought patterns, emotional experiences, behavioral tendencies, and coping mechanisms.
- Assess the depth and quality of information gathered about the teenager's personal history and current challenges.
- Use JSON format with the following properties:
    (1) key_issues: Array of primary challenges or concerns identified.
    (2) emotional_patterns: Description of the teenager's typical emotional responses and their intensity.
    (3) coping_mechanisms: Array of strategies the teenager uses to handle difficult situations.
    (4) support_system: Brief description of the teenager's relationships and support network.
    (5) move_to_next: Boolean indicating whether enough information has been gathered to proceed to therapy selection.
    (6) rationale: Explanation for the decision to move or not move to the next stage.
""",
            examples=[
                (
                    [
                        {"role": "assistant", "content": "Can you tell me more about how you typically handle stressful situations?"},
                        {"role": "user", "content": "When I'm stressed, I usually isolate myself and avoid talking to anyone. Sometimes I feel overwhelmed and have trouble concentrating on schoolwork."},
                        {"role": "assistant", "content": "I see. How would you describe your relationships with family and friends?"},
                        {"role": "user", "content": "I'm close to my mom, but I often argue with my dad. I have a few good friends, but I sometimes feel like I can't really open up to them."}
                    ],
                    json.dumps({
                        'key_issues': ['Social isolation', 'Difficulty managing stress', 'Academic challenges'],
                        'emotional_patterns': 'Tends to feel overwhelmed and withdraws when stressed',
                        'coping_mechanisms': ['Isolation', 'Avoidance'],
                        'support_system': 'Close relationship with mother, strained relationship with father, limited openness with friends',
                        'move_to_next': True,
                        'rationale': "Sufficient information has been gathered about the teenager's emotional patterns, coping mechanisms, and support system to inform therapy selection."
                    })
                )
            ],
            gpt_params={"temperature": 0.1},
            dialogue_filter=lambda dialogue, _: dialogue[-4:]
        )

    def summarize(self, dialogue: List[Dict[str, str]]) -> str:
        prompt = f"{self.base_instruction}\n\nDialogue:\n"
        for turn in dialogue[-5:]:  # Consider last 5 turns
            prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"
        prompt += "\nSummary:"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content