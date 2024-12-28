import notificator.main as notificator

from typing import Union

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from multiprocessing import Process

import json

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:4321",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


notificatorProcess=None



#Notificator related API

@app.get("/start")
def startNoti():
    global notificatorProcess

    if notificatorProcess:
        raise HTTPException(status_code=409, detail="The program is already started up!")

    notificatorProcess = Process(target = notificator.main)
    notificatorProcess.start()

@app.get("/stop")
def stopNoti():
    global notificatorProcess

    if not notificatorProcess:
        raise HTTPException(status_code=409, detail="The program is already stoped!")

    notificatorProcess.terminate()

    notificatorProcess=None

@app.get("/restart")
def restartNoti():
    stopNoti()
    startNoti()
    


@app.get("/config")
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
    general: general = None
    ntfy: ntfy = None


@app.put("/config")
def update_item(item: Config):
    
    with open('./data/configs.json') as f:
        configs=json.load(f)
    
    newConfig = jsonable_encoder(item)



    #If they return censured values, we arent going to change them
    for pkey, sections in newConfig.items():
        configs.setdefault(pkey, {})
        for key, value in sections.items():
            if value and value.replace("*", "")!="":
                configs[pkey][key]=newConfig[pkey][key]
    
    with open('./data/configs.json',"w") as f:
        json.dump(configs, f, sort_keys=True,indent=4)


#Topics related API

@app.get("/topics")
def getTopics():

    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)

    resTopics={}
    for key, topic in topics.items():
        resTopics[key]=topic["enabled"]
    
    return JSONResponse(content=resTopics) 

@app.get("/topics/{topic}")
def getTopic(topic:str):

    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)
    
    return JSONResponse(content=topics[topic])


class queryModel(BaseModel):
    keywords: str
    order_by: str 
    is_shippable: bool = None
    max_sale_price: int = None
    min_sale_price: int = None
    category_ids: int = None
    latitude: int = None
    longitude: int = None
    condition: str = None


class topicModel(BaseModel):
    name: str
    enabled: bool
    querys: list[queryModel]
    ntfy: list[str] = None



@app.put("/topics/update")
def update_item(topic: topicModel):
    
    newTopic = jsonable_encoder(topic)
    name=newTopic["name"].lower()
    del newTopic["name"]

    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)
    
    topics[name]=newTopic

    with open('./data/topicsToCheck.json',"w") as f:
        json.dump(topics, f, sort_keys=True,indent=4)

@app.put("/topics/add")
def update_item(name: str):
    name=name.lower()
    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)
    
    topics[name]={"enabled":False,"querys":[],"ntfy":[]}

    with open('./data/topicsToCheck.json',"w") as f:
        json.dump(topics, f, sort_keys=True,indent=4)

@app.put("/topics/remove")
def update_item(name: str):

    with open('./data/topicsToCheck.json') as f:
        topics=json.load(f)
    
    del topics[name]

    with open('./data/topicsToCheck.json',"w") as f:
        json.dump(topics, f, sort_keys=True,indent=4)


@app.put("/uploadAlready/remove")
def getTopic(topicName:str):
    
    with open('./data/uploadAlredy.json') as f:
        topics=json.load(f)
    
    print(topicName)
    del topics[topicName]

    with open('./data/uploadAlredy.json',"w") as f:
        json.dump(topics, f, sort_keys=True,indent=4)