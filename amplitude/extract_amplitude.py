# Load environment variables
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import time
from pathlib import Path  

load_dotenv()

url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': '20260101T00',
    'end': '20260108T00'
}

api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")

# making the max api calls 3 in case of system errors
max_attempts = 3
attempt = 0

while attempt <= max_attempts:
    print(f"Attempt {attempt}...")
    response = requests.get(url, params=params, auth=(api_key, secret_key))

    if response.status_code == 200: #if api call successful
        try:
            # 1. Create directory if it doesn't exist
            Path("data").mkdir(exist_ok=True)
            
            # 2. Define filename with .zip extension using time of api call
            filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filepath = f'data/{filename}.zip'

            # 3. Write binary content ('wb') to the file
            with open(filepath, 'wb') as file:
                file.write(response.content)
            
            print(f'Zip file saved successfully: {filepath}')
            break  # Exit loop on success of zip saving

        except Exception as e:
            print(f"Error saving zip file: {e}")
            break # Exit loop on error saving 
            
    elif response.status_code >= 500:
        # Server error - wait 10s and retry
        print(f"Server error {response.status_code}. Retrying in 10s...")
        time.sleep(10)
        attempt += 1
    else:
        # Client error (401, 403, 404) - don't retry
        print(f"Client error {response.status_code}: {response.reason}")
        print(response.text)
        break

if attempt > max_attempts:
    print("Maximum attempts reached. Download failed.")


