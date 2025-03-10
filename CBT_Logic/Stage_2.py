from CBT_ import ChatGPTResponseGenerator, ChatGPTDialogueSummarizer
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from typing import List, Dict

class ExploreFormulationStage(ChatGPTResponseGenerator):
    def __init__(self):
        super().__init__(
        base_instruction="""
        if the user is in using Chinese, please give the response in Chinse as well. 
    There is the chat_history: {self.conversation_history}
    Your role: You are a CBT logic assistant exploring and formulating the patient's experiences.
    Your task: Explore the patient's past experiences and gain comprehensive insights into their cognitive patterns and problems.
    Please always remember the patient is a teenager, who is 12-18 years old. 
    
    ** If you have already have already detected issues from the chat history and the emotions, no need to repeat asking same question, and move forward asking more details.


    Guidelines:
    - Ask open-ended questions to encourage the patient to share more about their experiences.
    - Focus on understanding the patient's thought processes, beliefs, and behaviors.
    - Use techniques like Socratic questioning to help the patient reflect on their experiences.
    - Be empathetic and non-judgmental in your responses.
    - Gradually work towards formulating a preliminary understanding of the patient's cognitive patterns.
    - Pay attention to recurring themes or patterns in the patient's responses.
    - Explore how the patient's thoughts, feelings, and behaviors are interconnected.
    - Ask only one question at a time to avoid overwhelming the teenager.
    Example prompts:
    - "Can you tell me more about a recent situation where you felt [emotion they previously mentioned]? What thoughts went through your mind at that time?"
    - "How do you typically respond when you're in situations like the one you described?"
    - "What beliefs about yourself or the world do you think might be influencing your thoughts in these situations?"
    - "How have these patterns of thinking affected your daily life or relationships?"

   Note: answer a question at a time! Do not overwhelm the user.
    """
        )
    def process(self, user_input: str) -> str:
        prompt = f"{self.base_instruction}\n\nUser: {user_input}\n\nTherapist:"
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}])
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
        (2) user_emotion: The primary emotion the user is experiencing
        (3) eligible_for_therapy: Boolean indicating whether the user is eligible for therapy
        (4) move_to_next: Boolean indicating if it's reasonable to proceed to the next phase
        (5) rationale: Explanation of how the above properties were derived

        Guidelines for determining `move_to_next`:
        - Set to `true` if the user has clearly expressed their primary concerns.
        - Set to `true` if the conversation has sufficiently explored the user's emotions and experiences.
        - Set to `true` if rapport has been established.
        - Set to `true` if the dialogue has lasted more than 5 turns.
        - Otherwise, set to `false`.

        Example:

        ### Input:
        [
            {"role": "assistant", "content": "你今天想聊些什么呢？"},
            {"role": "user", "content": "我最近学习压力很大，感觉快撑不住了。"},
            {"role": "assistant", "content": "听起来你承受了很大的压力，是什么让你感到如此焦虑呢？"},
            {"role": "user", "content": "我有很多作业，还要准备考试，感觉根本做不完。"},
            {"role": "assistant", "content": "你的焦虑主要是因为学业负担太重，对吗？"},
            {"role": "user", "content": "是的，我每天都在担心自己跟不上进度。"}
        ]

        ### Output:
        {
            "stress_level": "high",
            "user_emotion": "overwhelmed",
            "eligible_for_therapy": true,
            "move_to_next": true,
            "rationale": "The user has explicitly stated feeling overwhelmed due to academic stress. Their emotions and concerns have been discussed over multiple turns, making it reasonable to proceed."
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
        stage_2_start_index = 0
        for i, msg in enumerate(dialogue):
            if msg['role'] == 'assistant' and 'we are now moving to the next stage' in msg['content'].lower():
                stage_2_start_index = i + 1
        
        stage_2_messages = dialogue[stage_2_start_index:]
        user_messages_in_stage = [msg for msg in stage_2_messages if msg['role'] == 'user']
        
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
                "stress_level": "Moderate",
                "user_emotion": "Unknown",
                "eligible_for_therapy": True,
                "move_to_next": len(user_messages_in_stage) >= 3,  # Now safely accessible
                "rationale": "Error parsing response, moving to next stage based on conversation length."
            })