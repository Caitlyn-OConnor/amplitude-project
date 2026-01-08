import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time


url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': '20260101T00',
    'end': '20260108T00'
}

load_dotenv()

api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")

filename = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

response = requests.get(url, params=params, auth=(api_key, secret_key))


print(response.status_code)
print(response.text)


