import telebot

# Указываем токен вашего бота
BOT_TOKEN = '7186072535:AAEY1bD8D-xpvvFZihsaDoTFI2ujKlxPems'

# Создаем объект бота
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, f'Ваш chat_id: {message.chat.id}')

bot.polling(none_stop=True, interval=0)