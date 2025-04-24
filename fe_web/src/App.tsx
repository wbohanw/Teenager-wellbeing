import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
// We'll update these imports after creating the TypeScript files
import LandingPage from "./LandingPage";
import ChatPage from "./ChatPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </Router>
  );
}

export default App;
