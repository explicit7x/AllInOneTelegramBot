from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import *
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start command
@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    add_user(user_id)

    btn = [
        [InlineKeyboardButton("📥 Downloader", callback_data="downloader"),
         InlineKeyboardButton("🤖 AI Chat", callback_data="chat")],
        [InlineKeyboardButton("🧠 Study Zone", callback_data="study"),
         InlineKeyboardButton("🎭 Fun Zone", callback_data="fun")],
        [InlineKeyboardButton("💎 Upgrade to Premium", callback_data="premium")]
    ]

    message.reply_text("Welcome to All-In-One Bot!", reply_markup=InlineKeyboardMarkup(btn))

# Callback handler
@app.on_callback_query()
def callback_handler(client, callback):
    user_id = callback.from_user.id
    data = callback.data

    if data == "premium":
        text = ("**Upgrade Plans:**\n\n"
                "💎 Weekly - ₹99\n"
                "📅 Monthly - ₹399\n"
                "🌟 Yearly - ₹3999\n\n"
                "**UPI ID:** `oson4825@oksbi`\n"
                "Send payment screenshot to admin.")
        callback.message.edit(text, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Send Screenshot", url="https://t.me/explicit7x")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back")]
        ]))

    elif data == "chat":
        if is_premium(user_id):
            callback.message.edit("🤖 AI Chat is active.\n\n*Reply to this message with your question.*",
                                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))
        else:
            callback.message.edit("❌ AI Chat is only for premium users.",
                                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))

    elif data == "downloader":
        callback.message.edit("📥 Send your download link here.",
                              reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))

    elif data == "study":
        callback.message.edit("🧠 Study Zone:\n- Notes\n- PDFs\n- Practice Sets (Coming soon)",
                              reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))

    elif data == "fun":
        callback.message.edit("🎭 Fun Zone:\n- Memes\n- Jokes\n- Games (Coming soon)",
                              reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))

    elif data == "back":
        start(client, callback.message)

# AI dummy response (optional)
@app.on_message(filters.text & ~filters.command("start"))
def handle_text(client, message):
    user_id = message.from_user.id
    if is_premium(user_id):
        message.reply_text("🤖 *AI Response:* You asked: " + message.text)
    else:
        message.reply_text("⚠️ Only premium users can use AI chat.\nUpgrade to premium to continue.")

app.run()
