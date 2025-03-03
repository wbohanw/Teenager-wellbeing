import React, { useState } from "react";
import "./ChatPage.css";
import miloImg from "../images/milo.png";
import { sendMessageToChatbot } from "../connector";

function ChatPage() {
  const [messages, setMessages] = useState([
    { text: "你好，我是Milo, 今天感觉怎么样？", sender: "bot" },
  ]);
  const [inputText, setInputText] = useState("");

  const sendMessage = async () => {
    if (inputText.trim() === "") return;

    const newMessages = [...messages, { text: inputText, sender: "user" }];
    setMessages(newMessages);
    setInputText("");

    const response = await sendMessageToChatbot(inputText);
    if (response.response) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: response.response, sender: "bot" },
      ]);
    }
  };

    
  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); 
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="character-panel">
        <h2>Good Morning, Jane 👋</h2>
        <img src={miloImg} alt="Milo" className="milo-image" />
        <p>Milo</p>
      </div>

      <div className="chat-box">
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`chat-bubble ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>

        <div className="chat-input">
          <input
            type="text"
            placeholder="How do you feel today?"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button onClick={sendMessage}>
            <svg viewBox="0 0 24 24">
              <path d="M2 21L23 12L2 3V10L17 12L2 14V21Z"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
