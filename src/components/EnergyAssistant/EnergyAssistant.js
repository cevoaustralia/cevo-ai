<<<<<<< HEAD
import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Paper,
  Chip,
  IconButton,
  CircularProgress,
} from '@mui/material';
import {
  Send,
  AttachFile,
  Close,
} from '@mui/icons-material';

function EnergyAssistant() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [context, setContext] = useState({});

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:2024/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: input,
          session_id: sessionId,
          conversation_history: messages,
          has_file: selectedFile !== null,
          file_name: selectedFile?.name || null
        })
      });

      const data = await response.json();
      
      // Update session and context
      if (data.session_id) setSessionId(data.session_id);
      if (data.context) setContext(data.context);
      
      const botMessage = {
        type: 'bot',
        content: data.response,
        agent: data.agent_used,
        reasoning: data.reasoning
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      setMessages(prev => [...prev, {
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        agent: 'ERROR'
      }]);
    }

    setInput('');
    setSelectedFile(null);
    setLoading(false);
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Paper sx={{ p: 3, mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          Energy Assistant
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Ask me about your energy account, bills, or new connections
        </Typography>
        {context.customer_number && (
          <Chip
            label={`Customer: ${context.customer_number} | Agent: ${context.current_agent}`}
            color="primary"
            variant="outlined"
            sx={{ mt: 2 }}
          />
        )}
      </Paper>

      <Card sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <CardContent sx={{ flexGrow: 1, overflow: 'auto', maxHeight: '60vh' }}>
          {messages.map((msg, idx) => (
            <Box
              key={idx}
              sx={{
                mb: 2,
                display: 'flex',
                justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start',
              }}
            >
              <Paper
                sx={{
                  p: 2,
                  maxWidth: '70%',
                  bgcolor: msg.type === 'user' ? 'primary.main' : 'grey.100',
                  color: msg.type === 'user' ? 'primary.contrastText' : 'text.primary',
                }}
              >
                <Typography variant="body1">{msg.content}</Typography>
                {msg.agent && (
                  <Typography variant="caption" sx={{ mt: 1, display: 'block', opacity: 0.7 }}>
                    Agent: {msg.agent} | {msg.reasoning}
                  </Typography>
                )}
              </Paper>
            </Box>
          ))}
          {loading && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <CircularProgress size={20} />
              <Typography variant="body2" color="text.secondary">
                Thinking...
              </Typography>
            </Box>
          )}
        </CardContent>

        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          {selectedFile && (
            <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
              <AttachFile fontSize="small" />
              <Typography variant="body2">{selectedFile.name}</Typography>
              <IconButton size="small" onClick={() => setSelectedFile(null)}>
                <Close fontSize="small" />
              </IconButton>
            </Box>
          )}
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              variant="outlined"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Hi! I can help with bills, account info, or new connections. What can I help you with?"
              disabled={loading}
            />
            <input
              type="file"
              id="file-upload"
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={(e) => setSelectedFile(e.target.files[0])}
              style={{ display: 'none' }}
            />
            <IconButton
              onClick={() => document.getElementById('file-upload').click()}
              disabled={loading}
            >
              <AttachFile />
            </IconButton>
            <Button
              variant="contained"
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              endIcon={<Send />}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Card>
    </Box>
=======
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
>>>>>>> 95ddde555ae5454b57a3805ddf9237cc51dea0a1
  );
}

export default EnergyAssistant;