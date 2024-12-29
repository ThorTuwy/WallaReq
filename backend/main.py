import notificator.main as notificator

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse,RedirectResponse



from multiprocessing import Process

import json

from pydantic import BaseModel


app = FastAPI()




notificatorProcess=None







def recursiveJSONMerger(main, mew):
    
     

    if type(mew) is not dict:
        main=mew
        return main
    
    for key, value in mew.items():
        
        

        if (type(value) is str and value.replace("*", "")==""):
            continue

        if isinstance(value, dict):
            if key not in main:
                main[key]={}
            recursiveJSONMerger(main[key],value)

        elif isinstance(value, list):
            main[key]=[]
            
            for i in value:
                main[key].append(recursiveJSONMerger({},i))
                
        else:
            main[key]=value
            if value=="":
                main[key]=None

    return main


#Notificator related API

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


@app.get("/")
def startNoti():
    return RedirectResponse("/index.html")

@app.get("/API/start")
def startNoti():
    global notificatorProcess

    if notificatorProcess:
        raise HTTPException(status_code=409, detail="The program is already started up!")

    notificatorProcess = Process(target = notificator.main)
    notificatorProcess.start()

@app.get("/API/stop")
def stopNoti():
    global notificatorProcess

    if not notificatorProcess:
        raise HTTPException(status_code=409, detail="The program is already stoped!")

    notificatorProcess.terminate()

    notificatorProcess=None

@app.get("/API/status")
def stopNoti():
    global notificatorProcess

    return notificatorProcess!=None

@app.get("/API/restart")
def restartNoti():
    stopNoti()
    startNoti()
    


@app.get("/API/config")
def changeConfigs():

    #For security reasons, this would not return token and other sensitive data
    securityDataCheck=["token"]

    with open('./data/configs.json') as f:
        configs=json.load(f)
    
    for pkey, sections in configs.items():
        for key, _ in sections.items():
            if key in securityDataCheck:
                configs[pkey][key]="*"*len(configs[pkey][key])
    
    return JSONResponse(content=configs) 





class general(BaseModel):
    sleepTime: int

class ntfy(BaseModel):
    token: str
    domain: str

class Config(BaseModel):
    general: general 
    ntfy: ntfy


@app.put("/API/config")
def update_item(item: Config):
    
    with open('./data/configs.json') as f:
        configs=json.load(f)
    
    newConfig = jsonable_encoder(item)



    # Ignoring None values
    # Also If they return censured values, we arent going to change them
    
    configs=recursiveJSONMerger(configs,newConfig)

    with open('./data/configs.json',"w") as f:
        json.dump(configs, f, sort_keys=True,indent=4)


#Topics related API

@app.get("/API/topics")
def getTopics():

    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)

    resTopics={}
    for key, topic in topics.items():
        resTopics[key]=topic["enabled"]
    
    return JSONResponse(content=resTopics) 

@app.get("/API/topics/{topic}")
def getTopic(topic:str):

    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)
    
    return JSONResponse(content=topics[topic])


class queryModel(BaseModel):
    keywords: str
    order_by: str 
    is_shippable: bool | str | None = None
    max_sale_price: int | str | None   = None
    min_sale_price: int | str | None   = None
    category_ids: int | str | None   = None
    latitude: int | str | None  = None
    longitude: int | str | None  = None
    condition: str | str | None  = None


class topicModel(BaseModel):
    name: str
    enabled: bool
    querys: list[queryModel]
    ntfy: list[str] | None  = None



@app.put("/API/topics/update")
def update_item(topic: topicModel):
    
    newTopic = jsonable_encoder(topic)
    name=newTopic["name"].lower()
    del newTopic["name"]

    if(name==""):
        raise HTTPException(status_code=409, detail="Name can't be empty")

    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)
    
    topic={}
    if name in topics:
        topic=topics[name]

    topics[name]=recursiveJSONMerger(topic,newTopic)

    with open('./data/topicsToCheck.json',"w") as f:
        json.dump(topics, f, sort_keys=True,indent=4)

@app.put("/API/topics/add")
def update_item(name: str):
    name=name.lower()
    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)
    
    topics[name]={"enabled":False,"querys":[],"ntfy":[]}

    with open('./data/topicsToCheck.json',"w") as f:
        json.dump(topics, f, sort_keys=True,indent=4)

@app.put("/API/topics/remove")
def update_item(name: str):

    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)
    
    del topics[name]

    with open('./data/topicsToCheck.json',"w") as f:
        json.dump(topics, f, sort_keys=True,indent=4)


@app.put("/API/uploadAlready/remove")
def getTopic(topicName:str):
    
    with open('./data/uploadAlredy.json') as f:
        topics=json.load(f)
    
    print(topicName)
    del topics[topicName]

    with open('./data/uploadAlredy.json',"w") as f:
        json.dump(topics, f, sort_keys=True,indent=4)


app.mount("/", StaticFiles(directory="dist"), name="static")
