This is a react js application. The project uses best practices for organising files in a directory structure. There are three pages on the site. 
1) Internal_assistant
2) External assistant 
3) Data Insights

Internal_assistant page has two components:
- Energy component with a chatbox at the top and an upload box at the bottom
- Finance component with a chatbox at the top and an upload box at the bottom
The upload box is a reusable component.

## Backend
The backend is a Python FastAPI server that uses LangGraph and AWS Bedrock (Claude 4.5 Sonnet) for chat functionality.

