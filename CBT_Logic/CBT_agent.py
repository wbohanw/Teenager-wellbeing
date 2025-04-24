import json

class CBTAgent:
    def __init__(self):
        self.current_stage = 0
        self.stages = [
            "Pre-Stage",
            "Assessment",
            "Explore & Formulation",
            "Information Gathering",
            "Therapy Implementation"
        ]
        self.stage_completion_criteria = {
            "Pre-Stage": self._pre_stage_completion,
            "Assessment": self._assess_stage_completion,
            "Explore & Formulation": self._explore_formulation_stage_completion,
            "Information Gathering": self._information_gathering_stage_completion,
            "Therapy Implementation": self._therapy_implementation_stage_completion
        }

    def should_advance_stage(self, summary_json):
        summary = json.loads(summary_json)
        
        return summary.get("move_to_next", False)
    
    def advance_stage(self) -> None:
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
            print(f"Advanced to stage: {self.get_current_stage()}")

    def get_current_stage(self):
        return self.stages[self.current_stage]

    def is_therapy_complete(self):
        return self.current_stage >= len(self.stages) - 1

    def _assess_stage_completion(self, summary):
        return (
            summary.get('move_to_next', False) and
            summary.get('stress_level') and
            summary.get('user_emotion')
        )

    def _explore_formulation_stage_completion(self, summary):
        return (
            summary.get('move_to_next', False) and
            len(summary.get('identified_patterns', [])) > 0 and
            len(summary.get('behavioral_tendencies', [])) > 0
        )

    def _information_gathering_stage_completion(self, summary):
        return (
            summary.get('move_to_next', False) and
            len(summary.get('key_issues', [])) > 0 and
            summary.get('emotional_patterns') and
            len(summary.get('coping_mechanisms', [])) > 0
        )

    def _therapy_implementation_stage_completion(self, summary):
        return (
            summary.get('move_to_next', False) and
            summary.get('therapy_progress', False)
        )

    def _pre_stage_completion(self, summary):
        return (
            summary.get('move_to_next', False) and
            summary.get('user_name') and
            len(summary.get('interests', [])) > 0
        )

    def get_stage_progress(self):
        return f"Stage {self.current_stage + 1} of {len(self.stages)}: {self.get_current_stage()}"

    def reset(self):
        self.current_stage = 0