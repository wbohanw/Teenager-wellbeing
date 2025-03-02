from datetime import datetime, timedelta
import json
from typing import List, Dict


class TherapyScheduler:
    def __init__(self):
        self.follow_up_data = {}
        
    def schedule_follow_up(self, user_id: str, chosen_therapy: str, conversation_history: List[Dict[str, str]]):
        """Schedule a follow-up check for 3 days after the therapy session"""
        follow_up_date = datetime.now() + timedelta(days=3)
        
        # Extract key advice and exercises from the conversation
        recent_advice = self._extract_recent_advice(conversation_history)
        
        self.follow_up_data[user_id] = {
            'therapy_type': chosen_therapy,
            'advice_given': recent_advice,
            'follow_up_date': follow_up_date,
            'check_in_count': 0
        }
        
        return (
            f"\n\nI'll check in with you in 3 days to see how you're doing with these "
            f"exercises and self-management strategies. You'll receive a notification, "
            f"and we can adjust the approach if needed. Is there a particular time of "
            f"day that works best for you?"
        )

    def _extract_recent_advice(self, conversation_history: List[Dict[str, str]]) -> List[str]:
        """Extract recent advice from conversation history"""
        recent_advice = []
        for message in reversed(conversation_history[-5:]):
            if message['role'] == 'assistant' and ('advice' in message['content'].lower() or 
                                                 'try' in message['content'].lower() or 
                                                 'could' in message['content'].lower()):
                recent_advice.append(message['content'])
        return recent_advice

    def create_follow_up_message(self, user_id: str) -> Dict:
        """Create personalized follow-up message based on user data"""
        user_data = self.follow_up_data.get(user_id)
        if not user_data:
            return None

        if user_data['check_in_count'] == 0:
            message = {
                'title': "TreePal Check-in",
                'content': (
                    f"Hi! How are you doing with the {user_data['therapy_type']} "
                    f"exercises and self-management strategies we discussed? Would you like to:"
                ),
                'options': [
                    "Share how it's going 😊",
                    "Get different advice 🤔",
                    "Talk about new challenges 💭"
                ]
            }
        else:
            message = {
                'title': "TreePal Follow-up",
                'content': (
                    "How have the adjusted strategies been working for you? "
                    "Would you like to:"
                ),
                'options': [
                    "Continue with current approach 👍",
                    "Try something different 🔄",
                    "Discuss new concerns 💭"
                ]
            }
        
        return message

    def process_follow_up_response(self, user_id: str, response: str) -> Dict:
        """Process user's response to follow-up and provide appropriate next steps"""
        user_data = self.follow_up_data.get(user_id)
        if not user_data:
            return None

        if "going well" in response.lower() or "continue" in response.lower():
            return {
                'content': (
                    "That's great to hear! Would you like to:\n"
                    "1. Continue with the current exercises\n"
                    "2. Try some additional strategies\n"
                    "3. Share specific successes or challenges"
                ),
                'requires_new_session': False
            }
        elif "different" in response.lower() or "new" in response.lower():
            return {
                'content': (
                    "I understand you'd like to try something different. Would you prefer to:\n"
                    "1. Modify the current exercises\n"
                    "2. Try a completely new approach\n"
                    "3. Start a new therapy session to reassess your needs"
                ),
                'requires_new_session': True
            }
        else:
            return {
                'content': (
                    "Thank you for sharing. Would you like to:\n"
                    "1. Discuss specific challenges you're facing\n"
                    "2. Get additional coping strategies\n"
                    "3. Start a fresh therapy session"
                ),
                'requires_new_session': True
            }