import telebot
from config import keys, TOKEN
from extentions import ConvertionExeption, CurrencyConverter


bot = telebot.TeleBot(TOKEN)  # создаем объект бот (экземпляр класса TeleBot) с токеном, полученным при регистрации


@bot.message_handler(commands=['start', 'help'])  # Вывод инструкции
def values(message: telebot.types.Message):
    text = 'Для запроса введите: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n \n \
Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  # обработчик запросов
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConvertionExeption('Введите 3 параметра!!!')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()