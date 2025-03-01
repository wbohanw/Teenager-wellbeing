import React from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css"; 

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="landing-chat-box">
        <span className="greeting">
          👋 <span>Hello, I am Milo</span>
        </span>

        <button className="chat-button" onClick={() => navigate("/chat")}>
          Let's Chat
        </button>
      </div>
    </div>
  );
}

export default LandingPage;
