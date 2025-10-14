import React, { useState, useMemo } from 'react';
import FileUpload from '../FileUpload';

function EnergyAssistant() {
  const [threadId, setThreadId] = useState(() => `thread_${Date.now()}`);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const startNewChat = () => {
    setThreadId(`thread_${Date.now()}`);
    setMessages([]);
  };

  const sendMessage = async (content) => {
    setIsLoading(true);
    
    // Add user message immediately
    const userMessage = { id: Date.now(), type: 'human', content };
    setMessages(prev => [...prev, userMessage]);
    
    try {
      const response = await fetch(`http://localhost:2024/threads/${threadId}/runs/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: [{ type: 'human', content }] })
      });
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6).trim();
            if (dataStr === '[DONE]') {
              return;
            }
            try {
              const data = JSON.parse(dataStr);
              if (data.type === 'assistant') {
                setMessages(prev => [...prev, data]);
              }
            } catch (e) {
              console.error('Parse error:', e, 'Line:', dataStr);
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="energy-container">
      <div className="chat-box">
        <div className="chat-messages">
          <div>Messages count: {messages.length}</div>
          {messages.map((message, index) => (
            <div key={message.id || index} className="message">
              <strong>{message.type}:</strong> {message.content?.content || message.content}
            </div>
          ))}
        </div>
        <div className="chat-input">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const form = e.target;
              const message = new FormData(form).get("message");
              form.reset();
              sendMessage(message);
            }}
          >
            <input 
              type="text" 
              name="message"
              placeholder="Type your message..."
            />
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Sending...' : 'Send'}
            </button>
            <button type="button" onClick={startNewChat} style={{marginLeft: '10px'}}>
              New Chat
            </button>
          </form>
        </div>
      </div>
      
      <FileUpload domain="energy" />
    </div>
  );
}

export default EnergyAssistant;