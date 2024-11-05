import scrap,notification,random,time,os,json,datetime

#Configs
with open('./data/configs.json') as f:
    configs=json.load(f)

if not configs["general"]["sleepTime"]:
    raise Exception("SleepTime dont exist in (configs.json)")
elif not isinstance(configs["general"]["sleepTime"],(int,float)):
    raise Exception("SleepTime is not a number (configs.json)")

sleepTime=configs["general"]["sleepTime"]*60



with open('./data/topicsToCheck.json') as f:
    topicsToCheck=json.load(f)





def ntfyToMethods(ntfyChannels):
    if not configs["ntfy"]:
        raise Exception("Ntfy is not configured (configs.json)")

    ntfyMethods=[]

    if isinstance(ntfyChannels,str):
        ntfyChannels=[ntfyChannels]
    elif not isinstance(ntfyChannels,(list,tuple)):
        raise Exception("Invalid ntfy value (topicsToCheck.json)")

    for channel in ntfyChannels:

        ntfyMethods.append({
            "ntfyURL":f"{configs["ntfy"]["domain"]}/{channel}",
            "ntfyToken":configs["ntfy"]["token"]
        })
    
    return ntfyMethods




def main():
    #Preparing all notifications methods
    notificationMethods={}
    for topic in topicsToCheck:
        

        topicNotificationMethods={}

        if topic["ntfy"]:
            topicNotificationMethods["ntfy"]=ntfyToMethods(topic["ntfy"])

            
        
        notificationMethods[topic["name"]]=topicNotificationMethods
    
    while True:
        for topic in topicsToCheck:
            resaults=scrap.check(topic["query"])
            if resaults:
                notification.sendNotifications(resaults,notificationMethods[topic["name"]])
        
        currentSleepTime=sleepTime+random.randint( round(sleepTime*(10/100)), round(sleepTime*(20/100)) )
        print(f"Cheking finish, now the program will wait: {currentSleepTime}s")
        time.sleep(currentSleepTime)
        

if __name__ == "__main__":
    main()



    