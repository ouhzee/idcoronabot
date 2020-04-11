import os
import time
import logging
from uuid import uuid4
import requests
from functools import wraps
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatAction, ParseMode, Bot
import json, threading
import re, datetime, jsonparser, connection, re
from telegram.ext import Updater, CommandHandler, PicklePersistence, MessageHandler, Filters, CallbackQueryHandler, \
    CallbackContext
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
updater = Updater('1081827561:AAHdTmkPfJOP6HAeDuIZYwwUtVA4deVnMgw', use_context=True)
dispatcher = updater.dispatcher
apiUrl = "https://api.kawalcorona.com/"
indonesia = requests.get(apiUrl + "indonesia/")
#provinsi = indonesia + "provinsi"
conn = connection.create_connection('corona.db')
#cur = conn.cursor()
provinceList = {"Jakarta": 31, "Banten":36,
"Jawa Barat": 32,
"Jawa Tengah": 33, 
"Jawa Timur": 35, 
"DIY":34,
"Bali": 51,
"Kalimantan Barat":61,
"Kalimantan Tengah":62,
"Kalimantan Timur":64,
"Kalimantan Utara":65,
"Kalimantan Selatan": 63,
"Sulawesi Tenggara": 74,
"Sulawesi Utara":71,
"Sulawesi Tengah":72,
"Sulawesi Barat":76,
"Sulawesi Selatan":73,
"Sumatera Utara": 12,
"Sumatera Barat": 13,
"Sumatera Selatan":16,
"Kep. Riau":21,
"Riau":14,
"Aceh":11,
"Bengkulu":17,
"Belitung":19,
"Lampung":18,
"Jambi":15,
"NTB":52,
"Maluku":81,
"Maluku Utara":82,
"Papua":94,
"Papua Barat":91,
"Close Menu": "close"}
settingList = connection.read_turnedon_notif(conn)


def manualPage(file):
    '''
    pass the /path/file.txt
    '''
    with open(file, 'r') as banner:
        return banner.read()


def send_action(action):
    '''
    send action while processing func command
    '''
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)
        return command_func
    return decorator


@send_action(ChatAction.TYPING)
def add_group(update, context):
    if update.message.new_chat_members[0].id == context.bot.id:
        time.sleep(1.5)
        update.message.reply_text(text=f'Hi,\nthankyou for adding me to {update.message.chat.title}\nPlease read the manual by invoking help or click this /help for available feature')


def buildButton(buttons, n_col, header_button=None, footer_button=None):
    menu = [buttons[i:i + n_col] for i in range(0, len(buttons), n_col)]
    if header_button:
        menu.insert(0, header_button)
    if footer_button:
        menu.append(footer_button)
    return menu


def settingsQuery(update, context):
    '''
    update keyboard using callback_query
    '''
    buttonList = []
    for key, value in provinceList.items():
        #for i in settingList:
            #if (update.message.chat.id == i[0]):
        #if (value==i[1] and i[2]==1):
        if (update.callback_query.message.chat.id, value, 1) in settingList:
            buttonList.append(InlineKeyboardButton(text=f"{key} 🔘", callback_data=value))
        else:
            buttonList.append(InlineKeyboardButton(text=key, callback_data=value))
    markup = InlineKeyboardMarkup(buildButton(buttonList,n_col=2))
    return markup


