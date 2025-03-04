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
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}])
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
        (2) emotional_patterns: Description of the teenager's typical emotional responses and their intensity.
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
            "emotional_patterns": "Feels overwhelmed under stress and tends to withdraw from social interactions.",
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
        for turn in dialogue[-5:]:  # Consider last 5 turns
            prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"
        prompt += "\nSummary:"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        print(response)
        return response.choices[0].message.content