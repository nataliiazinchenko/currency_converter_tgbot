import telebot, dotenv, os
from dotenv import load_dotenv
from currency_converter import CurrencyConverter
from telebot import types


# first initializations of variables, objects etc
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    '''
    Function that allows bot to send a message with an amount request after /start command in bot
    '''
    bot.send_message(message.chat.id, 'Hello, enter amount to convert')
    bot.register_next_step_handler(message, amount)


def amount(message):
    '''
    Function that takes amount to convert, draws buttons and handles incorrect input values
    '''
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Incorrect amount: it should be numerical value. Try again.')
        bot.register_next_step_handler(message, amount)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_usd_eur = types.InlineKeyboardButton('USD / EUR', callback_data='usd/eur')
        btn_eur_usd = types.InlineKeyboardButton('EUR / USD', callback_data='eur/usd')
        btn_uah_eur = types.InlineKeyboardButton('UAH / EUR', callback_data='uah/eur')
        btn_uah_usd = types.InlineKeyboardButton('UAH / USD', callback_data='uah/usd')
        markup.add(btn_usd_eur, btn_eur_usd, btn_uah_eur, btn_uah_usd)
        bot.send_message(message.chat.id, 'Choose currency pair', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Incorrect amount: it should be more than 0. Try again.')
        bot.register_next_step_handler(message, amount)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    '''
    Function that works with callback data from buttons, described in amount(message) function
    and actually converts entered amount
    '''
    values = call.data.upper().split('/')
    res = currency.convert(amount, values[0], values[1])
    bot.send_message(call.message.chat.id, f'Today, entered {amount} {values[0]} makes {res:.2f} {values[1]}')
    bot.send_message(call.message.chat.id, 'If you want to convert another value, enter it here')
    bot.register_next_step_handler(call.message, amount)



bot.infinity_polling()