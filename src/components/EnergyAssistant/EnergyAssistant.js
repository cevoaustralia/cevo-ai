import React, { useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import './EnergyAssistant.css';

function EnergyAssistant() {
  const [threadId, setThreadId] = useState(() => `thread_${Date.now()}`);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const fileInputRef = useRef(null);
  
  const startNewChat = async () => {
    // Clear files from upload server
    try {
      await fetch(`http://localhost:5000/files/${threadId}`, {
        method: 'DELETE'
      });
    } catch (error) {
      console.error('Error clearing files from server:', error);
    }
    
    setThreadId(`thread_${Date.now()}`);
    setMessages([]);
    setSelectedFiles([]);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
      fileInputRef.current.files = null;
    }
  };

  const sendMessage = async (content, files = []) => {
    setIsLoading(true);
    
    // Add user message immediately
    const userMessage = { 
      id: Date.now(), 
      type: 'human', 
      content,
      files: files.map(f => f.name)
    };
    setMessages(prev => [...prev, userMessage]);
    
    // Clear files immediately after adding user message
    setSelectedFiles([]);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    
    try {
      const formData = new FormData();
      formData.append('message', content);
      
      // Add files to form data
      files.forEach(file => {
        formData.append('files', file);
      });
      
      const response = await fetch(`http://localhost:2024/threads/${threadId}/runs/stream`, {
        method: 'POST',
        body: formData
      });
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let assistantMessage = { id: Date.now() + 1, type: 'assistant', content: '' };
      
      // Add empty assistant message to start streaming
      setMessages(prev => [...prev, assistantMessage]);
      
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
                // Update the assistant message content
                setMessages(prev => 
                  prev.map(msg => 
                    msg.id === assistantMessage.id 
                      ? { ...msg, content: data.content }
                      : msg
                  )
                );
              }
            } catch (e) {
              console.error('Parse error:', e, 'Line:', dataStr);
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        id: Date.now() + 2, 
        type: 'error', 
        content: `Error: ${error.message}` 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="energy-container">
      <div className="chat-box">
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={message.id || index} className={`message ${message.type}`}>
              <strong>{message.type}:</strong> 
              {message.type === 'assistant' ? (
                <ReactMarkdown>{message.content}</ReactMarkdown>
              ) : (
                <div>{message.content}</div>
              )}
              {message.files && message.files.length > 0 && (
                <div className="attached-files">
                  📎 {message.files.join(', ')}
                </div>
              )}
            </div>
          ))}
          {isLoading && <div className="loading">Assistant is typing...</div>}
        </div>
        
        <div className="chat-input">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const form = e.target;
              const message = new FormData(form).get("message");
              if (message.trim() || selectedFiles.length > 0) {
                form.reset();
                sendMessage(message || '', selectedFiles);
              }
            }}
          >
            <div className="input-container">
              <input 
                ref={fileInputRef}
                type="file" 
                multiple
                onChange={(e) => setSelectedFiles(prev => [...prev, ...Array.from(e.target.files)])}
                accept=".pdf,.docx,.csv,.txt,.html,.md,.jpg,.jpeg,.png,.gif,.webp"
                style={{ display: 'none' }}
                id="file-input"
              />
              <label htmlFor="file-input" className="file-icon" title="Attach files">
                📎
              </label>
              <input 
                type="text" 
                name="message"
                placeholder="Type your message..."
                style={{ flex: 1 }}
              />
              <button type="submit" disabled={isLoading}>
                {isLoading ? 'Sending...' : 'Send'}
              </button>
              <button type="button" onClick={startNewChat}>
                New Chat
              </button>
            </div>
          </form>
        </div>
        
        {selectedFiles.length > 0 && (
          <div className="selected-files-preview">
            {selectedFiles.map((file, index) => (
              <div key={index} className="file-item">
                📎 {file.name}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
>>>>>>> 95ddde555ae5454b57a3805ddf9237cc51dea0a1
  );
}

export default EnergyAssistant;