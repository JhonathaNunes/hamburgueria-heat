from config import Config
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
from app import init_app

app = init_app()


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Oooopa")


def echo_reverse(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text[::-1])


def main() -> None:
    updater = Updater(Config.TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        echo_reverse
    ))

    updater.start_polling()
    updater.idle()
