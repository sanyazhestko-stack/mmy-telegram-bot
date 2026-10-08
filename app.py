import nest_asyncio
nest_asyncio.apply()

import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Дальше идут все остальные твои импорты:
import os
import threading
from flask import Flask
from pyrogram import Client, filters
# ... и так далее
import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# --- ТОВАРЫ ---
roblox_items = ["50 robux", "100 robux", "250 robux"]
roblox_prices = [30, 50, 75]
# ... (остальные списки оставь как были) ...

# --- FLASK ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

@app.route('/health')
def health():
    return "OK"

# --- ФУНКЦИЯ ЗАПУСКА БОТА (запускается в отдельном потоке) ---
def run_telegram_bot():
    # Создаём и устанавливаем event loop для этого потока
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Создаём клиент внутри функции, чтобы он привязался к этому циклу
    bot_app = Client("my_bot", bot_token=BOT_TOKEN, api_id=1, api_hash="1")
    
    # Регистрируем хэндлеры
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
        # ... (логика обработки кнопок остаётся) ...
        await query.answer()

    # Запускаем бота
    bot_app.run()

# --- ЗАПУСК ---
if __name__ == "__main__":
    # Запускаем Telegram-бота в фоновом потоке
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем Flask в главном потоке (Render требует этого для порта)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
