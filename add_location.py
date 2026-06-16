import sys
import urllib.parse
import json
import secrets
import string
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python add_location.py 'https://ekosystem.wroc.pl/gospodarowanie-odpadami/harmonogram-wywozu-odpadow/?lokalizacja=XXXX&ulica=YYYY'")
        sys.exit(1)
        
    target_url = sys.argv[1]
    parsed_url = urllib.parse.urlparse(target_url)
    query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
    
    if 'lokalizacja' not in query_params or 'ulica' not in query_params:
        print("Error: The URL must contain both 'lokalizacja' and 'ulica' parameters.")
        sys.exit(1)
        
    real_address = {
        "streetId": int(query_params['ulica']),
        "houseId": int(query_params['lokalizacja'])
    }
    
    if not os.path.exists('locations.json'):
        locations = {}
    else:
        with open('locations.json', 'r') as f:
            locations = json.load(f)
        
    # Generate a random 8-character hex string for the key
    real_key = secrets.token_hex(4)
    while real_key in locations:
        real_key = secrets.token_hex(4)
        
    locations[real_key] = real_address
    
    with open('locations.json', 'w') as f:
        json.dump(locations, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully added location to locations.json!")
    print(f"This location is assigned to key: {real_key}")
    print(f"Calendar will be calendar_{real_key}.ics")

if __name__ == '__main__':
    main()
