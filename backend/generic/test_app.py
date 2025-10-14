import requests
import json

def test_thread_conversation():
    thread_id = "test_thread_123"
    base_url = "http://localhost:2024"
    
    # Test first message
    print("Testing first message...")
    payload1 = {
        "messages": [
            {"type": "human", "content": "Hello, my name is John"}
        ]
    }
    
    response1 = requests.post(f"{base_url}/threads/{thread_id}/runs", json=payload1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        print("First message sent successfully")
    
    # Test second message (should remember context)
    print("\nTesting second message with context...")
    payload2 = {
        "messages": [
            {"type": "human", "content": "What is my name?"}
        ]
    }
    
    response2 = requests.post(f"{base_url}/threads/{thread_id}/runs", json=payload2)
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        print("Second message sent successfully")
    
    # Get all messages in thread
    print("\nGetting thread messages...")
    messages_response = requests.get(f"{base_url}/threads/{thread_id}/messages")
    if messages_response.status_code == 200:
        messages = messages_response.json()
        print("Thread messages:", json.dumps(messages, indent=2))

if __name__ == "__main__":
    test_thread_conversation()