#@send_action(ChatAction.TYPING)
def dataPressed(update, context):
    if (re.match(r'closedata',update.callback_query.data)):
        update.callback_query.edit_message_text('Menu closed')
    else:
        strfind = re.findall(r'\d+', update.callback_query.data)
        dataprovince = jsonparser.dataProvince(int(strfind[0]))
        provincecounter = jsonparser.parseCounter(int(strfind[0]))
        dataindo = jsonparser.dataIndonesia()
        with open('lastupdate.txt', 'r') as file:
            waktu = file.read()
        update.callback_query.edit_message_text(text='Fetching')
        time.sleep(0.5)
        update.callback_query.edit_message_text(text='Fetching.')
        time.sleep(0.5)
        update.callback_query.edit_message_text(text='Fetching..')
        time.sleep(0.5)
        update.callback_query.edit_message_text(text='Fetching...')
        time.sleep(0.5)
        update.callback_query.edit_message_text(text=f'\
        🇮🇩 <b>Indonesia</b> 🇮🇩\n\<code>
        Positif     : {dataindo[0]}         ({dataindo[3]})\n\
        Sembuh      : {dataindo[1]}         ({dataindo[4]})\n\
        Meninggal   : {dataindo[2]}         ({dataindo[5]})\n\n</code>\
        <b>Data Provinsi {dataprovince[0]}\n</b> \<code>
        Positif     : {dataprovince[1]}     ({provincecounter[0]})\n\
        Sembuh      : {dataprovince[2]}     ({provincecounter[1]})\n\
        Meninggal   : {dataprovince[3]}     ({provincecounter[2]})\n\n</code>\
        <i>Last {waktu}</i>', parse_mode=ParseMode.HTML)


def settingsButton(update, context):
    '''
    update keyboard using message.chat.id
    '''
    buttonList = []
    for key, value in provinceList.items():
        #for i in settingList:
            #if (update.message.chat.id == i[0]):
        #if (value==i[1] and i[2]==1):
        if (update.message.chat.id, value, 1) in settingList:
            buttonList.append(InlineKeyboardButton(text=f"{key} 🔘", callback_data=value))
        else:
            buttonList.append(InlineKeyboardButton(text=key, callback_data=value))
    markup = InlineKeyboardMarkup(buildButton(buttonList,n_col=2))
    return markup


@send_action(ChatAction.TYPING)
def dataCommand(update, context):
    buttonList = []
    for key, value in provinceList.items():
        buttonList.append(InlineKeyboardButton(text=f"{key}", callback_data=str(value)+'data'))
    markup = InlineKeyboardMarkup(buildButton(buttonList,n_col=2))
    print(datetime.now().strftime('%d-%M-%Y %H:%M ')+f"data invoked by {update.message.from_user.username} title {update.message.chat.title}")
    time.sleep(1.5)
    update.message.reply_text(text='Select which area \nyou want to get the data from', reply_markup=markup)


@send_action(ChatAction.TYPING)
def helpCommand(update, context):
    print(datetime.now().strftime('%d-%M-%Y %H:%M ')+f"help invoked by {update.message.from_user.username} title {update.message.chat.title}")
    time.sleep(1.5)
    update.message.reply_text(text=manualPage('manualpage.txt'),parse_mode=ParseMode.HTML)


#@send_action(ChatAction.TYPING)
def settingsPressed(update, context):
    global settingList
    global conn
    
    if update.callback_query.data == 'close':
        update.callback_query.edit_message_text('Settings Closed')
    else:
        connection.save_settings(conn, update.callback_query.message.chat.id, str(update.callback_query.message.chat.title), update.callback_query.message.chat.type, str(update.callback_query.message.chat.username), update.callback_query.data)
        settingList = connection.read_turnedon_notif(conn)
        markup = settingsQuery(update, context)
        update.callback_query.edit_message_reply_markup(reply_markup=markup)


@send_action(ChatAction.TYPING)
def settingsCommand(update, context):
    #buttonList = []
    markup = settingsButton(update, context)
    print(datetime.now().strftime('%d-%M-%Y %H:%M ')+f"settings invoked by {update.message.from_user.username} title {update.message.chat.title}")
    time.sleep(1.5)
    update.message.reply_text(text='You can set single or multiple area.\n<b><i>Note, selecting multiple area you\'ll get burst notification message</i></b>', reply_markup=markup, parse_mode=ParseMode.HTML)


@send_action(ChatAction.TYPING)
def startCommand(update, context):
    time.sleep(1)
    print(datetime.now().strftime('%d-%M-%Y %H:%M ')+f"start invoked by {update.message.from_user.username} title {update.message.chat.title}")
    update.message.reply_text(text="Henlo, you can get latest data in regard to covid-19 spread in Indonesia.\nTurn the notification on when there's new data updated from Menkes by invoking <code>/settings</code>.\n\nPlease read the manual by invoking help or click this /help.", parse_mode=ParseMode.HTML)


def cekUpdate():
    t = threading.Timer(1800, cekUpdate)
    t.daemon = True
    t.start()
    if jsonparser.cekChanges(conn):
        jsonparser.updateCounter(conn)
        for turnedon in jsonparser.TURNEDONNOTIF:
            chat = [chat[0] for chat in jsonparser.PREFERENCES if chat[1]==turnedon]
            prov_id = jsonparser.dataProvince(turnedon)
            counter = jsonparser.parseCounter(turnedon)
            with open('lastupdate.txt', 'r') as file:
                waktu = file.read()
            dataindo = jsonparser.dataIndonesia()
            for i in chat:
                try:
                    dispatcher.bot.send_message(chat_id=i, text=f'🦠COVID-19 UPDATE🦠\n\n\
                    <b><i>Indonesia</i></b>\n\
                    Positif     : {dataindo[0]}         ({dataindo[3]})\n\
                    Sembuh      : {dataindo[1]}         ({dataindo[4]})\n\
                    Meninggal   : {dataindo[2]}         ({dataindo[5]})\n\n\
                    <b>{prov_id[0]}</b>\n\<code>
                    Positif     : {prov_id[1]}           ({counter[0]})\n\
                    Sembuh      : {prov_id[2]}           ({counter[1]})\n\
                    Meninggal   : {prov_id[3]}           ({counter[2]})</code>\n\n\
                    <i>Last {waktu}</i>', parse_mode=ParseMode.HTML)
                except:
                    print(f"bot di kick dari {i}")
                #time.sleep(1.8)
    

"""def settingsMenu(update, context):
    button = [[InlineKeyboardButton("DKI Jakarta", callback_data=31),InlineKeyboardButton("Jawa Barat", callback_data=32)],
    [InlineKeyboardButton("Jawa Timur", callback_data=35),InlineKeyboardButton("Banten", callback_data=36)],
    [InlineKeyboardButton("Jawa Tengah", callback_data=33),InlineKeyboardButton("Sulawesi Selatan", callback_data=73)],
    [InlineKeyboardButton("Bali", callback_data=51),InlineKeyboardButton("Yogyakarta",callback_data=34)],
    [InlineKeyboardButton("Kalimantan Timur", callback_data=64),InlineKeyboardButton("Papua",callback_data=94)],
    [InlineKeyboardButton("Sumatera Utara", callback_data=12),InlineKeyboardButton("Sumatera Selatan", callback_data=16)],
    [InlineKeyboardButton("Kalimantan Selatan",callback_data=63),InlineKeyboardButton("Riau",callback_data=14)],
    [InlineKeyboardButton("Lampung", callback_data=18),InlineKeyboardButton("Kalimantan Tengah",callback_data=62)],
    [InlineKeyboardButton("Kalimantan Barat", callback_data=61),InlineKeyboardButton("Kep. Riau",callback_data=21)],
    [InlineKeyboardButton("Sumatera Barat",callback_data=13),InlineKeyboardButton("Kalimantan Utara",callback_data=65)],
    [InlineKeyboardButton("NTT",callback_data=52),InlineKeyboardButton("Sulawesi Tenggara",callback_data=74)],
    [InlineKeyboardButton("Aceh",callback_data=11),InlineKeyboardButton("Sulawesi Tengah",callback_data=72)],
    [InlineKeyboardButton("Sulawesi Utara",callback_data=71),InlineKeyboardButton("Jambi",callback_data=15)],
    [InlineKeyboardButton("Bengkulu",callback_data=17),InlineKeyboardButton("Kep. Bangka Belitung",callback_data=19)],
    [InlineKeyboardButton("Sulawesi Barat",callback_data=76),InlineKeyboardButton("Papua Barat",callback_data=91)],
    [InlineKeyboardButton("Maluku",callback_data=81),InlineKeyboardButton("Maluku Utara",callback_data=82)]]
    update.message.reply_text(text="Please select province you want to get notification from")"""



#peng = CommandHandler('settings', settings)
#dispatcher.add_handler(peng)
#dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, add_group))

def main():
    #updater = Updater(
    #    '915594611:AAGmABjTbCPZBbwgwjhenyLcTqGCNFlQCFs', use_context=True)
    #dispatcher = updater.dispatcher
    #conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],states={FIRST: [CallbackQueryHandler(decrement, pattern=0),CallbackQueryHandler(increment, pattern=2)]},fallbacks=[CommandHandler('start', start)])
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, add_group))
    dispatcher.add_handler(CommandHandler('start', startCommand))
    dispatcher.add_handler(CommandHandler('data', dataCommand))
    dispatcher.add_handler(CommandHandler('settings', settingsCommand))
    dispatcher.add_handler(CallbackQueryHandler(dataPressed, pattern=r'\d+data|\w+data'))
    dispatcher.add_handler(CallbackQueryHandler(settingsPressed))
    dispatcher.add_handler(CommandHandler('help', helpCommand))
    cekUpdate()
    updater.start_polling(poll_interval=3.0, clean=True)
    updater.idle()
    

if __name__ == "__main__":
    main()
