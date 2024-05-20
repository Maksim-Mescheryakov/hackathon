import requests
from script_token import get_token

url = 'https://ai.rt.ru/api/1.0/chatgpt/chat'

# Получаем токен из другого скрипта
token = get_token()

payload = {
    "uuid": "b54d90c5-da21-4a6e-a2f0-13b2b75ef7e8",
    "chat": {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "Ваш вопрос здесь"
            }
        ],
        "temperature": 1,
        "top_p": 1,
        "n": 1,
        "stop": "",
        "max_tokens": 100,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "idMessage": 1
    }
}

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    messages = response.json().get('chat')['messages']
    if messages:
        answer = messages[0]['content']
        print(f'Ответ: {answer}')
    else:
        print('Нет сообщений в ответе')
else:
    print(f'Ошибка: {response.text}')