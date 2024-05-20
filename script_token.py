import requests
from dotenv import load_dotenv
import os

load_dotenv()

email_user = os.getenv("EMAIL_USER")
psww_user = os.getenv("PSWW_USER")

url = 'https://ai.rt.ru/api/1.0/auth/authentication'
payload = {
    "email": email_user,
    "password": psww_user
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    token = response.json().get('token')
    print(f'Token: {token}')
else:
    print(f'Error: {response.text}')

def get_token():
    return token