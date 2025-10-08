import React from 'react';
import { useStream } from '@langchain/langgraph-sdk/react';
import FileUpload from '../FileUpload';

function EnergyAssistant() {
  const thread = useStream({
    apiUrl: "http://localhost:2024",
    assistantId: "agent",
    messagesKey: "messages",
  });

  return (
    <div className="energy-container">
      <div className="chat-box">
        <div className="chat-messages">
          {thread.messages.map((message) => (
            <div key={message.id} className="message">
              {message.content}
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
              thread.submit({ messages: [{ type: "human", content: message }] });
            }}
          >
            <input 
              type="text" 
              name="message"
              placeholder="Type your message..."
            />
            {thread.isLoading ? (
              <button type="button" onClick={() => thread.stop()}>
                Stop
              </button>
            ) : (
              <button type="submit">Send</button>
            )}
          </form>
        </div>
      </div>
      
      <FileUpload />
    </div>
  );
}

export default EnergyAssistant;