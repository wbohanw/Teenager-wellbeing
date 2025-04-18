import json
import os
from typing import Dict, Optional

class UserPreferences:
    def __init__(self):
        self.preferences_dir = "user_data"
        if not os.path.exists(self.preferences_dir):
            os.makedirs(self.preferences_dir)
    
    def save_preferences(self, user_id: str, preferences: Dict) -> bool:
        try:
            file_path = os.path.join(self.preferences_dir, f"{user_id}_preferences.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False
    
    def get_preferences(self, user_id: str) -> Optional[Dict]:
        try:
            file_path = os.path.join(self.preferences_dir, f"{user_id}_preferences.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading preferences: {e}")
            return None

# Create a global instance
preferences_manager = UserPreferences() 