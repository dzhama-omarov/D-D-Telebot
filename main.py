from telebot import TeleBot, StateMemoryStorage
from config import BOT_TOKEN
from database.models import initialize_db
from bot.handlers import register_handlers
from bot.callbacks import register_callbacks


initialize_db()

storage = StateMemoryStorage()

bot = TeleBot(token=BOT_TOKEN, state_storage=storage)

register_callbacks(bot)
register_handlers(bot)


if __name__ == "__main__":
    print("\nBot started...")
    bot.infinity_polling()
