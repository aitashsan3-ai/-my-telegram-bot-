# -*- coding: utf-8 -*-
import os
import telebot
from telebot import types
import datetime
import random

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
if not TOKEN:
    raise RuntimeError("BOT_TOKEN مفقود (أضِفه في Railway > Variables)")
if not ADMIN_ID:
    raise RuntimeError("ADMIN_ID مفقود (أضِفه في Railway > Variables)")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
start_time = datetime.datetime.utcnow()

@bot.message_handler(commands=['start','help'])
def start_cmd(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "اهلا مدير ✅\nاكتب: تعليمات")
    else:
        bot.reply_to(message, "البوت شغّال ✅")

@bot.message_handler(func=lambda m: m.text and 'تعليمات' in m.text)
def guide(message):
    txt = ("الأوامر:\n"
           "- معلوماتي\n"
           "- رتبتي\n"
           "- للتقييد: (بالرد) اكتب: تقيد\n"
           "- لفك التقييد: (بالرد) اكتب: فك")
    bot.reply_to(message, f"<strong>{txt}</strong>")

@bot.message_handler(func=lambda m: m.text and 'معلوماتي' in m.text)
def myinfo(message):
    u = message.from_user
    try:
        bio = bot.get_chat(u.id).bio or "-"
    except:
        bio = "-"
    txt = (f"اسم: {u.first_name}\n"
           f"يوزر: @{u.username if u.username else '-'}\n"
           f"ايدي: {u.id}\n"
           f"وقت التشغيل (UTC): {start_time}\n"
           f"بايو: {bio}")
    bot.reply_to(message, f"<strong>{txt}</strong>")

@bot.message_handler(func=lambda m: m.text and 'رتبتي' in m.text)
def rank(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "<strong>المدير العسل ✨</strong>")
    else:
        bot.reply_to(message, "<strong>المحترم ✨</strong>")

@bot.message_handler(func=lambda m: m.text and (m.text.startswith('تقيد') or m.text.startswith('فك')))
def restrict_unrestrict(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "<strong>انت لست المدير</strong>")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "<strong>ارسل الأمر بالرد على رسالة الشخص</strong>")
        return
    target = message.reply_to_message.from_user.id
    try:
        if message.text.startswith('تقيد'):
            perms = types.ChatPermissions(can_send_messages=False)
            bot.restrict_chat_member(message.chat.id, target, permissions=perms)
            bot.reply_to(message, f"<strong>تم تقييد {target}</strong>")
        else:
            perms = types.ChatPermissions(
                can_send_messages=True,
                can_send_audios=True, can_send_documents=True, can_send_photos=True,
                can_send_videos=True, can_send_video_notes=True, can_send_voice_notes=True,
                can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True
            )
            bot.restrict_chat_member(message.chat.id, target, permissions=perms)
            bot.reply_to(message, f"<strong>تم فك القيود عن {target}</strong>")
    except Exception as e:
        bot.reply_to(message, f"<strong>خطأ: {e}</strong>")

if __name__ == "__main__":
    print("✅ Bot is starting on Railway ...")
    bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)