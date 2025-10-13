import requests
import json

def test_agent():
    url = "http://localhost:2024/invoke"
    
    payload = {
        "messages": [
            {"type": "human", "content": "Hello, how are you?"}
        ]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("Success!")
        print("Response:", json.dumps(result, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.reason)

if __name__ == "__main__":
    test_agent()