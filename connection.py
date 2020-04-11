import sqlite3
from datetime import datetime
from sqlite3 import Error

def create_connection(dbfile):
    '''
    specify /path/to/dbfile
    :param dbfile: database file
    :return: Connection object or None
    '''
    conn = None
    try:
        conn = sqlite3.connect(dbfile, isolation_level=None, check_same_thread=False)
        return conn
    except Error as err:
        print(err)

    return conn


def save_settings(conn, chat_id, title, chat_type, username, prov_id):
    '''
    add new records into settings table
    :param conn:
    :param chat_id:
    :param city: pass city fileds on database
    :param nilai: nilai either 1 or 0 (true/false)
    :return: chat_id
    '''
    cur = conn.cursor() #kursor connection
    #check if chat_id exists, if not then update settings
    cur.execute('select chat_id from conversations where chat_id=?;', (chat_id,))
    if cur.fetchone():
        cur.execute('select chat_id from user_preferences where chat_id=? and prov_id=?;', (chat_id, prov_id,))
        if cur.fetchone():
            cur.execute('update user_preferences set nilai=not nilai where chat_id=? and prov_id=?;',(chat_id, prov_id))
            print(datetime.now().strftime('%d-%M-%Y %H:%M ')+f"{chat_id} has changed settings for {prov_id}")
        else:
            cur.execute('insert into user_preferences (chat_id, prov_id, nilai) values(?, ?, ?);', (chat_id, prov_id, 1))

    else:
        #try:
        cur.execute('insert into conversations (chat_id, title, type, username) values(?, ?, ?, ?);', (chat_id, title,chat_type, username))
        cur.execute('insert into user_preferences (chat_id, prov_id, nilai) values(?, ?, ?);', (chat_id, prov_id, 1))
        print(datetime.now().strftime('%d-%M-%Y %H:%M ')+f"new chat id {chat_id} {username} {title} inserted to conversations and updated settings")
        #except Error as err:
            #print(err)



def read_turnedon_notif(conn):
    '''
    querying all chat_id that has tuning on notification province (1=True)
    return tuple inside list [(chat_id, prov_id, nilai), (chat_id, prov_id, nilai)]
    '''
    cur=conn.cursor()
    cur.execute('select * from user_preferences where nilai=1;')
    return cur.fetchall()