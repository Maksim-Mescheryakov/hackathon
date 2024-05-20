import os
import requests
import psycopg2
import json
import urllib3
import warnings
from dotenv import load_dotenv
load_dotenv()

email_user = os.getenv("EMAIL_USER")
psww_user = os.getenv("PSWW_USER")
# Отключение предупреждений InsecureRequestWarning и NotOpenSSLWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")

# Подключаемся к БД
conn = psycopg2.connect(
    host="79.165.23.61",
    database="NLP",
    user="employee3826",
    password="3826"
)

# Создаем объект КУРСОР
cur = conn.cursor()

# Запрос в БД
cur.execute('SELECT * FROM "C3826".trecords WHERE id >= 1') # меняя id

# Выводим значения из столбца record_text
result = cur.fetchall()
for i, text_all in enumerate(result):
   record_text = text_all[3]
#    final_text = f"Номер записи - {i+1}\nТекст записи:\n{record_text}\n" 
print()

# Первый запрос для получения токена
auth_url = "https://ai.rt.ru/api/1.0/auth/authentication"
auth_headers = {
    "accept": "*/*",
    "Content-Type": "application/json"
}
auth_data = {
    "email": email_user,
    "password": psww_user
}

auth_response = requests.post(auth_url, headers=auth_headers, json=auth_data, verify=False)

# Формирование ПРОМТА для ИИ
promt_text_start = "Имеется в текстовом виде запись разговора между менеджером и клиентом:"    
promt_text_end = "Как ты считаешь, данный клиент к какой из 5 категорий относится?"
categoria_block = "Категории: Резко негативный, Слабо негативный, Нейтральный, Скорее склонен к покупке, Явно заинтересован. покажи только название категории без описания"
promt_for_AI = f"{promt_text_start}\n\n'{record_text}'\n\n{promt_text_end}\n{categoria_block}"

if auth_response.status_code == 200:
    token = auth_response.json().get('token')
    print("Token:", token)
    print()

    # Второй запрос 
chatgpt_url = "https://ai.rt.ru/api/1.0/chatgpt/chat"
chatgpt_headers = {
    "accept": "*/*",
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
chatgpt_data = {
    "uuid": "b54d90c5-da21-4a6e-a2f0-13b2b75ef7e8",
    "chat": {
        "frequency_penalty": None,
        "presence_penalty": None,
        "temperature": None,
        "max_tokens": None,
        "messages": [
            {
                "created": 1716118956113,
                "role": "user",
                "content": promt_for_AI
            }
        ],
        "top_p": None,
        "model": "gpt-3.5-turbo",
        "stop": None,
        "n": None
    }
}

# Вывод данных запроса третьего запроса

print(f"Текст запроса ИИ:\n{promt_for_AI}")

chatgpt_response = requests.post(chatgpt_url, headers=chatgpt_headers, json=chatgpt_data, verify=False)

# Вывод тела ответа в консоль
# print("\nChatGPT Response Body:", chatgpt_response.text)

if chatgpt_response.status_code == 200:
    chatgpt_json = chatgpt_response.json()
    category_from_ai = chatgpt_json[0]['message']['content']
        # Вставляем ответ в базу данных
    for record_id in range(1, 10):
        cur.execute('UPDATE "C3826".copy_trecords_qa SET record_type = %s WHERE id = %s', (category_from_ai, record_id))
        conn.commit()
    
    print("\nОтвет ИИ:", category_from_ai)
else:
    print(f"\nFailed to get response from ChatGPT. Status code: {chatgpt_response.status_code}, Response: {chatgpt_response.text}")
