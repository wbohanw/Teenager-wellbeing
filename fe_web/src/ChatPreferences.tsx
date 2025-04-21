import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface ChatPreferences {
  language: string;
  purpose: string;
  personalityTraits: string[];
  tone: string;
  titlePreference: string;
  properNouns: string[];
}

const ChatPreferences: React.FC = () => {
  const navigate = useNavigate();
  const [language, setLanguage] = useState<string>('');
  const [purpose, setPurpose] = useState<string>('');
  const [selectedTraits, setSelectedTraits] = useState<string[]>([]);
  const [selectedTone, setSelectedTone] = useState<string>('');
  const [selectedTitle, setSelectedTitle] = useState<string>('');
  const [selectedProperNouns, setSelectedProperNouns] = useState<string[]>([]);

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

  const handleTraitToggle = (trait: string) => {
    if (selectedTraits.includes(trait)) {
      setSelectedTraits(selectedTraits.filter(t => t !== trait));
    } else {
      setSelectedTraits([...selectedTraits, trait]);
    }
  };

  const handleProperNounToggle = (noun: string) => {
    if (selectedProperNouns.includes(noun)) {
      setSelectedProperNouns(selectedProperNouns.filter(n => n !== noun));
    } else {
      setSelectedProperNouns([...selectedProperNouns, noun]);
    }
  };

  const handleStartChat = () => {
    // Prepare preferences data
    const preferences: ChatPreferences = {
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
    <div className="max-w-5xl mx-auto p-5 md:p-10 bg-bg-primary rounded-xl shadow-md">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2 text-primary">Chat Preferences</h1>
        <p className="text-text-secondary text-lg">Customize how Milo will communicate with you</p>
      </div>

      <div className="bg-bg-secondary rounded-lg p-6 mb-8">
        <div className="flex items-center gap-3 mb-6">
          <label className="relative inline-block w-14 h-7">
            <input type="checkbox" className="opacity-0 w-0 h-0" checked readOnly />
            <span className="absolute cursor-pointer inset-0 bg-gray-300 rounded-full transition-all duration-300 before:content-[''] before:absolute before:h-5 before:w-5 before:left-1 before:bottom-1 before:bg-white before:rounded-full before:transition-all before:duration-300 checked:bg-primary checked:before:translate-x-7"></span>
          </label>
          <span>Verbal Style Cues</span>
        </div>

        <div className="flex flex-col gap-6">
          <div className="mb-5">
            <h3 className="font-semibold mb-3 text-text-primary">Language</h3>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Please enter"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="flex-1 p-2.5 border border-border rounded-md text-base focus:outline-none focus:ring-2 focus:ring-primary/30"
              />
              <button className="w-10 h-10 flex items-center justify-center bg-bg-primary border border-border rounded-md">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-5 h-5 fill-text-secondary">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
                </svg>
              </button>
            </div>
          </div>

          <div className="mb-5">
            <h3 className="font-semibold mb-3 text-text-primary">Conversation Purpose</h3>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Please enter"
                value={purpose}
                onChange={(e) => setPurpose(e.target.value)}
                className="flex-1 p-2.5 border border-border rounded-md text-base focus:outline-none focus:ring-2 focus:ring-primary/30"
              />
              <button className="w-10 h-10 flex items-center justify-center bg-bg-primary border border-border rounded-md">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-5 h-5 fill-text-secondary">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
                </svg>
              </button>
            </div>
          </div>

          <div className="mb-5">
            <h3 className="font-semibold mb-3 text-text-primary">Titles</h3>
            <div className="flex flex-wrap gap-3">
              {titles.map((title) => (
                <button
                  key={title}
                  className={`py-2 px-4 bg-bg-primary border border-border rounded-full text-sm transition-all duration-200 ${selectedTitle === title ? 'bg-primary-light border-primary text-primary' : ''}`}
                  onClick={() => setSelectedTitle(title)}
                >
                  {title}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-5">
            <h3 className="font-semibold mb-3 text-text-primary">Proper Nouns</h3>
            <div className="flex flex-wrap gap-3">
              {properNouns.map((noun) => (
                <button
                  key={noun}
                  className={`py-2 px-4 bg-bg-primary border border-border rounded-full text-sm transition-all duration-200 ${selectedProperNouns.includes(noun) ? 'bg-primary-light border-primary text-primary' : ''}`}
                  onClick={() => handleProperNounToggle(noun)}
                >
                  {noun}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-5">
            <h3 className="font-semibold mb-3 text-text-primary">Personality Traits</h3>
            <div className="flex gap-2 mb-4">
              <input
                type="text"
                placeholder="Please enter"
                className="flex-1 p-2.5 border border-border rounded-md text-base focus:outline-none focus:ring-2 focus:ring-primary/30"
              />
              <button className="w-10 h-10 flex items-center justify-center bg-bg-primary border border-border rounded-md">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-5 h-5 fill-text-secondary">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
                </svg>
              </button>
            </div>
            <div className="flex flex-wrap gap-2.5 mt-4">
              {personalityTraits.map((trait) => (
                <button 
                  key={trait} 
                  className={`py-2 px-4 bg-bg-primary border border-border rounded-full text-sm transition-all duration-200 ${selectedTraits.includes(trait) ? 'bg-primary-light border-primary text-primary' : ''}`}
                  onClick={() => handleTraitToggle(trait)}
                >
                  {trait}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-5">
            <h3 className="font-semibold mb-3 text-text-primary">Tone</h3>
            <div className="flex flex-wrap gap-3">
              {tones.map((tone) => (
                <button
                  key={tone}
                  className={`py-2 px-4 bg-bg-primary border border-border rounded-full text-sm transition-all duration-200 ${selectedTone === tone ? 'bg-primary-light border-primary text-primary' : ''}`}
                  onClick={() => setSelectedTone(tone)}
                >
                  {tone}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button 
          className="flex items-center gap-2 py-3 px-6 bg-primary text-white border-none rounded-lg text-lg font-semibold cursor-pointer transition-all duration-200 hover:bg-primary-dark hover:-translate-y-0.5 shadow-md"
          onClick={handleStartChat}
        >
          Start Chat
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-5 h-5 fill-current">
            <path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default ChatPreferences; 