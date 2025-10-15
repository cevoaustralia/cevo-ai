import React, { useState, useRef } from 'react';

function InternalAssistant() {
  const [threadId, setThreadId] = useState(() => `thread_${Date.now()}`);
  const [messages, setMessages] = useState([{
    id: 0,
    type: 'assistant',
    content: 'Hello! How can I help you with your internal needs?'
  }]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const fileInputRef = useRef(null);
  
  const startNewChat = () => {
    setThreadId(`thread_${Date.now()}`);
    setMessages([{
      id: 0,
      type: 'assistant',
      content: 'Hello! How can I help you with your internal needs?'
    }]);
    setSelectedFiles([]);
  };

  const sendMessage = async (content, files = []) => {
    setIsLoading(true);
    
    const userMessage = { 
      id: Date.now(), 
      type: 'human', 
      content,
      files: files.map(f => f.name)
    };
    setMessages(prev => [...prev, userMessage]);
    
    try {
      const formData = new FormData();
      formData.append('message', content);
      
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
      setSelectedFiles([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="internal-assistant-container">
      <div className="chat-box">
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={message.id || index} className={`message ${message.type}`}>
              <strong>{message.type}:</strong> 
              <div>{message.content}</div>
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
          <div className="file-selection">
            <input 
              ref={fileInputRef}
              type="file" 
              multiple
              onChange={(e) => setSelectedFiles(Array.from(e.target.files))}
              accept=".pdf,.docx,.csv,.txt,.html,.md,.jpg,.jpeg,.png,.gif,.webp"
              style={{ marginBottom: '10px' }}
            />
            {selectedFiles.length > 0 && (
              <div className="selected-files">
                Selected: {selectedFiles.map(f => f.name).join(', ')}
              </div>
            )}
          </div>
          
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const form = e.target;
              const message = new FormData(form).get("message");
              if (message.trim()) {
                form.reset();
                sendMessage(message, selectedFiles);
              }
            }}
          >
            <input 
              type="text" 
              name="message"
              placeholder="Type your message..."
              required
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
    </div>
  );
}

export default InternalAssistant;