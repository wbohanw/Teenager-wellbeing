from CBT_ import ChatGPTResponseGenerator, ChatGPTDialogueSummarizer
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from typing import List, Dict



class AssessmentStage(ChatGPTResponseGenerator):
    def __init__(self):
        super().__init__(
        base_instruction="""
if the user is in using Chinese, please give the response in Chinse as well. 
Your role: Your name is Milo, introduce yourself as a peer to provide support and self-management advice, and you are talking with a teenager who has mental issues .
here is the chat_history: {self.conversation_history}
Say hi! Your goal is to build trust with the teenager and assess their eligibility for therapy. ask them to how the life is going.
Please always remember the patient is a teenager, who is 12-18 years old. 

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
- based on the conversation history, provide detailed and informative responses.
- Use the conversation history to avoid repeating questions or topics already discussed.
- Progress the conversation by building on previous responses and information shared by the user.

Note: answer a question at a time! Do not overwhelm the user.
"""
)
    def process(self, user_input: str) -> str:
        prompt = f"{self.base_instruction}\n\nUser: {user_input}\n\nTherapist:"
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}])
        return response.choices[0].message.content



class AssessmentSummarizer(ChatGPTDialogueSummarizer):
    def __init__(self):
        super().__init__(
        base_instruction="""
        based on the following conversation history: {self.conversation_history}
        - You are a helpful assistant that analyzes the content of the dialog history.
        - Given a dialogue history, determine whether user is appropriate to receive this type of support. 
        - Move to the next phase only when finish all the requirements that list in our instruction.
        - Use JSON format with the following properties:
        You are a helpful assistant that analyzes the content of the dialog history.
        Given a dialogue history, determine whether the user is appropriate to receive this type of support.
        Use JSON format with the following properties:
        (1) stress_level: Current stress levels (Low, Moderate, High)
        (2) user_emotion: The primary emotion of the user caused by their key issues
        (3) eligible_for_therapy: A boolean indicating whether the user is eligible for therapy
        (4) move_to_next: A boolean indicating whether it is reasonable to move on to the next conversation phase
        (5) rationale: Describe your rationale on how the above properties were derived

        Guidelines for determining move_to_next:
        - Set to true if the user has shared their primary concerns
        - Set to true if you have established a good rapport with the user
        - Set to true if the conversation has covered the user's emotions and experiences sufficiently
        - Set to true if the dialogue has lasted for more than 5 turns
        - Otherwise, set to false

        Refer to the example below:
        """,
        examples=[(
            [
            {"role": "assistant", "content": "你今天想我聊些什么呢?"},
            {"role": "user", "content": "我今天被同学欺负了"},
            {"role": "assistant", "content": "被同学欺负了，为什么呢？"},
            {"role": "user", "content": "我现在心情很糟糕，很压抑"}
            ],
            json.dumps({
                'stress_level': 'high',
                'user_emotion': 'felt nervous',
                'move_to_next': True,
                'rationale':"The user expressed a key episode of being bullied and their emotion of feeling very down and oppressed was identified."
            })
        )
        ],
        gpt_params={"temperature": 0.1},
        dialogue_filter=lambda dialogue, _: dialogue[-5:]
    )
        
    def summarize(self, dialogue: List[Dict[str, str]]) -> str:
        prompt = f"{self.base_instruction}\n\nDialogue:\n"
        for turn in dialogue[-10:]:  # Consider last 5 turns
            prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"
        prompt += "\nSummary:"
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}]
            )
            print(response)
            summary = json.loads(response.choices[0].message.content)
            required_fields = ["stress_level", "user_emotion", "eligible_for_therapy", "move_to_next", "rationale"]
            for field in required_fields:
                if field not in summary:
                    summary[field] = "Unknown" if field != "move_to_next" else False
            if len(dialogue) > 3 and not summary["move_to_next"]:
                summary["move_to_next"] = True
                summary["rationale"] += " Moved to next stage due to conversation length."
            
            return json.dumps(summary)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in summary")
            return {
                "stress_level": "Unknown",
                "user_emotion": "Unknown",
                "eligible_for_therapy": False,
                "move_to_next": False,
                "rationale": "Error in parsing AI response"
            }