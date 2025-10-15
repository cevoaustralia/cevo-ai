import unittest
import requests
import time
import subprocess
import os

class TestFunctionalAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:2024"
        cls.wait_for_service()
    
    @classmethod
    def wait_for_service(cls):
        for _ in range(30):
            try:
                response = requests.get(f"{cls.base_url}/health")
                if response.status_code == 200:
                    break
            except:
                time.sleep(1)
    
    def test_current_customer_flow(self):
        payload = {
            "query": "Why is my bill so high?",
            "customer_number": "12345"
        }
        response = requests.post(f"{self.base_url}/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["agent_used"], "CURRENT_CUSTOMER")
    
    def test_new_customer_flow(self):
        payload = {
            "query": "I want to switch providers",
            "address": "123 Collins St, Melbourne VIC"
        }
        response = requests.post(f"{self.base_url}/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["agent_used"], "NEW_CUSTOMER")
    
    def test_missing_customer_number(self):
        payload = {"query": "Why is my bill so high?"}
        response = requests.post(f"{self.base_url}/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("customer number", data["response"].lower())

if __name__ == '__main__':
    unittest.main()