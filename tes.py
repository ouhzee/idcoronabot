import json, requests

import sqlite3
from sqlite3 import Error

apiUrl = 'https://api.kawalcorona.com/indonesia'
hasil = json.loads(requests.get(apiUrl).text)


conn = create_connection('corona.db')

cur = conn.cursor()
cur.execute('pragma foreign_keys = on;')
save_settings(conn, 200, 'none', 'supergroup', '@user', 32, 1)
#cur.execute('insert into user_preferences values(-1000, 32, 1);')
conn.close()



"""def bannerMessage(file):
    '''
    provide file path name
    '''
    with open(file, 'r') as banner:
        #ambil = json.load(banner)
    
        #for i in json.load(banner):
            #if int(i.get('positif').replace(',', '')) >= 1677:
        parsed = [i for i in json.load(banner)]
        if int(parsed[0]["positif"].replace(',', '')) == 1677:
                print(parsed[0]['positif'])


bannerMessage('indonesia.json')
#bannerMessage('c:\\Users\\adeqecil\\bot_corona\\addGroup.txt')"""