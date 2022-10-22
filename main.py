import json

import requests
import telebot

from config import TOKEN, exchanges
from extensions import *

bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Что бы начать работу введите мне команду с маленькой буквы в следующем формате: \n <название валюты> <в какую валюту перевести> <количество переводимой валюты> \n \n Запрос может выглядеть так: рубль доллар 100 \n \n  Для получения списка доступных валют введите команду /values "
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        base, sym, amount = values

    except ValueError as e:
        bot.reply_to(message, "Неверное количество параметров!")

    if len(values) != 3:
        raise APIException ("Неправильное количество параметров!")
    base, sym, amount = values
    r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={exchanges[base]}&tsyms={exchanges[sym]}")
    try:
        resp = Convertor.get_price(base, sym, amount)
        text = f" {resp}"
        bot.reply_to(message, text)
    except APIException as e:
        bot.reply_to(message, f'Ошибка в ккоманде: \n {e}')



bot.polling()


