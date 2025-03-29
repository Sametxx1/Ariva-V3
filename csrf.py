#!/usr/bin/env python3
import re
import requests
import json
from http.cookies import SimpleCookie

def get_instagram_csrf_token():
    """
    Function to retrieve the CSRF token from Instagram
    
    Returns:
        str or None: The CSRF token if found, None otherwise
    """
    session = requests.Session()
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    
    try:
        print("Attempting to get CSRF token from Instagram...")
        response = session.get('https://www.instagram.com/', headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return None
        
       
        for cookie in session.cookies:
            if cookie.name == 'csrftoken':
                print("Found CSRF token in cookies!")
                return cookie.value
        
        
        page_source = response.text
        
       
        csrf_match = re.search(r'"csrf_token":"([^"]+)"', page_source)
        if csrf_match:
            token = csrf_match.group(1)
            print("Found CSRF token in page source!")
            return token
        
       
        shared_data_match = re.search(r'window\._sharedData\s*=\s*({.*?});</script>', page_source, re.DOTALL)
        if shared_data_match:
            try:
                shared_data = json.loads(shared_data_match.group(1))
                if 'config' in shared_data and 'csrf_token' in shared_data['config']:
                    print("Found CSRF token in shared data!")
                    return shared_data['config']['csrf_token']
            except json.JSONDecodeError:
                pass
        
         
        try:
            api_response = session.get('https://www.instagram.com/data/shared_data/', headers=headers)
            if api_response.status_code == 200:
                data = api_response.json()
                if 'config' in data and 'csrf_token' in data['config']:
                    print("Found CSRF token in API response!")
                    return data['config']['csrf_token']
        except Exception as e:
            print(f"Error with API request: {e}")
        
        print("Could not find CSRF token in any source")
        return None
    
    except Exception as e:
        print(f"Error while getting CSRF token: {e}")
        return None

if __name__ == "__main__":
    token = get_instagram_csrf_token()
    if token:
        print(f"Instagram CSRF Token: {token}")
    else:
        print("Failed to retrieve CSRF token. Make sure you have internet connectivity.")
