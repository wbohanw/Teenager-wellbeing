import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css"; 

function LandingPage() {
  const navigate = useNavigate();
  const [darkMode, setDarkMode] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Check for user's preferred color scheme on component mount
  useEffect(() => {
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    setDarkMode(prefersDark);
    
    if (prefersDark) {
      document.body.classList.add('dark');
    }
  }, []);
  
  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark');
  };

  return (
    <div className={`landing-container ${darkMode ? 'dark' : ''}`}>
      <div className="landing-background"></div>
      <div className="landing-overlay"></div>
      
      {/* Header */}
      <header className="landing-header">
        <div className="landing-logo">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
            <path d="M13 7h-2v6h2V7zm0 8h-2v2h2v-2z"/>
          </svg>
          Milo
        </div>
        
        <nav className="landing-nav">
          <a href="#" className="nav-link">主页</a>
          <a href="#" className="nav-link">个人资料</a>
          <a href="#" className="nav-link">设置</a>
          <a href="#" className="nav-link">帮助</a>
          
          <button className="landing-theme-toggle" onClick={toggleDarkMode}>
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
        </nav>
        
        <div className="landing-mobile-menu">
          <button className="landing-mobile-toggle" onClick={() => setMobileMenuOpen(true)}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" />
            </svg>
          </button>
        </div>
      </header>
      
      {/* Main content */}
      <main className="landing-content">
        <div className="landing-main">
          <div className="landing-info">
            <h1 className="landing-title">
            认识 <span>Milo</span>, 您的心理健康伙伴
            </h1>
            
            <p className="landing-subtitle">
            Milo 是一款由人工智能驱动的对话助手，旨在通过友善的交流、引导与情感支持，帮助青少年提升心理健康
            </p>
            
            <div className="landing-features">
              <div className="landing-feature">
                <div className="feature-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h10c.55 0 1-.45 1-1z" />
                  </svg>
                </div>
                <div className="feature-text">
                  <h3 className="feature-title">友善的交流</h3>
                  <p className="feature-description">在一个安全、无评判的空间中，与 Milo 聊聊你的一天、感受或面临的挑战。</p>
                </div>
              </div>
              
              <div className="landing-feature">
                <div className="feature-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z" />
                  </svg>
                </div>
                <div className="feature-text">
                  <h3 className="feature-title">私密与安全</h3>
                  <p className="feature-description">您的对话内容将受到严格保护，采用先进的安全措施，确保个人信息的隐私性。</p>
                </div>
              </div>
              
              <div className="landing-feature">
                <div className="feature-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6h-6z" />
                  </svg>
                </div>
                <div className="feature-text">
                  <h3 className="feature-title">成长与支持</h3>
                  <p className="feature-description">获得个性化的指导、情感支持，以及培养健康应对策略的实用工具。</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="landing-chat-box">
            <div className="greeting">
              <span>你好, 我是 Milo</span>
            </div>
            
            <div className="milo-image-container">
              <img 
                src="placeholder.png" 
                alt="Milo Avatar" 
                className="milo-image" 
              />
            </div>
            
            <p className="greeting-text">
            我在这里陪你聊天、倾听，并在你面对日常挑战和情绪时给予支持。
            </p>

            <button className="chat-button" onClick={() => navigate("/chat")}>
              <span>我们聊聊吧</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z" />
              </svg>
            </button>
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-copyright">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 9h2V9h-2v6z" />
          </svg>
          <span>© 2023 Milo AI. All rights reserved.</span>
        </div>
        
        <div className="footer-links">
          <a href="#" className="footer-link">Privacy Policy</a>
          <a href="#" className="footer-link">Terms of Service</a>
          <a href="#" className="footer-link">Support</a>
          <a href="#" className="footer-link">Contact</a>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;
