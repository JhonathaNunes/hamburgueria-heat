import logging
import locale
from sqlalchemy import create_engine
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from config import Config
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# State definitions for top level conversation
SELECTING_ACTION, LOOKING_MENU, ACCESS_PLATFORM = map(chr, range(3))
# State definitions for descriptions conversation
SELECTING_FEATURE, TYPING = map(chr, range(3, 5))
# Meta states
STOPPING, SHOWING = map(chr, range(5, 7))

END = ConversationHandler.END

# General status
(
    START_OVER,
    SELF
) = map(chr, range(7, 9))


def start(update: Update, context: CallbackContext):
    welcome_text = (
        'Bem-vindo a Hamburgueria Heat, selecione uma das opções abaixo'
    )

    buttons = [
        [
            InlineKeyboardButton(
                text='Visualizar cardápio',
                callback_data=str(LOOKING_MENU)
            ),
            InlineKeyboardButton(
                text='Acessar plataforma',
                callback_data=str(ACCESS_PLATFORM)
            )
        ]
    ]

    keybord = InlineKeyboardMarkup(buttons)

    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=welcome_text,
            reply_markup=keybord
        )
    else:
        update.message.reply_text(
            text=welcome_text,
            reply_markup=keybord
        )

    context.user_data[START_OVER] = False
    return SELECTING_ACTION


def show_menu(update: Update, context: CallbackContext):
    menu = '*****MENU*****\n'

    with engine.connect() as con:
        products = con.execute('SELECT name, price, description FROM products')

        for p in products:
            (name, price, description) = p
            menu += (
                f'{name} ... R$ {locale.format("%.2f", price)}'
                f'\n{description}\n'
            )

    buttons = [[InlineKeyboardButton(text='Voltar', callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=menu, reply_markup=keyboard)

    context.user_data[START_OVER] = True
    return SHOWING


def show_platform(update: Update, context: CallbackContext) -> None:
    buttons = [[InlineKeyboardButton(text='Voltar', callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text='Acesse nossa plataforma em http://localhost:5000',
        reply_markup=keyboard
    )

    context.user_data[START_OVER] = True
    return SHOWING


def echo_reverse(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text[::-1])


def stop(update: Update, context: CallbackContext) -> int:
    '''End Conversation by command.'''
    update.message.reply_text('Até a próxima!')

    return END


def main() -> None:
    updater = Updater(Config.TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        echo_reverse
    ))

    selection_handlers = [
        CallbackQueryHandler(show_menu, pattern='^' + str(LOOKING_MENU) + '$'),
        CallbackQueryHandler(
            show_platform,
            pattern='^' + str(ACCESS_PLATFORM) + '$'
        )
    ]

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SHOWING: [CallbackQueryHandler(start, pattern='^' + str(END) + '$')],
            SELECTING_ACTION: selection_handlers
        },
        fallbacks=[CommandHandler('stop', stop)],
        map_to_parent={STOPPING: END}
    )

    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()
