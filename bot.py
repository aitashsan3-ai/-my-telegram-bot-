# -*- coding: utf-8 -*-
import telebot
from telebot import types
import datetime
import random

# التوكن والآيدي جاهزين مباشرة
TOKEN = "7698149753:AAH2kkWKLYGtq8kTUY6ZH_OJgEng9uZ0xAk"
ADMIN_ID = 7316672086

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "اهلا يا ادمن ✅")
    else:
        bot.reply_to(message, "اهلا بك في البوت ✨")

@bot.message_handler(commands=['quote'])
def send_quote(message):
    quotes = [
        "🚀 النجاح يبدأ بخطوة",
        "🌸 ابتسم فالحياة جميلة",
        "💡 لا تستسلم ابداً"
    ]
    bot.send_message(message.chat.id, random.choice(quotes))

print("البوت شغال ...")
bot.infinity_polling()