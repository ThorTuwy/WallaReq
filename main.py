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

        #notificationMethods[String]=[{data to process the noti},...]
        notificationMethods={}
        if topic["ntfy"]:
            
            notificationMethods["ntfy"]=[]
                        
            ntfyChannels=topic["ntfy"]

            if isinstance(topic["ntfy"],str):
                ntfyChannels=[topic["ntfy"]]
            elif not isinstance(topic["ntfy"],(array,tuple)):
                raise Exception("Invalid ntfy value in topicsToCheck.json")

            for channel in ntfyChannels:

                notificationMethods["ntfy"].append({
                    "ntfyURL":f"{os.getenv('NTFY_DOMAIN')}/{channel}",
                    "ntfyToken":os.getenv('NTFY_TOKEN')
                })
        

        if resaults:
            notification.sendNotifications(resaults,notificationMethods)

    #Sleep: sleepTime+sleepTime[10%,20%]
    time.sleep(sleepTime+random.randint( round(sleepTime*(10/100)), round(sleepTime*(20/100)) ))