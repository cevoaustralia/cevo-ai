#!/usr/bin/env python3
import json
import sys
from typing import Dict, List

class AddressServer:
    def __init__(self):
        self.coverage_areas = {
            'NSW': ['sydney', 'newcastle', 'wollongong'],
            'VIC': ['melbourne', 'geelong', 'ballarat'],
            'QLD': ['brisbane', 'gold coast', 'cairns'],
            'WA': ['perth', 'fremantle'],
            'SA': ['adelaide', 'mount gambier']
        }
    
    def check_address(self, address: str) -> Dict:
        """Check if address is in service coverage area"""
        address_lower = address.lower()
        
        for state, cities in self.coverage_areas.items():
            for city in cities:
                if city in address_lower:
                    return {
                        'available': True,
                        'state': state,
                        'city': city.title(),
                        'message': f'Energy services available in {city.title()}, {state}'
                    }
        
        return {
            'available': False,
            'message': 'Energy services may not be available at this address. Please contact support for verification.'
        }
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle MCP server requests"""
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'check_address':
            address = params.get('address', '')
            return self.check_address(address)
        
        return {'error': 'Unknown method'}

def main():
    server = AddressServer()
    
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = server.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({'error': str(e)}))
            sys.stdout.flush()

if __name__ == '__main__':
    main()