import scrap,notification,random,time,os,json

import datetime

from dotenv import load_dotenv
load_dotenv()

sleepTime=int(os.getenv('sleepTime'))*60

def dentro_de_rango_horario(inicio, fin):
    ahora = datetime.datetime.now().time()
    hora_inicio = datetime.time(*inicio)
    hora_fin = datetime.time(*fin)

    if hora_inicio <= ahora <= hora_fin:
        return True
    else:
        return False




with open('topicsToCheck.json') as f:
    topicsToCheck=json.load(f)



while True:

    for topic in topicsToCheck:
        resaults=[]

        resaults=scrap.check(topic["query"])

        if resaults:
            notification.sendPush(resaults,topic["ntfyURL"])

    time.sleep(sleepTime+random.randint( round(sleepTime*(10/100)), round(sleepTime*(20/100)) ))