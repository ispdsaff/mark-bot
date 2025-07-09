import os
import logging
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from db import init_db
from handlers import start, menu, generation, review, fallback

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_SERVICE_NAME = os.getenv("RENDER_SERVICE_NAME")
PORT = int(os.getenv("PORT", 8000))
WEBHOOK_URL = f"https://{RENDER_SERVICE_NAME}.onrender.com/{BOT_TOKEN}"

def main():
    # 📦 Инициализация базы данных
    init_db()

    # ⚙️ Создание Telegram-приложения
    application = Application.builder().token(BOT_TOKEN).build()

# === Хендлеры команд ===
application.add_handler(CommandHandler("start", start.start_handler))

# === Callback-хендлеры ===
application.add_handler(CallbackQueryHandler(start.callback_handler, pattern="^start_interaction$|^market_"))
application.add_handler(CallbackQueryHandler(menu.menu_handler, pattern="^menu_"))
application.add_handler(CallbackQueryHandler(generation.generation_handler, pattern="^gen_"))
application.add_handler(CallbackQueryHandler(review.review_handler, pattern="^review_"))

# === Обработка текстового ввода ===
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generation.text_input_handler))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, review.text_input_handler))

# === Фолбэк (всё остальное) ===
application.add_handler(MessageHandler(filters.ALL, fallback.fallback_handler))

    # 🌐 Вебхук запуск
    application.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=f"https://{RENDER_SERVICE_NAME}.onrender.com/{BOT_TOKEN}"
)


if __name__ == "__main__":
    main()