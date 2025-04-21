import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import miloImage from "./images/milo.png";
import backgroundImage from "./images/background.png";
import { TbSquareRoundedLetterM } from "react-icons/tb";

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);

  return (
    <div className="flex flex-col min-h-screen bg-bg-secondary text-text-primary transition-all duration-normal relative overflow-hidden">
      {/* Background */}
      <div 
        className="absolute top-0 left-0 w-full h-full z-0 bg-center bg-cover opacity-60 filter blur-0 transition-all duration-normal"
        style={{ backgroundImage: `url(${backgroundImage})` }}
      ></div>
      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-white/70 to-white/30 z-1 transition-all duration-normal"></div>
      
      {/* Header */}
      <nav className="flex items-center justify-between px-6 py-4 bg-white/80 backdrop-blur-sm shadow-sm border-b border-border relative z-10">
        <div className="text-xl font-bold text-primary flex items-center gap-3">
          <TbSquareRoundedLetterM className="w-8 h-8 fill-primary" />
          Milo AI
        </div>
        
        <div className="md:hidden block">
          <button 
            className="w-10 h-10 rounded-full flex items-center justify-center bg-transparent border-none cursor-pointer text-text-secondary"
            onClick={() => setMobileMenuOpen(true)}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-6 h-6">
              <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z" />
            </svg>
          </button>
        </div>
      </nav>
      
      {/* Main content */}
      <main className="flex-1 flex items-center justify-center relative z-2 py-10 px-5">
        <div className="flex max-w-7xl w-full gap-15 items-center justify-between lg:flex-row flex-col">
          <div className="flex-1 max-w-xl animate-[slideInLeft_1s_ease-out]">
            <h1 className="text-4xl md:text-5xl font-extrabold mb-6 leading-tight relative">
              认识 <span className="text-primary relative inline-block after:content-[''] after:absolute after:left-0 after:bottom-[10px] after:w-full after:h-2 after:bg-primary-light after:-z-1 after:rounded">Milo</span>, 您的心理健康伙伴
            </h1>
            
            <p className="text-lg mb-8 text-text-secondary leading-relaxed">
              Milo 是一款由人工智能驱动的对话助手，旨在通过友善的交流、引导与情感支持，帮助青少年提升心理健康
            </p>
            
            <div className="flex flex-col gap-4 mb-10">
              <div className="flex items-center gap-4 md:flex-row flex-col md:items-center items-start">
                <div className="w-12 h-12 rounded-xl bg-primary-light text-primary flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-6 h-6">
                    <path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h10c.55 0 1-.45 1-1z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold mb-1 text-text-primary">友善的交流</h3>
                  <p className="text-text-secondary text-sm">在一个安全、无评判的空间中，与 Milo 聊聊你的一天、感受或面临的挑战。</p>
                </div>
              </div>
              
              <div className="flex items-center gap-4 md:flex-row flex-col md:items-center items-start">
                <div className="w-12 h-12 rounded-xl bg-primary-light text-primary flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-6 h-6">
                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold mb-1 text-text-primary">私密与安全</h3>
                  <p className="text-text-secondary text-sm">您的对话内容将受到严格保护，采用先进的安全措施，确保个人信息的隐私性。</p>
                </div>
              </div>
              
              <div className="flex items-center gap-4 md:flex-row flex-col md:items-center items-start">
                <div className="w-12 h-12 rounded-xl bg-primary-light text-primary flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-6 h-6">
                    <path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6h-6z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold mb-1 text-text-primary">成长与支持</h3>
                  <p className="text-text-secondary text-sm">获得个性化的指导、情感支持，以及培养健康应对策略的实用工具。</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex-1 max-w-md bg-bg-primary p-10 flex flex-col justify-center items-center rounded-lg shadow-lg text-center border border-border relative z-2 animate-[slideInRight_1s_ease-out] transition-all duration-normal before:content-[''] before:absolute before:top-0 before:left-0 before:right-0 before:h-1 before:bg-gradient-to-r before:from-primary before:to-transparent before:rounded-t-lg">
            <div className="text-xl flex items-center justify-center gap-3 font-bold text-text-primary mb-8 relative after:content-[''] after:absolute after:bottom-[-16px] after:left-1/2 after:transform after:-translate-x-1/2 after:w-10 after:h-1 after:bg-primary after:rounded">
              <span>你好, 我是 Milo</span>
            </div>
            
            <div className="relative w-44 h-44 mx-auto my-10 rounded-full overflow-hidden shadow-lg">
              <img 
                src={miloImage} 
                alt="Milo Avatar" 
                className="w-full h-full object-cover rounded-full transition-all duration-500"
              />
              <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-primary/30 to-transparent"></div>
            </div>
            
            <p className="text-base leading-relaxed text-text-secondary mb-10 max-w-xs">
              我在这里陪你聊天、倾听，并在你面对日常挑战和情绪时给予支持。
            </p>

            <button 
              className="bg-gray-100/40 text-black  border-2 border-gray-600/40 py-4 px-8 text-base font-semibold rounded-3xl cursor-pointer transition-all duration-fast shadow-md hover:bg-primary-dark hover:translate-y-[-3px] hover:shadow-lg flex items-center gap-3 relative overflow-hidden before:content-[''] before:absolute before:inset-0 before:bg-gradient-to-r before:from-transparent before:via-white/20 before:to-transparent before:-translate-x-full hover:before:animate-shimmer"
              onClick={() => navigate("/chat")}
            >
              <span>开始聊天</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-5 h-5 transition-transform duration-fast group-hover:translate-x-1">
                <path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z" />
              </svg>
            </button>
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="py-8 px-6 flex justify-between items-center relative z-2 text-sm text-text-secondary border-t border-border backdrop-blur-sm bg-bg-primary/50 md:flex-row flex-col gap-5">
        <div className="flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-4 h-4">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 9h2V9h-2v6z" />
          </svg>
          <span>© 2025 Milo AI. All rights reserved.</span>
        </div>
        
        <div className="flex gap-6 md:flex-row flex-wrap justify-center">
          <a href="#" className="text-text-secondary no-underline hover:text-primary transition-colors duration-fast">Privacy Policy</a>
          <a href="#" className="text-text-secondary no-underline hover:text-primary transition-colors duration-fast">Terms of Service</a>
          <a href="#" className="text-text-secondary no-underline hover:text-primary transition-colors duration-fast">Support</a>
          <a href="#" className="text-text-secondary no-underline hover:text-primary transition-colors duration-fast">Contact</a>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;