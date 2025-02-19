import random
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
    url = f"https://zrp.okdesk.ru/api/v1/issues/list?api_token={token}&assignee_ids[]=22&status_codes[]=opened&status_codes[]=in_progress"
    
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
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

def check_issues_and_notify():
    count = get_issues_count(TICKET_SYSTEM_TOKEN)
    resp = get_duty()

    if resp and "json" in resp:  # Проверяем, что resp содержит ключ "json"
        mention = ", ".join(resp["json"])
    else:
        mention = "дежурный"

        # Список вариаций сообщений
    MESSAGE_VARIANTS = [
    "Коллеги! По Зелёнке у нас висит {count} не закрытых задач. Это не круто! {mention}, в бой https://zrp.okdesk.ru/",
    "Внимание! У нас {count} нерешённых задач в Зелёнке. {mention}, давайте разберёмся: https://zrp.okdesk.ru/",
    "Эй, команда! В Зелёнке накопилось {count} задач. {mention}, пора действовать: https://zrp.okdesk.ru/",
    "Ого! {count} задач ждут своего часа в Зелёнке. {mention}, за работу: https://zrp.okdesk.ru/",
    "Коллеги, {count} задач в Зелёнке требуют внимания. {mention}, вперёд: https://zrp.okdesk.ru/",
    "Упс! В Зелёнке {count} задач ещё не закрыты. {mention}, давайте исправим: https://zrp.okdesk.ru/",
    "Эй-эй! {count} задач в Зелёнке ждут нас. {mention}, за дело: https://zrp.okdesk.ru/",
    "Коллеги, {count} задач в Зелёнке — это слишком! {mention}, в бой: https://zrp.okdesk.ru/",
    "Внимание! {count} задач в Зелёнке требуют решения. {mention}, пора взяться: https://zrp.okdesk.ru/",
    "Ого-го! {count} задач в Зелёнке. {mention}, давайте разберёмся: https://zrp.okdesk.ru/"
]
    
    if count is not None and count > 10:
        # Выбираем случайное сообщение из списка
        message = random.choice(MESSAGE_VARIANTS).format(count=count, mention=mention)
        bot.send_message(CHAT_ID, message)


# Планирование проверок
schedule.every().day.at(TIME1).do(check_issues_and_notify)
schedule.every().day.at(TIME2).do(check_issues_and_notify)

# Запуск планировщика
while True:
    schedule.run_pending()
    time.sleep(1)