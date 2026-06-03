import React, { useState, useRef, useEffect } from 'react';
import { Send, Globe, Star, Heart } from 'lucide-react';
import LanguageSwitcher from './LanguageSwitcher';
import IntentBadge from './IntentBadge';

export default function ChatInterface({ language, setLanguage, onNewResponse }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentResponseInfo, setCurrentResponseInfo] = useState(null);
  
  // Active session ID
  const [sessionId] = useState(() => `session-${Math.random().toString(36).substring(2, 9)}`);
  
  const chatEndRef = useRef(null);

  // Suggestion chips
  const [chips, setChips] = useState(['Pool Timing', 'Restaurant Hours', 'Late Checkout']);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Contextual suggestion chips based on intent
  const updateChips = (intent) => {
    if (intent === 'amenity_question') {
      setChips(['Spa Treatments', 'Fitness Center', 'WiFi Details']);
    } else if (intent === 'booking_inquiry') {
      setChips(['Cancellation Policy', 'Early Check-in', 'Grand Suite Info']);
    } else {
      setChips(['Pool Timing', 'Restaurant Hours', 'Late Checkout']);
    }
  };

  const handleSend = async (textToSend) => {
    const queryText = textToSend || input;
    if (!queryText.trim() || loading) return;

    // Append user message
    const userMsg = { sender: 'user', text: queryText };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: queryText,
          language: language
        })
      });

      if (!response.ok) {
        throw new Error('API server error');
      }

      const data = await response.json();
      
      // Append bot response
      const botMsg = {
        sender: 'bot',
        text: data.response,
        intent: data.intent,
        confidence: data.confidence,
        sources: data.sources,
        retrieval_score: data.retrieval_score,
        conversation_id: data.conversation_id,
        feedbackSubmitted: false
      };
      
      setMessages((prev) => [...prev, botMsg]);
      setCurrentResponseInfo(data);
      updateChips(data.intent);
      
      // Notify parent to refresh sources
      if (onNewResponse) {
        onNewResponse(data.sources || []);
      }
    } catch (error) {
      console.error("Error sending chat:", error);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: "### Connection Error\n\nI encountered an issue connecting to the Aurelius servers. Please check if the backend is running.",
          intent: 'other',
          confidence: 1.0,
          sources: [],
          retrieval_score: 0.0,
          conversation_id: null
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (msgIndex, rating) => {
    const msg = messages[msgIndex];
    if (!msg.conversation_id) return;

    try {
      const response = await fetch('http://127.0.0.1:8000/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: msg.conversation_id,
          rating: rating,
          comment: `Feedback from UI for msg index ${msgIndex}`
        })
      });

      if (response.ok) {
        setMessages((prev) => {
          const updated = [...prev];
          updated[msgIndex] = { ...updated[msgIndex], feedbackSubmitted: true, rating: rating };
          return updated;
        });
      }
    } catch (e) {
      console.error("Failed to submit feedback:", e);
    }
  };

  // Helper to parse bot markdown responses (e.g. ### Pool Timing\n\nContent...)
  const renderBotText = (text) => {
    if (text.startsWith('###')) {
      const parts = text.split('\n\n');
      const title = parts[0].replace('###', '').trim();
      const body = parts.slice(1).join('\n\n');
      return (
        <div>
          <h3 className="font-display text-lg font-bold text-brand-primary mb-2">
            {title}
          </h3>
          <p className="font-body text-sm leading-relaxed text-brand-tertiary whitespace-pre-line">
            {body}
          </p>
        </div>
      );
    }
    return (
      <p className="font-body text-sm leading-relaxed text-brand-tertiary whitespace-pre-line">
        {text}
      </p>
    );
  };

  return (
    <div className="flex-1 bg-white flex flex-col justify-between h-screen relative">
      {/* Top Header */}
      <header className="h-[70px] px-8 border-b border-brand-secondary/15 flex items-center justify-between shrink-0 select-none bg-brand-bg/20">
        <h2 className="font-display text-xl font-semibold text-brand-primary tracking-wide">
          Aurelius Concierge
        </h2>

        {/* Right header controls */}
        <div className="flex items-center gap-6">
          <LanguageSwitcher language={language} setLanguage={setLanguage} />
          
          <div className="flex items-center gap-2">
            <button className="w-8 h-8 rounded-full border border-brand-secondary/20 flex items-center justify-center text-brand-primary hover:bg-brand-secondary/10 transition-colors">
              <Globe size={15} />
            </button>
            <div className="w-8 h-8 rounded-full bg-brand-primary flex items-center justify-center text-brand-secondary font-bold text-xs">
              S
            </div>
          </div>
        </div>
      </header>

      {/* Conversations Area */}
      <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">
        {/* Welcome Block if no messages */}
        {messages.length === 0 && (
          <div className="py-12 max-w-[600px]">
            <h1 className="font-display text-3xl font-semibold text-brand-primary leading-tight mb-4 text-glow">
              Welcome to Aurelius, Mr. Sterling.
            </h1>
            <p className="font-display text-xl text-brand-tertiary font-light">
              How may I assist your stay today?
            </p>
            
            <div className="mt-8 space-y-1 p-4 border border-brand-secondary/20 rounded-lg bg-[#FFFDF8]">
              <span className="font-body text-[9px] uppercase tracking-widest text-[#B8962D] font-bold block mb-1">
                Suggested questions:
              </span>
              <p className="font-body text-xs text-brand-tertiary">
                Ask about checkout policy, swimming pool hours, WiFi availability, room amenities, or try a multilingual test by typing in Hinglish or Hindi.
              </p>
            </div>
          </div>
        )}

        {/* Render Chat Bubbles */}
        {messages.map((msg, index) => (
          <div key={index} className="flex flex-col">
            {msg.sender === 'user' ? (
              /* User Bubble */
              <div className="self-end max-w-[70%]">
                <div className="px-5 py-3 rounded-2xl rounded-tr-sm bg-white border border-brand-secondary text-brand-primary font-body text-sm shadow-sm select-text">
                  {msg.text}
                </div>
              </div>
            ) : (
              /* Bot Response */
              <div className="self-start max-w-[85%] space-y-2 select-text">
                <div className="p-1">
                  {renderBotText(msg.text)}
                </div>

                {/* Intent Badge */}
                {msg.intent && (
                  <div className="pt-1">
                    <IntentBadge intent={msg.intent} confidence={msg.confidence} variant="details" />
                  </div>
                )}

                {/* Feedback Row */}
                <div className="flex items-center gap-2 pt-1 border-t border-gray-100 mt-2">
                  <span className="font-body text-[10px] text-brand-tertiary/60">Rate this response:</span>
                  <div className="flex items-center gap-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        disabled={msg.feedbackSubmitted}
                        onClick={() => handleFeedback(index, star)}
                        className={`transition-colors ${
                          msg.feedbackSubmitted && msg.rating >= star
                            ? 'text-brand-secondary'
                            : msg.feedbackSubmitted
                            ? 'text-gray-200'
                            : 'text-gray-300 hover:text-brand-secondary'
                        }`}
                      >
                        <Star size={12} fill={msg.feedbackSubmitted && msg.rating >= star ? '#D4AF37' : 'none'} />
                      </button>
                    ))}
                  </div>
                  {msg.feedbackSubmitted && (
                    <span className="font-body text-[9px] text-green-600 font-bold ml-1">Thank you!</span>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className="self-start flex flex-col space-y-2">
            <div className="flex items-center gap-1.5 px-4 py-3 bg-brand-bg/30 border border-brand-secondary/10 rounded-2xl rounded-tl-sm w-[70px] justify-center">
              <span className="w-2.5 h-2.5 rounded-full bg-brand-secondary dot-bounce"></span>
              <span className="w-2.5 h-2.5 rounded-full bg-brand-secondary dot-bounce"></span>
              <span className="w-2.5 h-2.5 rounded-full bg-brand-secondary dot-bounce"></span>
            </div>
            <div className="font-body text-[10px] text-brand-tertiary italic">
              Aurelius is typing...
            </div>
          </div>
        )}
        
        <div ref={chatEndRef} />
      </div>

      {/* Suggested chips & Input Area */}
      <div className="p-6 border-t border-brand-secondary/15 bg-white shrink-0 select-none">
        {/* Suggestion Chips */}
        <div className="flex flex-wrap items-center gap-2 mb-4">
          {chips.map((chip, idx) => (
            <button
              key={idx}
              disabled={loading}
              onClick={() => handleSend(chip)}
              className="px-4 py-1.5 rounded-full border border-brand-secondary/35 text-brand-primary bg-brand-bg/10 hover:bg-brand-secondary/10 transition-colors font-body text-xs font-medium cursor-pointer"
            >
              {chip}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-3 border border-brand-secondary/30 rounded-xl px-4 py-3 bg-brand-bg/5 hover:border-brand-secondary transition-all"
        >
          <input
            type="text"
            value={input}
            disabled={loading}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Speak with your concierge..."
            className="flex-1 bg-transparent border-none outline-none font-body text-sm text-brand-primary placeholder-brand-tertiary/65 font-medium"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className={`w-9 h-9 rounded-lg flex items-center justify-center transition-all ${
              input.trim() && !loading
                ? 'bg-brand-primary text-brand-secondary hover:shadow-md'
                : 'bg-brand-tertiary/10 text-brand-tertiary/40 cursor-not-allowed'
            }`}
          >
            <Send size={15} />
          </button>
        </form>
      </div>
    </div>
  );
}
