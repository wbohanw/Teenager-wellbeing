import React, { useState, useEffect, useRef } from "react";
import "./ChatPage.css";
import { sendMessageToChatbot, savePreferencesToBackend } from "../connector";
import happy from "../videos/happy.mov";
import sad from "../videos/sad.mov";
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
import { useLocation } from "react-router-dom";

function ChatPage() {
  // State
  const [messages, setMessages] = useState([
    { text: "你好，我是Milo, 今天感觉怎么样？", sender: "bot", timestamp: new Date() },
  ]);
  const [inputText, setInputText] = useState("");
  const [currentVideo, setCurrentVideo] = useState(action2);
  const [showNextButton, setShowNextButton] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const [showPreferences, setShowPreferences] = useState(false);
  const [preferences, setPreferences] = useState(
    location.state?.preferences || JSON.parse(localStorage.getItem('chatPreferences')) || {}
  );
  
  // Add these states for preferences
  const [language, setLanguage] = useState(preferences.language || '');
  const [purpose, setPurpose] = useState(preferences.purpose || '');
  const [selectedTraits, setSelectedTraits] = useState(preferences.personalityTraits || []);
  const [selectedTone, setSelectedTone] = useState(preferences.tone || '');
  const [selectedTitle, setSelectedTitle] = useState(preferences.titlePreference || '');
  const [selectedProperNouns, setSelectedProperNouns] = useState(preferences.properNouns || []);
  
  // Refs
  const chatEndRef = useRef(null);
  const videoRef = useRef(null);
  const intervalRef = useRef(null);
  const timeoutRef = useRef(null);
  
  // Video management
  const defaultVideos = [action2, action3, action4, action5, action6, action7, action8, action9, action10, action11, action12];
  const actionVideos = {
    happy: happy,
    sad: sad,
    welcome: action3,
    thinking: action4,
    waiting: action5,
    nodding: action6,
    random: action7,
    idle: action8,
  };

  // Add these constants for preferences options
  const personalityTraits = [
    'Openness', 'Closedness', 'Agreeable', 'Non-Agreeable', 'Conscientiousness', 'Unconscientiousness',
    'Extroverted', 'Introverted', 'Optimistic', 'Pessimistic',
    'Helpful', 'Attentive', 'Efficient', 'Intelligent', 'Guiding',
    'Sensitive', 'Empathetic', 'Curious', 'Amusing', 'Supportive', 'Inquisitive',
    'Funny', 'Unpredictable', 'Snarky', 'Cute', 'Weird', 'Unusual', 'Charismatic', 'Bold', 'Creative',
    'Calm', 'Collected', 'Supportive', 'Caring', 'Non-judgmental', 'Motivational',
    'Predictive', 'Co-operative', 'Task Orientated', 'Competent', 'Cooperative'
  ];

  const tones = [
    'Formal', 'Casual', 'Imperative', 'Interrogative', 'Non-continuous Conversation', 'Relationship-oriented'
  ];

  const titles = [
    'Personal and Informal Titles', 'Professional and Formal Titles', 'Avoiding Use of Titles'
  ];

  const properNouns = ['내가', '제가'];
  
  // Initialize default video cycle
  useEffect(() => {
    startDefaultCycle();
    
    // Check for user's preferred color scheme
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    setDarkMode(prefersDark);
    
    if (prefersDark) {
      document.body.classList.add('dark');
    }
    
    return () => {
      clearInterval(intervalRef.current);
      clearTimeout(timeoutRef.current);
    };
  }, []);
  
  // Scroll to bottom when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // Start random video cycle
  const startDefaultCycle = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    // Set random idle video
    const randomIndex = Math.floor(Math.random() * defaultVideos.length);
    setCurrentVideo(defaultVideos[randomIndex]);
    
    // Start cycle
    intervalRef.current = setInterval(() => {
      setCurrentVideo(prev => {
        const availableVideos = defaultVideos.filter(video => video !== prev);
        const randomIndex = Math.floor(Math.random() * availableVideos.length);
        return availableVideos[randomIndex];
      });
    }, 10000);
  };

  // Play specific video once
  const playSpecificVideo = (videoKey) => {
    clearInterval(intervalRef.current);
    clearTimeout(timeoutRef.current);
    
    const videoToPlay = actionVideos[videoKey] || defaultVideos[0];
    setCurrentVideo(videoToPlay);
    
    // Return to default cycle after video duration
    const videoDuration = videoRef.current?.duration * 1000 || 5000;
    timeoutRef.current = setTimeout(() => {
      startDefaultCycle();
    }, videoDuration);
  };

  // Play emotion-based video
  const playEmotionVideo = (emotion) => {
    clearInterval(intervalRef.current);
    clearTimeout(timeoutRef.current);

    switch(emotion) {
      case 'happy':
        setCurrentVideo(happy);
        break;
      case 'sad':
        setCurrentVideo(sad);
        break;
      case 'neutral':
        const randomIndex = Math.floor(Math.random() * defaultVideos.length);
        setCurrentVideo(defaultVideos[randomIndex]);
        break;
      default:
        break;
    }

    // Return to idle videos after playing once
    const videoDuration = videoRef.current?.duration * 1000 || 5000;
    timeoutRef.current = setTimeout(() => {
      startDefaultCycle();
    }, videoDuration);
  };

  // Handle next button click
  const handleNext = async () => {
    setShowNextButton(false);
    setIsTyping(true);
    
    // Play thinking animation
    playSpecificVideo('thinking');
    
    const response = await sendMessageToChatbot("next");
    setIsTyping(false);
    
    if (response.response) {
      setMessages(prev => [
        ...prev, 
        { 
          text: response.response, 
          sender: "bot", 
          timestamp: new Date() 
        }
      ]);
      
      if (response.user_emotion) {
        playEmotionVideo(response.user_emotion.toLowerCase());
      }
    }
  };

  // Add these handlers for preferences
  const handleTraitToggle = (trait) => {
    if (selectedTraits.includes(trait)) {
      setSelectedTraits(selectedTraits.filter(t => t !== trait));
    } else {
      setSelectedTraits([...selectedTraits, trait]);
    }
  };

  const handleProperNounToggle = (noun) => {
    if (selectedProperNouns.includes(noun)) {
      setSelectedProperNouns(selectedProperNouns.filter(n => n !== noun));
    } else {
      setSelectedProperNouns([...selectedProperNouns, noun]);
    }
  };
  
  const savePreferences = async () => {
    const newPreferences = {
      language,
      purpose,
      personalityTraits: selectedTraits,
      tone: selectedTone,
      titlePreference: selectedTitle,
      properNouns: selectedProperNouns
    };
    
    // Save to localStorage
    localStorage.setItem('chatPreferences', JSON.stringify(newPreferences));
    setPreferences(newPreferences);
    
    // Send to backend
    await savePreferencesToBackend(newPreferences);
    
    setShowPreferences(false);
  };

  // Send message to chatbot
  const sendMessage = async () => {
    if (inputText.trim() === "") return;

    // Add user message
    const newMessages = [
      ...messages, 
      { 
        text: inputText, 
        sender: "user", 
        timestamp: new Date() 
      }
    ];
    
    setMessages(newMessages);
    setInputText("");
    
    // Show typing indicator and waiting animation
    setIsTyping(true);
    playSpecificVideo('waiting');

    // Get response from chatbot - Add preferences to the request
    const response = await sendMessageToChatbot(inputText, preferences);
    setIsTyping(false);
    
    if (response.response) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          text: response.response, 
          sender: "bot", 
          timestamp: new Date() 
        },
      ]);
      
      // Handle emotional response
      if (response.user_emotion) {
        playEmotionVideo(response.user_emotion.toLowerCase());
      }
      
      // Show next button if needed
      if (response.move_to_next) {
        setShowNextButton(true);
      }
    }
  };

  // Handle keyboard input
  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); 
      sendMessage();
    }
  };
  
  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark');
  };
  
  // Format timestamp
  const formatTimestamp = (timestamp) => {
    const now = new Date();
    const diff = Math.floor((now - timestamp) / 60000); // minutes
    
    if (diff < 1) return "just now";
    if (diff === 1) return "1 minute ago";
    if (diff < 60) return `${diff} minutes ago`;
    
    const hours = Math.floor(diff / 60);
    if (hours === 1) return "1 hour ago";
    if (hours < 24) return `${hours} hours ago`;
    
    return timestamp.toLocaleDateString();
  };

  return (
    <div className={`chat-container ${darkMode ? 'dark' : ''}`}>
      <div className="page-background"></div>
      
      {/* Navigation */}
      <div className="nav-bar">
        <div className="nav-logo">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
            <path d="M13 7h-2v6h2V7zm0 8h-2v2h2v-2z"/>
          </svg>
          Milo Chat
        </div>
        
        <div className="nav-links">
          <a href="#" className="nav-link">Home</a>
          <a href="#" className="nav-link">Profile</a>
          <a href="#" className="nav-link">Settings</a>
          <a href="#" className="nav-link">Help</a>
          
          {/* Add this button to open preferences */}
          <button className="nav-link preferences-btn" onClick={() => setShowPreferences(true)}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" />
            </svg>
            Preferences
          </button>
        </div>
        
        <button className="theme-toggle" onClick={toggleDarkMode}>
          {darkMode ? (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M12 9c1.65 0 3 1.35 3 3s-1.35 3-3 3-3-1.35-3-3 1.35-3 3-3m0-2c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M9.37 5.51c-.18.64-.27 1.31-.27 1.99 0 4.08 3.32 7.4 7.4 7.4.68 0 1.35-.09 1.99-.27C17.45 17.19 14.93 19 12 19c-3.86 0-7-3.14-7-7 0-2.93 1.81-5.45 4.37-6.49zM12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z" />
            </svg>
          )}
        </button>
        
        <button className="mobile-menu-toggle" onClick={() => setMobileMenuOpen(true)}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" />
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="mobile-menu open">
          <div className="mobile-menu-header">
            <div className="nav-logo">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                <path d="M13 7h-2v6h2V7zm0 8h-2v2h2v-2z"/>
              </svg>
              Milo Chat
            </div>
            <button className="mobile-menu-close" onClick={() => setMobileMenuOpen(false)}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" />
              </svg>
            </button>
          </div>
          <div className="mobile-links">
            <a href="#" className="mobile-link">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8h5z" />
              </svg>
              Home
            </a>
            <a href="#" className="mobile-link">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
              </svg>
              Profile
            </a>
            <a href="#" className="mobile-link">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" />
              </svg>
              Settings
            </a>
            <a href="#" className="mobile-link">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z" />
              </svg>
              Help
            </a>
          </div>
        </div>
      )}

      {/* Preferences Popup */}
      {showPreferences && (
        <div className="preferences-overlay">
          <div className="preferences-popup">
            <div className="preferences-header">
              <h2>Chat Preferences</h2>
              <button className="close-preferences" onClick={() => setShowPreferences(false)}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" />
                </svg>
              </button>
            </div>
            
            <div className="preferences-content">
              <div className="toggle-section">
                <label className="toggle">
                  <input type="checkbox" checked={true} readOnly />
                  <span className="toggle-slider"></span>
                </label>
                <span>Verbal Style Cues</span>
              </div>
              
              <div className="preference-group">
                <h3>Language</h3>
                <div className="input-with-button">
                  <input
                    type="text"
                    placeholder="Please enter"
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                  />
                </div>
              </div>

              <div className="preference-group">
                <h3>Conversation Purpose</h3>
                <div className="input-with-button">
                  <input
                    type="text"
                    placeholder="Please enter"
                    value={purpose}
                    onChange={(e) => setPurpose(e.target.value)}
                  />
                </div>
              </div>

              <div className="preference-group">
                <h3>Titles</h3>
                <div className="option-buttons">
                  {titles.map((title) => (
                    <button
                      key={title}
                      className={`option-button ${selectedTitle === title ? 'selected' : ''}`}
                      onClick={() => setSelectedTitle(title)}
                    >
                      {title}
                    </button>
                  ))}
                </div>
              </div>

              <div className="preference-group">
                <h3>Proper Nouns</h3>
                <div className="option-buttons">
                  {properNouns.map((noun) => (
                    <button
                      key={noun}
                      className={`option-button ${selectedProperNouns.includes(noun) ? 'selected' : ''}`}
                      onClick={() => handleProperNounToggle(noun)}
                    >
                      {noun}
                    </button>
                  ))}
                </div>
              </div>

              <div className="preference-group">
                <h3>Personality Traits</h3>
                <div className="trait-options">
                  {personalityTraits.map((trait) => (
                    <button 
                      key={trait} 
                      className={`trait-button ${selectedTraits.includes(trait) ? 'selected' : ''}`}
                      onClick={() => handleTraitToggle(trait)}
                    >
                      {trait}
                    </button>
                  ))}
                </div>
              </div>

              <div className="preference-group">
                <h3>Tone</h3>
                <div className="option-buttons">
                  {tones.map((tone) => (
                    <button
                      key={tone}
                      className={`option-button ${selectedTone === tone ? 'selected' : ''}`}
                      onClick={() => setSelectedTone(tone)}
                    >
                      {tone}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="preferences-actions">
              <button className="save-preferences" onClick={savePreferences}>
                Save Preferences
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="chat-content">
        {/* Character video panel */}
        <div className="character-panel">
          <video 
            ref={videoRef}
            key={currentVideo}
            autoPlay 
            loop 
            muted 
            className="character-video"
          >
            <source src={currentVideo} type="video/mp4" />
          </video>
          
          <div className="character-controls">
            <button className="character-control-btn" onClick={() => playSpecificVideo('welcome')}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z" />
              </svg>
            </button>
          </div>
          
          <div className="character-name">Milo</div>
        </div>
        
        {/* Chat interface */}
        <div className="chat-box">
          <div className="chat-header">
            <h2>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z" />
              </svg>
              Chat with Milo
            </h2>
            
            <div className="chat-actions">
              <button className="chat-action-btn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M15 4v7H5.17l-.59.59-.58.58V4h11m1-2H3c-.55 0-1 .45-1 1v14l4-4h10c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1zm5 4h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1z" />
                </svg>
              </button>
              <button className="chat-action-btn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4 0-2.05 1.53-3.76 3.56-3.97l1.07-.11.5-.95C8.08 7.14 9.94 6 12 6c2.62 0 4.88 1.86 5.39 4.43l.3 1.5 1.53.11c1.56.1 2.78 1.41 2.78 2.96 0 1.65-1.35 3-3 3z" />
                </svg>
              </button>
            </div>
          </div>
          
          <div className="chat-messages">
            {/* Date divider (optional) */}
            <div className="messages-date-divider">
              <span className="messages-date-text">Today</span>
            </div>
            
            {/* Conversation messages */}
            {messages.map((msg, index) => (
              <div key={index} className={`chat-bubble ${msg.sender} ${index === messages.length - 1 ? 'with-actions' : ''}`}>
                {msg.text}
                
                {index === messages.length - 1 && (
                  <div className="message-actions">
                    <button className="message-action-btn">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M16 22c1.1 0 2-.9 2-2l-.01-12c0-1.1-.89-2-1.99-2h-8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h8zM8 6h8v12H8V6z" />
                        <path d="M12.5 11.25H14v1.5h-1.5zM15 11.25h1.5v1.5H15zM10 11.25h1.5v1.5H10zM7.5 11.25H9v1.5H7.5zM16 8V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v4h8z" />
                      </svg>
                    </button>
                    <button className="message-action-btn">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z" />
                      </svg>
                    </button>
                  </div>
                )}
              </div>
            ))}
            
            {/* Typing indicator */}
            {isTyping && (
              <div className="chat-bubble bot typing">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            )}
            
            {/* Invisible element to scroll to */}
            <div ref={chatEndRef} />
          </div>

          {/* Chat input */}
          <div className="chat-input-container">
            <div className="chat-input">
              <div className="chat-input-actions">
                <button className="chat-input-action-btn">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z" />
                  </svg>
                </button>
              </div>
              
              <input
                type="text"
                placeholder="Type your message..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
              />
              
              <button className="chat-input-send" onClick={sendMessage}>
                <svg viewBox="0 0 24 24">
                  <path d="M2 21L23 12L2 3V10L17 12L2 14V21Z"></path>
                </svg>
              </button>
            </div>
          </div>
          
          {/* Next button */}
          {showNextButton && (
            <button className="next-button" onClick={handleNext}>
              <span>Continue</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Action buttons */}
      <div className="button-container">
        <button className="absolute-button" onClick={() => playSpecificVideo('random')}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M10.59 9.17L5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41l-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z" />
          </svg>
          Random
        </button>
        <button className="absolute-button" onClick={() => playSpecificVideo('welcome')}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" />
          </svg>
          Welcome
        </button>
        <button className="absolute-button" onClick={() => playSpecificVideo('happy')}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z" />
          </svg>
          Happy
        </button>
        <button className="absolute-button" onClick={() => playSpecificVideo('waiting')}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M15 1H9v2h6V1zm-4 13h2V8h-2v6zm8.03-6.61l1.42-1.42c-.43-.51-.9-.99-1.41-1.41l-1.42 1.42C16.07 4.74 14.12 4 12 4c-4.97 0-9 4.03-9 9s4.02 9 9 9 9-4.03 9-9c0-2.12-.74-4.07-1.97-5.61zM12 20c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z" />
          </svg>
          Wait
        </button>
        <button className="absolute-button" onClick={() => playSpecificVideo('nodding')}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" />
          </svg>
          Nod
        </button>
      </div>
    </div>
  );
}

export default ChatPage;
