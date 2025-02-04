import telebot
import requests
import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TICKET_SYSTEM_TOKEN = os.getenv('TICKET_SYSTEM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
URL_GET_HERO = os.getenv('URL_GET_HERO')
TIME1 = os.getenv('TIME1')
TIME2 = os.getenv('TIME2')

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_issues_count(token):
    url = f"https://zrp.okdesk.ru/api/v1/issues/list?api_token={token}&assignee_ids[]=22"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        issues = response.json()  
        return len(issues)  
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

def get_duty():
    
    try:
        response = requests.get(URL_GET_HERO)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

def check_issues_and_notify():
    count = get_issues_count(TICKET_SYSTEM_TOKEN)
    resp = get_duty()

    if resp:
        mention = ", ".join(resp)  # Преобразуем список в строку, разделяя элементы запятой
    else:
        mention = "дежурный"
    if count is not None and count > 10:
        bot.send_message(CHAT_ID, f"Коллеги! По Зелёнке у нас висит {count} не закрытых задач. Это не круто!! {mention}, в бой https://zrp.okdesk.ru/")

# Планирование проверок
schedule.every().day.at(TIME1).do(check_issues_and_notify)
schedule.every().day.at(TIME2).do(check_issues_and_notify)

# Запуск планировщика
while True:
    schedule.run_pending()
    time.sleep(1)