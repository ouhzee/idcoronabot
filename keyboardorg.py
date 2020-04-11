from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler)

import logging

FIRST, SECOND = range(2)

counter = 0

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


keyboard = [[InlineKeyboardButton('Decrement', callback_data=0)],
            [InlineKeyboardButton(f'[{counter}]', callback_data=1)],
            [InlineKeyboardButton('Increment', callback_data=2)]]


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def start(update, context):
    button_list = [
    InlineKeyboardButton("col1", callback_data=1),
    InlineKeyboardButton("col2", callback_data=1),
    InlineKeyboardButton("row 2", callback_data=2)]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.message.reply_text(text="A two-column menu", reply_markup=reply_markup)


def main():
    updater = Updater(
        '915594611:AAGmABjTbCPZBbwgwjhenyLcTqGCNFlQCFs', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()