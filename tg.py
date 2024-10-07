import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

TOKEN = "7081235596:AAFbrUzpGecJwW42i3IPUeJZLDm9aPp85ng"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Добрый день. Как вас зовут?")


@bot.message_handler(content_types=['text'])
def handle_message(message):
    try:
        price = get_currency_rate()
        name = message.text.strip()
        bot.send_message(message.chat.id, text=f"Рад знакомству, {name}! Курс доллара к рублю сегодня {price}")

        if any(word.lower() in message.text.lower() for word in ['good bot', 'well done']):
            bot.send_message(message.chat.id, 'Спасибо!')

    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка. Попробуйте еще раз.')
        print(f'Ошибка: {e}')


def get_currency_rate():
    url = "https://www.google.com/search?q=курс+доллара+к+рублю"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find("div", class_="BNeawe iBp4i AP7Wnd").get_text()
    try:
        price = float(result.replace(',', '.').split()[0])
        return price
    except ValueError:
        return "Не удалось получить курс"


bot.polling(none_stop=True, interval=0)