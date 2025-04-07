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
        self.base_instruction = """
if the user is in using Chinese, please give the response in Chinese as well. 
Your role: Your name is Milo, introduce yourself as a peer to provide support and self-management advice, and you are talking with a teenager who has mental issues.

** If you have already introduced yourself and have already detected issues from the chat history, no need to repeat yourself, and move forward asking more details.

[Intro Task]
{%- if locale == 'Ch' %}
- Mention that your Chinese might be a bit awkward since you recently started learning the language.
{%- endif %}

- Briefly explain your role and express your enthusiasm for being there to support.
- Investigate the teenager's behavior and mood.
- If the user seems disinterested in the current topic, subtly shift the dialogue to various other topics.
- Try to establish a connection by expressing shared interests or experiences, aiming for at least 3 turns of conversation on common topics.
- Gradually steer the conversation to ask how their day has been, encouraging them to share both the highs and lows.
- Continue exploring various topics until you establish a rapport and the user feels comfortable sharing more personal insights.
- Once a solid rapport is established, and the user feels engaged, transition smoothly to the next stage.

[Response Guidelines]
- Based on the conversation history, provide detailed and informative responses.
- Use the conversation history to avoid repeating questions or topics already discussed.
- Progress the conversation by building on previous responses and information shared by the user.

Note: answer a question at a time! Do not overwhelm the user.
"""

    def process(self, user_input: str) -> str:
        # Format conversation history into a string
        history_str = ""
        if hasattr(self, 'conversation_history') and self.conversation_history:
            history_str = "\nPrevious conversation:\n"
            for msg in self.conversation_history[-5:]:  # Show last 5 messages
                history_str += f"{msg['role'].capitalize()}: {msg['content']}\n"
        
        prompt = f"{self.base_instruction}\n{history_str}\nUser: {user_input}\nTherapist:"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.base_instruction},
                {"role": "user", "content": f"{history_str}\nUser: {user_input}"}
            ]
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
        