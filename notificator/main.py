import notificator.scrap as scrap
from notificator.notification import notificationManager

import random,time,json



#Configs
with open('./data/configs.json') as f:
    configs=json.load(f)

if not configs["general"]["sleepTime"]:
    raise Exception("SleepTime dont exist in (configs.json)")
elif not isinstance(configs["general"]["sleepTime"],(int,float)):
    raise Exception("SleepTime is not a number (configs.json)")

sleepTime=configs["general"]["sleepTime"]



with open('./data/topicsToCheck.json') as f:
    topics=json.load(f)

print(topics)

topicsToCheck={}
for name, topic in topics.items():
    try:
        if not topic["enabled"]:
            continue
    except:
        raise Exception("Invalid enabled value (topicsToCheck.json)")
    topicsToCheck[name]=topic

def main():
    #Preparing all notifications methods
    notificationMethods={}
    for name,topic in topicsToCheck.items():
        
        #Cheking querys
        if isinstance(topic["querys"],str):
            topic["querys"]=[topic["querys"]]
        elif not isinstance(topic["querys"],(list,tuple)):
            raise Exception("Invalid querys value (topicsToCheck.json)")


        notificationMethods[name]=notificationManager(topic,configs)
    


    print(topicsToCheck)

    while True:
        
        for name,topic in topicsToCheck.items():
            for parameters in topic["querys"]:
                resaults=scrap.check(name,parameters)
                notificationMethods[name].sendNotifications(resaults)
                    
            scrap.restartTopicTime(name)

        currentSleepTime=sleepTime+random.randint( round(sleepTime*(10/100)), round(sleepTime*(20/100)) )
        print(f"Cheking finish, now the program will wait: {currentSleepTime}s")
        time.sleep(currentSleepTime)
        



    