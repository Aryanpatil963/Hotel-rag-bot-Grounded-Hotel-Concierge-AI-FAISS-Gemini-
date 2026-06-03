import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import SourcePanel from './components/SourcePanel';
import AdminDashboard from './components/AdminDashboard';

export default function App() {
  const [activeScreen, setActiveScreen] = useState('chat'); // 'chat' or 'admin'
  const [language, setLanguage] = useState('en'); // 'en', 'hi', 'hinglish'
  const [sources, setSources] = useState([]); // List of retrieved sources

  const handleNewResponseSources = (newSources) => {
    setSources(newSources);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-brand-bg font-body antialiased">
      {/* Shared Sidebar */}
      <Sidebar activeScreen={activeScreen} setActiveScreen={setActiveScreen} />

      {/* Main Layout Area */}
      {activeScreen === 'chat' ? (
        <>
          {/* Middle Chat Interface */}
          <ChatInterface 
            language={language} 
            setLanguage={setLanguage} 
            onNewResponse={handleNewResponseSources} 
          />
          
          {/* Right Sources & Featured Amenity Panel */}
          <SourcePanel sources={sources} />
        </>
      ) : (
        /* Full width Admin Dashboard */
        <AdminDashboard />
      )}
    </div>
  );
}
