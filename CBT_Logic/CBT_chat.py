import openai
from CBT_agent import CBTAgent
from typing import List, Dict
from Stage_1 import AssessmentSummarizer, AssessmentStage
from Stage_2 import ExploreFormulationStage, ExploreFormulationSummarizer
from Stage_3 import InformationGatheringStage, InformationGatheringSummarizer
from Stage_4 import TherapyImplementationSummarizer, TherapyImplementationStage
from Therapy_Router import TherapyRouter
from schedule import TherapyScheduler
from Alert_agent import AlertAgent
import os
from dotenv import load_dotenv
import json
from openai import OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
load_dotenv()

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
        self.user_emotion = None
        self.conversation_history: List[Dict[str, str]] = []
        self.chosen_therapy = None
        self.therapy_rationale = None
        self.scheduler = TherapyScheduler()
        self.user_id = None
        self.click = False
        self.suggestion = None
        self.end_session = False
        self.preferences = None

    def update_preferences(self, preferences):
        """Update the chatbot's preferences"""
        self.preferences = preferences
        print(f"Updated preferences for user {self.user_id}: {preferences}")

    def get_prompt_with_preferences(self, base_prompt: str) -> str:
        """Enhance the base prompt with user preferences"""
        if not self.preferences:
            return base_prompt

        personality_traits = self.preferences.get('personalityTraits', [])
        tone = self.preferences.get('tone', '')
        language = self.preferences.get('language', '')
        
        # Add personality traits to the prompt
        if personality_traits:
            traits_str = ", ".join(personality_traits)
            base_prompt += f"\nPlease maintain a {traits_str} personality in your responses."
        
        # Add tone preference
        if tone:
            base_prompt += f"\nUse a {tone} tone in your responses."
        
        # Add language preference
        if language:
            base_prompt += f"\nRespond in {language}."
        
        return base_prompt

    def chat(self, user_input: str) -> str:
        if self.agent.current_stage < 3:
            return self.process_early_stages(user_input)
        elif self.agent.current_stage == 3 and self.chosen_therapy is None:
            return self.route_therapy(user_input)
        else:
            self.click = False
            self.end_session = True
            return self.process_rag_advice(user_input)

    def process_chosen_therapy(self, user_input: str) -> str:
        base_prompt = f"""
        You are a therapist specializing in {self.chosen_therapy}. Use {self.chosen_therapy} techniques to help the teenager based on the conversation history.

        For CBT: Focus on identifying and changing negative thought patterns and behaviors.
        For DBT: Emphasize acceptance and validation while teaching skills for change. Focus on mindfulness, distress tolerance, emotion regulation, and interpersonal effectiveness.
        For REBT: Target irrational beliefs and aim to develop more rational thinking. Use the ABC model.

        Conversation history: {json.dumps(self.conversation_history, indent=2)}

        User input: {user_input}

        Therapist response:
        """
        
        # Enhance the prompt with user preferences
        prompt = self.get_prompt_with_preferences(base_prompt)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        therapy_response = response.choices[0].message.content
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": therapy_response})
        return therapy_response

    def process_early_stages(self, user_input: str) -> str:
        current_stage, current_summarizer = self.stages[self.agent.current_stage]
        self.conversation_history.append({"role": "user", "content": user_input})
        response = current_stage.process(user_input, self.preferences, self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": response})
        
        try:
            summary_json = current_summarizer.summarize(self.conversation_history)
            summary = json.loads(summary_json)
            print(f"Stage summary: {summary}")
            self.user_emotion = summary.get('user_emotion', 'Unknown')
            
            if summary.get("move_to_next", "True"):
                self.agent.advance_stage()
                if self.agent.current_stage == 3:
                    return self.therapy_router.route(self.conversation_history)
        except json.JSONDecodeError as e:
            print(f"Error parsing summary JSON: {e}")
            # Continue with default values if JSON parsing fails
            self.user_emotion = 'Unknown'
        
        return response

    def route_therapy(self, user_input: str) -> str:
        try:
            self.chosen_therapy, self.therapy_rationale = self.therapy_router.route(self.conversation_history, self.preferences)
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": self.therapy_rationale})
            self.agent.advance_stage()
            self.click = True
            return self.chat(user_input)
        except Exception as e:
            print(f"Error in therapy routing: {e}")
            # Fallback response
            self.chosen_therapy = "CBT"
            self.therapy_rationale = "Based on our conversation, Cognitive Behavioral Therapy (CBT) would be most helpful for you. Let's continue with this approach."
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": self.therapy_rationale})
            self.agent.advance_stage()
            self.click = True
            return self.chat(user_input)

    def process_rag_advice(self, user_input: str) -> str:
        current_stage, current_summarizer = self.stages[3]  # RAGAdviceStage
        
        response = current_stage.process(user_input, self.conversation_history, self.chosen_therapy, self.preferences)
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        try:
            summary_json = current_summarizer.summarize(self.conversation_history, self.chosen_therapy)
            if summary_json:
                summary = json.loads(summary_json)
                print(f"RAG advice summary: {summary}")
                
                if summary.get('retrieve_new_advice', False):
                    response = current_stage.process(user_input, self.conversation_history, self.chosen_therapy, self.preferences)
                    self.conversation_history.append({"role": "assistant", "content": response})
                    self.end_session = True
                
                if not summary.get('continue_session', True):
                    return "Our therapy sessions have come to an end. I hope you've found them helpful. Remember to practice the techniques we've discussed. If you need further support in the future, don't hesitate to seek help."
        except json.JSONDecodeError as e:
            print(f"Error parsing RAG advice summary JSON: {e}")
            # Continue with the current response if JSON parsing fails
            pass
        except Exception as e:
            print(f"Error in RAG advice processing: {e}")
            # Continue with the current response if any other error occurs
            pass
        
        return response
        
    def alert(self, user_input: str) -> str:
        try:
            alert_analysis = self.alert_agent.analyze_conversation(user_input, self.conversation_history)
            if alert_analysis["concern"]:
                if self.alert_agent.should_alert():
                    return self.alert_agent.get_alert_message()
                else:
                    print(f"Concern detected ({self.alert_agent.self_harm_count}/3): {alert_analysis['reason']}")
        except Exception as e:
            print(f" ")
        return ""
        
    def get_current_stage_name(self) -> str:
        return self.agent.get_current_stage()

    def get_stage_progress(self) -> str:
        return self.agent.get_stage_progress()

    def complete_session(self):
        if self.user_id and self.chosen_therapy:
            follow_up_message = self.scheduler.schedule_follow_up(
                self.user_id,
                self.chosen_therapy,
                self.conversation_history
            )
            return (
                "Our session is complete. Remember to practice the techniques "
                f"we've discussed. {follow_up_message}"
            )

    
if __name__ == "__main__":
    # Test case
    api_key =  os.environ.get("OPENAI_API_KEY") # Replace with your actual OpenAI API key
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