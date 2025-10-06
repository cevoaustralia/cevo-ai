import React, { useState } from 'react';

function MortgageAssistant() {
  const [message, setMessage] = useState('');

  return (
    <div className="chat-container">
      <div className="chat-box">
        <div className="chat-messages">
          <div className="message">Hello! How can I help you with your mortgage questions?</div>
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
    </div>
  );
}

export default MortgageAssistant;