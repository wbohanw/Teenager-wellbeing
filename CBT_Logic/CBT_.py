from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
import json
import os
import time
import re
from dotenv import load_dotenv

class ChatGPTResponseGenerator:
    def __init__(self, base_instruction):
        self.model = "gpt-4o-mini"
        self.base_instruction = base_instruction

    def generate_response(self, user_input):
        response = client.chat.completions.create(model=self.model,
        messages=[
            {"role": "system", "content": self.base_instruction},
            {"role": "user", "content": user_input}
        ])
        return response.choices[0].message.content


class ChatGPTDialogueSummarizer:
    def __init__(self, base_instruction, examples, gpt_params, dialogue_filter):
        self.base_instruction = base_instruction
        self.examples = examples
        self.gpt_params = gpt_params
        self.dialogue_filter = dialogue_filter

    def summarize_dialogue(self, dialogue_history):
        filtered_dialogue = self.dialogue_filter(dialogue_history, self.gpt_params)
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": self.base_instruction},
            {"role": "user", "content": json.dumps(filtered_dialogue)}
        ])
        return json.loads(response.choices[0].message.content)


