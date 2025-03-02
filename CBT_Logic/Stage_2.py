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
            base_instruction="""
            based on the following conversation history: {self.conversation_history}
- Analyze the dialogue history to determine if sufficient exploration and formulation have occurred.
- Look for key cognitive patterns, recurring thoughts, and behavioral tendencies in the user's responses.
- Determine if enough information has been gathered to move to the next stage.
- Use JSON format with the following properties:
    (1) identified_patterns: Array of cognitive patterns or recurring thoughts identified.
    (2) behavioral_tendencies: Array of notable behavioral tendencies observed.
    (3) underlying_beliefs: Array of underlying beliefs or assumptions identified.
    (4) move_to_next: Boolean indicating whether to proceed to the next stage.
    (5) rationale: Explanation for the decision to move or not move to the next stage.
""",
            examples=[(
                [
                {"role": "assistant", "content": "你能告诉我最近一次感到焦虑的情况吗？当时你的想法是什么？"},
                {"role": "user", "content": "上周我有个重要的考试，我一直担心自己会失败。我觉得如果考砸了，我就是个失败者。"},
                {"role": "assistant", "content": "听起来你对考试结果有很大的压力。你为什么觉得考试成绩能决定你是否是个失败者呢？"},
                {"role": "user", "content": "因为我觉得如果我不能在每件事上都做到最好，那就意味着我不够优秀。"}
                ],
                json.dumps({
                    'identified_patterns': ['黑白思维', '过度概括化'],
                    'behavioral_tendencies': ['在压力情况下感到焦虑', '对自己要求过高'],
                    'underlying_beliefs': ['考试成绩不理想只是学习过程的一部分，不代表整体价值'],
                    'move_to_next': True,
                    'rationale': "We have identified key cognitive patterns and behavioral tendencies. The user has shared enough information about their thought processes to move to the next stage."
                })
            )],
            gpt_params={"temperature": 0.1},
            dialogue_filter=lambda dialogue, _: dialogue[-3:]
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