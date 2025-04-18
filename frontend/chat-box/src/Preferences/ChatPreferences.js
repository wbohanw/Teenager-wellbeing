import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChatPreferences.css';

function ChatPreferences() {
  const navigate = useNavigate();
  const [language, setLanguage] = useState('');
  const [purpose, setPurpose] = useState('');
  const [selectedTraits, setSelectedTraits] = useState([]);
  const [selectedTone, setSelectedTone] = useState('');
  const [selectedTitle, setSelectedTitle] = useState('');
  const [selectedProperNouns, setSelectedProperNouns] = useState([]);

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

  const properNouns = ['him/his', 'her/she'];

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

  const handleStartChat = () => {
    // Prepare preferences data
    const preferences = {
      language,
      purpose,
      personalityTraits: selectedTraits,
      tone: selectedTone,
      titlePreference: selectedTitle,
      properNouns: selectedProperNouns
    };

    // Store preferences in localStorage
    localStorage.setItem('chatPreferences', JSON.stringify(preferences));

    // Navigate to chat page
    navigate('/chat', { state: { preferences } });
  };

  return (
    <div className="preferences-container">
      <div className="preferences-header">
        <h1>Chat Preferences</h1>
        <p>Customize how Milo will communicate with you</p>
      </div>

      <div className="preferences-section">
        <div className="toggle-section">
          <label className="toggle">
            <input type="checkbox" checked={true} readOnly />
            <span className="toggle-slider"></span>
          </label>
          <span>Verbal Style Cues</span>
        </div>

        <div className="preferences-content">
          <div className="preference-group">
            <h3>Language</h3>
            <div className="input-with-button">
              <input
                type="text"
                placeholder="Please enter"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              />
              <button className="search-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
                </svg>
              </button>
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
              <button className="search-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
                </svg>
              </button>
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
            <div className="input-with-button">
              <input
                type="text"
                placeholder="Please enter"
              />
              <button className="search-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
                </svg>
              </button>
            </div>
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
      </div>

      <div className="preferences-actions">
        <button className="start-chat-button" onClick={handleStartChat}>
          Start Chat
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z" />
          </svg>
        </button>
      </div>
    </div>
  );
}

export default ChatPreferences; 