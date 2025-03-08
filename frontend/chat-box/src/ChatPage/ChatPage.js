import React, { useState, useEffect } from "react";
import "./ChatPage.css";
import { sendMessageToChatbot } from "../connector";
import welcome from "../videos/welcome.mov";
import random from "../videos/random.mov";
import hug from "../videos/hug.mov";
import temp from "../videos/temp.mp4";
import action1 from "../videos/action1.mp4";
import action2 from "../videos/action2.mp4";
import action3 from "../videos/action3.mp4";
import action4 from "../videos/action4.mp4";
import action5 from "../videos/action5.mp4";
import action6 from "../videos/action6.mp4";
import action7 from "../videos/action7.mp4";
import action8 from "../videos/action8.mp4";
import action9 from "../videos/action9.mp4";
import action10 from "../videos/action10.mp4";
import action11 from "../videos/action11.mp4";
import action12 from "../videos/action12.mp4";


function ChatPage() {
  const [messages, setMessages] = useState([
    { text: "你好，我是Milo, 今天感觉怎么样？", sender: "bot" },
  ]);
  const [inputText, setInputText] = useState("");
  const [videoIndex, setVideoIndex] = useState(0);
  const videos = [action1, action2, action3, action4, action5, action6, action7, action8, action9, action10, action11, action12];

  useEffect(() => {
    const timer = setInterval(() => {
      setVideoIndex((prev) => (prev + 1) % videos.length);
    }, 10000); // Change video every 10 seconds

    return () => clearInterval(timer);
  }, []);

  const sendMessage = async () => {
    if (inputText.trim() === "") return;

    const newMessages = [...messages, { text: inputText, sender: "user" }];
    setMessages(newMessages);
    setInputText("");

    const response = await sendMessageToChatbot(inputText);
    console.log(response);
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
      <video 
        key={videoIndex}
        autoPlay 
        loop 
        muted 
        className="background-video"
      >
        <source src={videos[videoIndex]} type="video/mp4" />
      </video>
      
      {/* <div className="character-panel">
        <h2>Good Morning, Jane 👋</h2>
        <p>Milo</p>
      </div> */}

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

      <div className="button-container">
        <button className="absolute-button">Random action</button>
        <button className="absolute-button">Action welcome</button>
        <button className="absolute-button">Action happy</button>
        <button className="absolute-button">Action wait</button>
        <button className="absolute-button">Action nod</button>
        <button className="absolute-button">Action idle</button>
      </div>
    </div>
  );
}

export default ChatPage;
