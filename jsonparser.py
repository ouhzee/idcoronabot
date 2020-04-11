import requests, json
import connection
from datetime import datetime
UPDATEINDONESIA = None
#with open('provinsi.json', 'r') as file:
#    UPDATEPROVINCE = json.load(file)
UPDATEPROVINCE = None
#COUNTERPOSITIF = None
#COUNTERSEMBUH = None
#COUNTERMENINGGAL = 0
PREFERENCES = None
TURNEDONNOTIF = []
COUNTERINDO = {}
COUNTERPROVINCE = {}
listprov = [11,12,13,14,15,16,17,18,19,21,31,32,33,34,35,36,51,52,61,62,63,64,65,71,72,73,74,76,81,82,91,94]


def getUpdate(namaData):
    '''
    pass either 'indonesia' or 'provinsi' as a string.
    
    '''
    global UPDATEINDONESIA
    global UPDATEPROVINCE
    apiUrl = "https://api.kawalcorona.com/"
    if namaData == 'indonesia':
        ambil = 'indonesia'
        UPDATEINDONESIA = json.loads((requests.get('https://api.kawalcorona.com/indonesia')).text)
    elif namaData == 'provinsi':
        ambil = 'indonesia/provinsi'
        UPDATEPROVINCE = json.loads((requests.get(apiUrl + ambil)).text)
    

def tofile(namafile):
    '''write to file pass the filename'''
    with open(namafile + '.json', 'w') as data :
        if namafile == 'indonesia':
            json.dump(UPDATEINDONESIA, data)
            with open('counterindo.json','w') as indo:
                json.dump(COUNTERINDO, indo)
            with open('lastupdate.txt', 'w') as file:
                file.write(datetime.now().strftime('%d, %B %Y %H:%M'))
        elif namafile == 'provinsi':
            json.dump(UPDATEPROVINCE, data)
            with open('counterprovince.json', 'w')as prov:
                json.dump(COUNTERPROVINCE, prov)


def cekChanges(conn):
    '''
    if yes > return 1
    '''
    
    #global COUNTERMENINGGAL
    #global COUNTERPOSITIF
    #global COUNTERSEMBUH
    global COUNTERINDO
    global UPDATEINDONESIA
    getUpdate('indonesia')
    with open('indonesia.json', 'r') as file:
        old = [i for i in json.load(file)]
    new =  [y for y in UPDATEINDONESIA]
        
    oldPositif = int(old[0]['positif'].replace(',', ''))
    newPositif = int(new[0]['positif'].replace(',', ''))
    oldSembuh = int(old[0]['sembuh'].replace(',', ''))
    newSembuh = int(new[0]['sembuh'].replace(',', ''))
    oldMeninggal = int(old[0]['meninggal'].replace(',', ''))
    newMeninggal = int(new[0]['meninggal'].replace(',', ''))
    
    if oldPositif != newPositif\
        or oldSembuh != newSembuh\
            or oldMeninggal != newMeninggal:
            COUNTERINDO['positif'] = newPositif-oldPositif
            COUNTERINDO['sembuh'] = newSembuh-oldSembuh
            COUNTERINDO['meninggal'] = newMeninggal-oldMeninggal
            tofile('indonesia')
            print(datetime.now().strftime('%d-%M-%Y %H:%M ')+"New data update from menkes")
            getUpdate('provinsi')
            #updateCounter(conn)
            #tofile('provinsi')
            return True
            
    else:
        print(datetime.now().strftime('%d-%M-%Y %H:%M ')+'No update found')
        return False


