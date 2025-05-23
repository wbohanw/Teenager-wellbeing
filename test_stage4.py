from CBT_Logic.Stage_4 import TherapyImplementationStage, TherapyImplementationSummarizer
from typing import List, Dict
import json

def test_stage4():
    # Initialize the stage and summarizer
    stage = TherapyImplementationStage()
    summarizer = TherapyImplementationSummarizer()
    
    # Simulate a conversation history
    conversation_history: List[Dict[str, str]] = [
        {"role": "assistant", "content": "你好，我是Milo。今天想聊些什么呢？"},
        {"role": "user", "content": "我最近学习压力很大，经常感到焦虑。"},
        {"role": "assistant", "content": "我理解你的感受。能具体说说是什么让你感到压力吗？"},
        {"role": "user", "content": "马上就要期末考试了，我担心考不好。而且父母对我的期望很高。"},
        {"role": "assistant", "content": "听起来你同时面临着考试压力和家庭期望。这些压力让你有什么具体的感受吗？"},
        {"role": "user", "content": "我经常失眠，而且会感到心跳加快，有时候甚至不想去上学。"}
    ]
    
    # Test the therapy implementation stage with CBT
    chosen_therapy = "CBT"
    user_input = "我觉得我可能做不到父母期望的那样好。"
    
    # Process the input through the therapy implementation stage
    response = stage.process(user_input, conversation_history, chosen_therapy)
    print("\nTherapy Response:")
    print(response)
    
    # Add the response to conversation history
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": response})
    
    # Test the summarizer
    summary = summarizer.summarize(conversation_history, chosen_therapy)
    print("\nSession Summary:")
    print(json.dumps(json.loads(summary), indent=2))

if __name__ == "__main__":
    test_stage4() 