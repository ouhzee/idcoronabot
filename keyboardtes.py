from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler)

import logging, connection

FIRST = range(1)

counter = 0

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

keyboard = [[InlineKeyboardButton('Decrement', callback_data='0')],
            [InlineKeyboardButton(f'[{counter}]', callback_data='1')],
            [InlineKeyboardButton('Increment', callback_data='2')]]


provinceList = {"Jakarta": 31, "Banten": 32}

conn = connection.create_connection('corona.db')
#cur = conn.cursor()

settingList = connection.read_turnedon_notif(conn)



def buttonQuery(update, context):
    buttonList = []
    markup = InlineKeyboardMarkup(buttonList)
    for key, value in provinceList.items():
        #for i in settingList:
            #if (update.message.chat.id == i[0]):
        #if (value==i[1] and i[2]==1):
        if (update.callback_query.message.chat.id, value, 1) in settingList:
            buttonList.append([InlineKeyboardButton(text=f"{key} [on]", callback_data=value)])
        else:
            buttonList.append([InlineKeyboardButton(text=key, callback_data=value)])
    return markup
    

def buttonCommand(update, context):
    buttonList = []
    markup = InlineKeyboardMarkup(buttonList)
    for key, value in provinceList.items():
        #for i in settingList:
            #if (update.message.chat.id == i[0]):
        #if (value==i[1] and i[2]==1):
        if (update.message.chat.id, value, 1) in settingList:
            buttonList.append([InlineKeyboardButton(text=f"{key} [on]", callback_data=value)])
        else:
            buttonList.append([InlineKeyboardButton(text=key, callback_data=value)])
    return markup


def start(update, context):
    update.message.reply_text(text='pilih province', reply_markup=buttonCommand(update, context))


def pressed(update, context):
    global settingList
    global conn
    
    connection.save_settings(conn, update.callback_query.message.chat.id, str(update.callback_query.message.chat.title), update.callback_query.message.chat.type, str(update.callback_query.message.chat.username), update.callback_query.data)
    settingList = connection.read_turnedon_notif(conn)
    update.callback_query.edit_message_reply_markup(reply_markup=buttonQuery(update, context))


def main():
    updater = Updater('915594611:AAGmABjTbCPZBbwgwjhenyLcTqGCNFlQCFs', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(pressed))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()