def updateCounter(conn):
    '''
    result will be COUNTERPROVINCE = [prov_id {'positif': value, 'sembuh':...}]
    '''
    #counter = 0
    global TURNEDONNOTIF
    global PREFERENCES
    global COUNTERPROVINCE
    global UPDATEPROVINCE
    global listprov
    PREFERENCES = connection.read_turnedon_notif(conn)
    for prov_id in PREFERENCES:
        TURNEDONNOTIF.append(prov_id[1])
    TURNEDONNOTIF = list(set(TURNEDONNOTIF))
    #getUpdate('provinsi')
    with open('provinsi.json') as file:
        old = [i for i in json.load(file)]
    '''for notif in TURNEDONNOTIF:
        for counter,dataOld in enumerate(old):
            if (dataOld['attributes']['Kode_Provi'] == notif and UPDATEPROVINCE[counter]['attributes']['Kode_Provi'] == notif):
                COUNTERPROVINCE[notif] = {'positif': UPDATEPROVINCE[counter]['attributes']['Kasus_Posi'] - dataOld['attributes']['Kasus_Posi'], 'sembuh': UPDATEPROVINCE[counter]['attributes']['Kasus_Semb'] - dataOld['attributes']['Kasus_Semb'], 'meninggal': UPDATEPROVINCE[counter]['attributes']['Kasus_Meni'] - dataOld['attributes']['Kasus_Meni']}
                tofile('provinsi')'''
    for idprov in listprov:
        for counter,dataOld in enumerate(old):
            if (dataOld['attributes']['Kode_Provi'] == idprov and UPDATEPROVINCE[counter]['attributes']['Kode_Provi'] == idprov):
                COUNTERPROVINCE[idprov] = {'positif': UPDATEPROVINCE[counter]['attributes']['Kasus_Posi'] - dataOld['attributes']['Kasus_Posi'], 'sembuh': UPDATEPROVINCE[counter]['attributes']['Kasus_Semb'] - dataOld['attributes']['Kasus_Semb'], 'meninggal': UPDATEPROVINCE[counter]['attributes']['Kasus_Meni'] - dataOld['attributes']['Kasus_Meni']}
                tofile('provinsi')



def parseCounter(prov_id):
    '''
    pass prov_id return positif, sembuh, meninggal in sequence
    '''
    with open('counterprovince.json','r') as provi:
        counter = json.load(provi)
    #try:
    return counter[str(prov_id)]['positif'], counter[str(prov_id)]['sembuh'], counter[str(prov_id)]['meninggal']
    #except KeyError:
    #    return 0,0,0


def dataProvince(prov_id):
    '''pass the prov id to search. return nama provinsi, positif, sembuh, meninggal'''
    result = []
    with open('provinsi.json', 'r') as file:
        data = [i for i in json.load(file)]
    for id in data:
        if prov_id == id['attributes']['Kode_Provi']:
            result.append(id['attributes']['Provinsi']) 
            result.append(id['attributes']['Kasus_Posi'])
            result.append(id['attributes']['Kasus_Semb'])
            result.append(id['attributes']['Kasus_Meni'])
    return result


def dataIndonesia():
    '''
    return data positif,sembuh,meninggal, counter positif,sembuh,meninggal
    '''
    #global COUNTERMENINGGAL
    #global COUNTERPOSITIF
    #global COUNTERSEMBUH
    global COUNTERINDO
    with open('indonesia.json', 'r') as file, open('counterindo.json','r') as indo:
        counter = json.load(indo)
        data = [i for i in json.load(file)]

    return data[0]['positif'], data[0]['sembuh'], data[0]['meninggal'], counter['positif'],counter['sembuh'],counter['meninggal']

"""def spesifik_prov(Kode_Provi):
    '''
    masukin kode provinsi.
    return "Provinsi", "Positif", "Sembuh", "Meninggal"
    '''
    with open('mydata.json') as f:
        parsed_data = json.load(f)

    for item in parsed_data:
        if item.get("attributes").get('Kode_Provi') == Kode_Provi:
            dotget = item.get('attributes')
            return dotget.get("Provinsi"), dotget.get("Kasus_Posi"), \
                dotget.get("Kasus_Semb"), dotget.get("Kasus_Meni")


print(f"Provinsi: {spesifik_prov(32)[0]}, Positif: {spesifik_prov(32)[1]},\
Sembuh: {spesifik_prov(32)[2]}, Meninggal: {spesifik_prov(32)[3]}")"""



'''for item in js:
    if item.get("attributes").get("Provinsi") == "DKI Jakarta":
        #print(item.get("attributes").get("Kode_Provi"))
        item["attributes"]["FID"]'''

"""todos_by_user = {}

# Increment complete TODOs count for each user.
for todo in todos:
    if todo["completed"]:
        try:
            # Increment the existing user's count.
            todos_by_user[todo["userId"]] += 1
        except KeyError:
            # This user has not been seen. Set their count to 1.
            todos_by_user[todo["userId"]] = 1

# Create a sorted list of (userId, num_complete) pairs.
top_users = sorted(todos_by_user.items(), 
                   key=lambda x: x[1], reverse=True)

# Get the maximum number of complete TODOs.
max_complete = top_users[0][1]

# Create a list of all users who have completed
# the maximum number of TODOs.
users = []
for user, num_complete in top_users:
    if num_complete < max_complete:
        break
    users.append(str(user))

max_users = " and ".join(users)"""