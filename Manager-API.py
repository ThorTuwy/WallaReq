import notificator.main as notificator

from typing import Union

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from multiprocessing import Process

import json

from pydantic import BaseModel


app = FastAPI()

notificatorProcess=None



#Notificator related API

@app.get("/start")
def startNoti():
    global notificatorProcess

    if notificatorProcess:
        raise HTTPException(status_code=409, detail="The program is already started up")

    notificatorProcess = Process(target = notificator.main)
    notificatorProcess.start()

@app.get("/stop")
def stopNoti():
    global notificatorProcess

    if not notificatorProcess:
        raise HTTPException(status_code=409, detail="The program is already stoped")

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
    general: general | None
    ntfy: ntfy | None


@app.put("/config")
def update_item(item: Config):
    
    with open('./data/configs.json') as f:
        configs=json.load(f)
    
    newConfig = jsonable_encoder(item)

    for pkey, sections in newConfig.items():
        for key, value in sections.items():
            configs.setdefault(pkey, {})
            if value:
                configs[pkey][key]=newConfig[pkey][key]
    
    with open('./data/configs.json',"w") as f:
        json.dump(configs, f, sort_keys=True,indent=4)



@app.put("/config")
def update_item(item: Config):
    
    with open('./data/configs.json') as f:
        configs=json.load(f)
    
    newConfig = jsonable_encoder(item)

    for pkey, sections in newConfig.items():
        for key, value in sections.items():
            configs.setdefault(pkey, {})
            if value:
                configs[pkey][key]=newConfig[pkey][key]
    
    with open('./data/configs.json',"w") as f:
        json.dump(configs, f, sort_keys=True,indent=4)
