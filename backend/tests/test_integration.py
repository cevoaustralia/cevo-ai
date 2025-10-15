import unittest
import requests
import psycopg2
import os
import time

class TestIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.api_url = "http://localhost:2024"
        cls.db_params = {
            'host': 'localhost',
            'database': 'energy_db',
            'user': 'postgres',
            'password': 'password',
            'port': '5432'
        }
        cls.wait_for_services()
    
    @classmethod
    def wait_for_services(cls):
        # Wait for API
        for _ in range(30):
            try:
                response = requests.get(f"{cls.api_url}/health")
                if response.status_code == 200:
                    break
            except:
                time.sleep(1)
        
        # Wait for DB
        for _ in range(30):
            try:
                conn = psycopg2.connect(**cls.db_params)
                conn.close()
                break
            except:
                time.sleep(1)
    
    def test_database_connection(self):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        self.assertEqual(result[0], 1)
        conn.close()
    
    def test_end_to_end_customer_query(self):
        # Insert test data
        try:
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO entity (id, name, address) 
                VALUES (12345, 'Test Customer', '123 Test St')
                ON CONFLICT (id) DO NOTHING
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database setup error: {e}")
        
        # Test API with database data
        payload = {
            "query": "What's my account information?",
            "customer_number": "12345"
        }
        response = requests.post(f"{self.api_url}/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["agent_used"], "CURRENT_CUSTOMER")
    
    def test_address_validation_integration(self):
        payload = {
            "query": "Can I get energy at my address?",
            "address": "123 Collins St, Melbourne VIC"
        }
        response = requests.post(f"{self.api_url}/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("melbourne", data["response"].lower())

if __name__ == '__main__':
    unittest.main()