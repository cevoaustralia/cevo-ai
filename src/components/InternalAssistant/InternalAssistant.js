import React, { useState } from 'react';
import FileUpload from '../FileUpload';

function InternalAssistant() {
  const [message, setMessage] = useState('');

  return (
    <div className="internal-assistant-container">
      <div className="chat-box">
        <div className="chat-messages">
          <div className="message">Hello! How can I help you with your internal needs?</div>
        </div>
        <div className="chat-input">
          <input 
            type="text" 
            value={message} 
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
          />
          <button>Send</button>
        </div>
      </div>
      
      <FileUpload />
    </div>
  );
}

export default InternalAssistant;