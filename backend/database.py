import psycopg2
import os
from typing import Dict, Optional

class EnergyDatabase:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'energy_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'port': os.getenv('DB_PORT', '5432')
        }
    
    def get_connection(self):
        return psycopg2.connect(**self.connection_params)
    
    def get_customer_by_number(self, customer_number: str) -> Optional[Dict]:
        """Retrieve customer data by customer number"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT e.id, e.name, e.address, i.net_amount, i.due_date
                        FROM entity e
                        LEFT JOIN invoice i ON e.id = i.entity_id
                        WHERE e.id = %s
                        ORDER BY i.posted_date DESC
                        LIMIT 1
                    """, (customer_number,))
                    
                    result = cur.fetchone()
                    if result:
                        return {
                            'customer_id': result[0],
                            'name': result[1],
                            'address': result[2],
                            'current_bill': float(result[3]) if result[3] else 0,
                            'due_date': result[4].isoformat() if result[4] else None
                        }
        except Exception as e:
            print(f"Database error: {e}")
        return None
    
    def check_address_coverage(self, address: str) -> bool:
        """Check if address is in service area"""
        # Simplified check - in real implementation would have coverage database
        coverage_areas = ['sydney', 'melbourne', 'brisbane', 'perth', 'adelaide']
        return any(area in address.lower() for area in coverage_areas)