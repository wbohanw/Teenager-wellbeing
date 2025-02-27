# import os
# from dotenv import load_dotenv
# from CBT_chat import CBTChatbot

# load_dotenv()

# def test_therapy_selection():
#     api_key = os.getenv("OPENAI_API_KEY")
#     chatbot = CBTChatbot(api_key)

#     # Simulate conversation history up to stage 3
#     chatbot.conversation_history = [
#         {"role": "user", "content": "我最近感觉很沮丧。"},
#         {"role": "assistant", "content": "我很抱歉听到你最近感到沮丧。能告诉我更多关于你的感受吗？是什么让你感到沮丧呢？"},
#         {"role": "user", "content": "我在学校的成绩一直不好，感觉很失败。"},
#         {"role": "assistant", "content": "我理解这种感觉确实很难受。学习成绩并不能定义一个人的全部价值。你能告诉我你在其他方面有什么擅长的吗？"},
#         {"role": "user", "content": "我比较擅长音乐和绘画，但感觉这些不重要。"},
#         {"role": "assistant", "content": "音乐和绘画是非常宝贵的才能！它们同样重要。你有没有想过如何将这些才能与你的学习结合起来呢？"},
#         {"role": "user", "content": "我没想过，但也许可以试试。"},
#         {"role": "assistant", "content": "这是个很好的想法！结合你的兴趣可能会让学习变得更有趣。我们已经收集了重要的信息，现在让我们来决定接下来的治疗方向。"}
#     ]

#     # Set the current stage to 3
#     chatbot.agent.current_stage = 3

#     print("Test 1: User chooses to select therapy")
#     response = chatbot.chat("1")
#     print("Chatbot:", response)
    
#     print("\nTest 2: User selects CBT")
#     response = chatbot.chat("1")
#     print("Chatbot:", response)
    
#     print("\nTest 3: Begin therapy session")
#     response = chatbot.chat("我该如何提高自信心？")
#     print("Chatbot:", response)

#     print("\nTest 4: Another therapy interaction")
#     response = chatbot.chat("但我总是觉得自己不够好。")
#     print("Chatbot:", response)

#     print("\nFinal stage:", chatbot.get_current_stage_name())

# if __name__ == "__main__":
#     test_therapy_selection()

    

import os
from dotenv import load_dotenv
from Stage_4 import TherapyImplementationStage, TherapyImplementationSummarizer  # Replace 'your_module' with the actual module name

load_dotenv()

def test_therapy_implementation():
    api_key = os.getenv("OPENAI_API_KEY")
    stage = TherapyImplementationStage()
    summarizer = TherapyImplementationSummarizer()

    # Simulated conversation history
    conversation_history = [
        {"role": "user", "content": "我最近总是感到很焦虑，特别是在学校里。"},
        {"role": "assistant", "content": "我理解你的感受。能告诉我更多关于在学校里让你感到焦虑的具体情况吗？"},
        {"role": "user", "content": "每次要做演讲或者小组讨论时，我就会特别紧张，害怕说错话。"},
        {"role": "assistant", "content": "这种感觉很常见。你尝试过什么方法来缓解这种紧张感吗？"},
        {"role": "user", "content": "我试过深呼吸，但好像没什么用。我还是会感到很不安。"}
    ]

    # Test case 1: CBT approach
    print("Test Case 1: CBT Approach")
    user_input = "我该怎么做才能不那么害怕在班上发言呢？"
    response = stage.process(user_input, conversation_history, "CBT")
    print("CBT Response:", response)


    # Test case 2: DBT approach
    print("\nTest Case 2: DBT Approach")
    user_input = "我感觉自己总是控制不住情绪，特别是当别人批评我的时候。"
    response = stage.process(user_input, conversation_history, "DBT")
    print("DBT Response:", response)

    # Test summarizer
    print("\nTesting Summarizer")
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": response})
    summary = summarizer.summarize(conversation_history, "DBT")
    print("Session Summary:", summary)

if __name__ == "__main__":
    test_therapy_implementation()