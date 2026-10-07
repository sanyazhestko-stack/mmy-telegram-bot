import os
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# --- ТОВАРЫ ---
roblox_items = ["50 robux", "100 robux", "250 robux"]
roblox_prices = [30, 50, 75]

pubgm_items = ["30uc", "60uc", "90uc"]
pubgm_prices = [30, 60, 90]

mlbb_items = ["50 Diamonds", "100 Diamonds", "200 Diamonds"]
mlbb_prices = [30, 50, 150]

fortnite_items = ["300 v-bucks", "800 v-bucks", "1200 v-bucks"]
fortnite_prices = [250, 400, 550]

# --- FLASK ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

@app.route('/health')
def health():
    return "OK"

# --- TELEGRAM БОТ ---
bot_app = Client("my_bot", bot_token=BOT_TOKEN, api_id=1, api_hash="1")

def show_items(items, prices):
    text = ""
    for i in range(len(items)):
        text += f"{i+1}. {items[i]} — {prices[i]}₽\n"
    return text

@bot_app.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Roblox", callback_data="game_roblox")],
        [InlineKeyboardButton("PUBGM", callback_data="game_pubgm")],
        [InlineKeyboardButton("MLBB", callback_data="game_mlbb")],
        [InlineKeyboardButton("Fortnite", callback_data="game_fortnite")],
    ])
    await message.reply("Привет! Выбери игру:", reply_markup=keyboard)

@bot_app.on_callback_query()
async def callback(client, query):
    data = query.data
    if data == "game_roblox":
        await query.message.edit_text(show_items(roblox_items, roblox_prices))
    elif data == "game_pubgm":
        await query.message.edit_text(show_items(pubgm_items, pubgm_prices))
    elif data == "game_mlbb":
        await query.message.edit_text(show_items(mlbb_items, mlbb_prices))
    elif data == "game_fortnite":
        await query.message.edit_text(show_items(fortnite_items, fortnite_prices))
    await query.answer()

def run_bot():
    bot_app.run()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
