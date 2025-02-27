import openai
from CBT_agent import CBTAgent
from typing import List, Dict
from Stage_1 import AssessmentSummarizer, AssessmentStage
from Stage_2 import ExploreFormulationStage, ExploreFormulationSummarizer
from Stage_3 import InformationGatheringStage, InformationGatheringSummarizer
from Stage_4 import TherapyImplementationSummarizer, TherapyImplementationStage
from Therapy_Router import TherapyRouter
from Alert_agent import AlertAgent
import os
from dotenv import load_dotenv
import json
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class CBTChatbot:
    def __init__(self, api_key):
        self.agent = CBTAgent()
        self.alert_agent = AlertAgent(api_key)
        self.therapy_router = TherapyRouter(api_key)
        self.stages = [
            (AssessmentStage(), AssessmentSummarizer()),
            (ExploreFormulationStage(), ExploreFormulationSummarizer()),
            (InformationGatheringStage(), InformationGatheringSummarizer()),
            (TherapyImplementationStage(), TherapyImplementationSummarizer()),
        ]
        self.conversation_history: List[Dict[str, str]] = []
        self.chosen_therapy = None
        self.therapy_rationale = None

    def chat(self, user_input: str) -> str:
        
        if self.agent.current_stage < 3:
            return self.process_early_stages(user_input)
        elif self.agent.current_stage == 3 and self.chosen_therapy is None:
            if user_input == "1":
                print(self.user_choose_therapy())
                therapy_choice = input("1, 2 or 3: ")
                return self.process_chosen_therapy(therapy_choice)
            elif user_input == "2":
                self.chosen_therapy, self.therapy_rationale = self.therapy_router.route(self.conversation_history)
                self.agent.advance_stage()
                return self.process_chosen_therapy("Let's begin our therapy session.")
            else:
                return "I'm sorry, I didn't understand that choice. Please enter 1 to choose a therapy yourself, or 2 to have me suggest one."
        else:
            return self.process_chosen_therapy(user_input)

    def process_early_stages(self, user_input: str) -> str:
        current_stage, current_summarizer = self.stages[self.agent.current_stage]

        self.conversation_history.append({"role": "user", "content": user_input})
        
        summary_json = current_summarizer.summarize(self.conversation_history)
        
        # Check if we should advance to the next stage
        if self.agent.should_advance_stage(summary_json):
            self.agent.advance_stage()
            if self.agent.current_stage == 3:
                return self.get_therapy_choice_prompt()
            else:
                # If we've advanced to any other stage, process the input in the new stage
                next_stage, next_summarizer = self.stages[self.agent.current_stage]
                response = next_stage.process(user_input)
                response_text = response
        else:
            # If we're not advancing, process the input in the current stage
            response = current_stage.process(user_input)
            response_text = response
        
        self.conversation_history.append({"role": "assistant", "content": response_text})
        
        return response_text

    def get_therapy_choice_prompt(self) -> str:
        prompt = f"""
        if the user is in using Chinese, please give the response in Chinse as well. 
        The user has reached stage 3 of the therapy session. Provide the following message in the same language as the user's last input:

        We've gathered important information. Now, let's determine the best approach to help you further.
        Would you like to choose a specific therapy approach, or would you prefer that I suggest one based on our conversation?
        1. I'd like to choose
        2. Milo suggest one for me
        Please enter 1 or 2.

        User's last input: {self.conversation_history[-1]['content']}
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content

    # def route_therapy(self, user_input: str) -> str:
    #     if user_input == "1":
    #         self.user_choose_therapy()

    #     elif user_input == "2":
    #         self.chosen_therapy, self.therapy_rationale = self.therapy_router.route(self.conversation_history)
    #         self.agent.advance_stage()
    #         return self.process_chosen_therapy("Let's begin our therapy session.")
    #     else:
    #         return "I'm sorry, I didn't understand that choice. Please enter 1 to choose a therapy yourself, or 2 to have me suggest one."

    def user_choose_therapy(self) -> str:
        prompt = f"""
        if the user is in using Chinese, please give the response in Chinse as well. 
        Provide the following message in the same language as the user's last input:

        Thank you, you will choose your your favorite therapy! Here are the therapy approaches available:
        1. CBT (Cognitive Behavioral Therapy)
        2. DBT (Dialectical Behavior Therapy)
        3. REBT (Rational Emotive Behavior Therapy)
        Please enter 1, 2, or 3 to choose your preferred therapy approach.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def process_chosen_therapy(self, user_input: str) -> str:
        if self.chosen_therapy is None:
            therapies = ["CBT", "DBT", "REBT"]
            if user_input in ["1", "2", "3"]:
                self.chosen_therapy = therapies[int(user_input) - 1]
                self.agent.advance_stage()  # Move to stage 4
            else:
                return "I'm sorry, I didn't understand that choice. Please enter 1 for CBT, 2 for DBT, or 3 for REBT."

        prompt = f"""
        You are a therapist specializing in {self.chosen_therapy}. Use {self.chosen_therapy} techniques to help the teenager based on the conversation history.

        For CBT: Focus on identifying and changing negative thought patterns and behaviors.
        For DBT: Emphasize acceptance and validation while teaching skills for change. Focus on mindfulness, distress tolerance, emotion regulation, and interpersonal effectiveness.
        For REBT: Target irrational beliefs and aim to develop more rational thinking for positive emotions. Use the ABC model.

        Conversation history: {json.dumps(self.conversation_history, indent=2)}

        User input: {user_input}

        Provide a therapy response in the same language as the user's input:
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        therapy_response = response.choices[0].message.content
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": therapy_response})
        return therapy_response

    def alert(self, user_input: str) -> str:
        try:
            alert_analysis = self.alert_agent.analyze_conversation(user_input, self.conversation_history)
            if alert_analysis["concern"]:
                if self.alert_agent.should_alert():
                    return self.alert_agent.get_alert_message()
                else:
                    print(f"Concern detected ({self.alert_agent.self_harm_count}/3): {alert_analysis['reason']}")
        except Exception as e:
            print(f"Error in alert system: {e}")
        return ""

    def get_current_stage_name(self) -> str:
        return self.agent.get_current_stage()

    def get_stage_progress(self) -> str:
        return self.agent.get_stage_progress()

if __name__ == "__main__":
    api_key = os.environ.get("OPENAI_API_KEY")
    chatbot = CBTChatbot(api_key)

    print("CBT Chatbot initialized. Type 'quit' to exit.")

    while True:
        print(f"\n{chatbot.get_stage_progress()}")
        user_input = input("User: ")

        if user_input.lower() == 'quit':
            break

        response = chatbot.chat(user_input)
        print("---------------------------------------------")
        
        alert_message = chatbot.alert(user_input)
        if alert_message:
            print("ALERT:", alert_message)
            break
        else:
            print("Chatbot:", response)

        if "Therapy session completed" in response:
            print(chatbot.conversation_history)
            break
            
    print("Chatbot session ended.")