import openai
import json
from typing import List, Dict, Tuple
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from typing import List, Dict

class TherapyRouter:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def route(self, chat_history: List[Dict[str, str]]) -> Tuple[str, str]:
        chat = "\n".join([f"{turn['role'].capitalize()}: {turn['content']}" for turn in chat_history])
        prompt = f"""
        if the user is in using Chinese, please give the response in Chinse as well. 
        Based on the following conversation history, determine the most appropriate therapy approach for the teenager. Choose from CBT (Cognitive Behavioral Therapy), DBT (Dialectical Behavior Therapy), or REBT (Rational Emotive Behavior Therapy).

        Conversation History:
        {chat}

        Consider the following therapy descriptions:

        1. CBT (Cognitive Behavioral Therapy):
        - Focuses on identifying and changing negative thought patterns and behaviors.
        - Helps individuals understand the connection between thoughts, feelings, and behaviors.
        - Suitable for anxiety, depression, and various mood disorders.

        2. DBT (Dialectical Behavior Therapy):
        - Emphasizes acceptance and change strategies.
        - Focuses on four main areas: mindfulness, distress tolerance, emotion regulation, and interpersonal effectiveness.
        - Particularly effective for individuals with intense emotions or self-destructive behaviors.

        3. REBT (Rational Emotive Behavior Therapy):
        - Targets irrational beliefs and aims to develop more rational thinking.
        - Uses the ABC model (Activating event, Belief, Consequence) to understand and change thought patterns.
        - Effective for individuals with rigid thinking patterns or extreme beliefs.

        Based on the teenager's presented issues, emotional state, and thought patterns, which therapy would be most beneficial?

        Provide your response in the following JSON format:
        {{
            "chosen_therapy": "CBT/DBT/REBT",
            "rationale": "Detailed explanation for why this therapy was chosen based on the teenager's information"
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )  

        result = json.loads(response.choices[0].message.content)
        return result["chosen_therapy"], result["rationale"]
    
def test_therapy_router():
    # Sample conversation history
    sample_history = [
        {"role": "user", "content": "I feel very depressed and anxious all the time."},
        {"role": "assistant", "content": "I'm sorry to hear that you're feeling this way. Can you tell me more about what's been happening?"},
        {"role": "user", "content": "I can't stop thinking negative thoughts about myself. I feel like I'm not good enough."},
        {"role": "assistant", "content": "It sounds like you're experiencing some challenging thoughts. How long have you been feeling this way?"},
        {"role": "user", "content": "For a few months now. I've been struggling with school and my relationships."},
    ]

    # Initialize TherapyRouter
    router = TherapyRouter(api_key)

    # Get therapy recommendation
    chosen_therapy, rationale = router.route(sample_history)

    print(f"Chosen Therapy: {chosen_therapy}")
    print(f"Rationale: {rationale}")

if __name__ == "__main__":
    test_therapy_router()