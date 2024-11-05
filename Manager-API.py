import notificator.main as notificator

from typing import Union

from fastapi import FastAPI
from fastapi import HTTPException

from multiprocessing import Process


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
    
#Configs Changes

@app.get("/configs")
def changeConfigs():
    pass