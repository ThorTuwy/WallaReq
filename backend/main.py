from fastapi import FastAPI, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import copy
import json
from multiprocessing import Process

import dataTemplates.configs_model as configs_model
import dataTemplates.topicsToCheck_model as topics_model

import notificator.main as notificator

dataDirectory = "./data"
templatesDirectory = "./dataTemplates"

TOPIC_TEMPLATE = {}
with open("./dataTemplates/template_topicsToCheck.json") as f:
    TOPIC_TEMPLATE = json.load(f)

CONFIGS_TEMPLATE = {}
with open("./dataTemplates/template_configs.json") as f:
    CONFIGS_TEMPLATE = json.load(f)


# If a JSON of data is not valid or is missing, this function will copy the dataTemplate of that file.


app = FastAPI()


def recursiveJSONMerger(main, new, template):
    if type(new) is not dict:
        main = new
        return main

    for key, value in new.items():
        new_template = None
        if key in template:
            new_template = template[key]

        if type(value) is str and value.replace("*", "") == "":
            continue

        if isinstance(value, dict):
            if key not in main:
                main[key] = {}
            recursiveJSONMerger(main[key], value, new_template)

        elif isinstance(value, list):
            main[key] = []

            for i in range(len(value)):
                main[key].append(recursiveJSONMerger({}, value[i], new_template))

        elif not value:
            main[key] = new_template
        else:
            main[key] = value

    return main


@app.get("/")
def getApp():
    return RedirectResponse("/index.html")


notificatorProcess = None


@app.get("/API/start")
def startNoti():
    global notificatorProcess

    if notificatorProcess:
        raise HTTPException(
            status_code=409, detail="The program is already started up!"
        )

    notificatorProcess = Process(target=notificator.main)
    notificatorProcess.start()


@app.get("/API/stop")
def stopNoti():
    global notificatorProcess

    if not notificatorProcess:
        raise HTTPException(status_code=409, detail="The program is already stoped!")

    notificatorProcess.terminate()

    notificatorProcess = None


@app.get("/API/status")
def getStatus():
    global notificatorProcess

    return notificatorProcess is not None


@app.get("/API/restart")
def restartNoti():
    stopNoti()
    startNoti()


@app.get("/API/config")
def changeConfigs():
    # For security reasons, this would not return token and other sensitive data
    securityDataCheck = ["token"]

    with open("./data/configs.json") as f:
        configs = json.load(f)

    for pkey, sections in configs.items():
        for key, _ in sections.items():
            if key in securityDataCheck:
                configs[pkey][key] = "*" * len(configs[pkey][key])

    return JSONResponse(content=configs)


@app.put("/API/config")
def get_config(item: configs_model.Configs):
    with open("./data/configs.json") as f:
        configs = json.load(f)

    newConfig = jsonable_encoder(item)

    # Ignoring None values
    # Also If they return censured values, we arent going to change them

    configs = recursiveJSONMerger(configs, newConfig, CONFIGS_TEMPLATE)

    with open("./data/configs.json", "w") as f:
        json.dump(configs, f, sort_keys=True, indent=4)


# Topics related API


@app.get("/API/topics")
def getTopics():
    with open("./data/topicsToCheck.json") as f:
        topics = json.load(f)

    resTopics = {}
    for key, topic in topics.items():
        resTopics[key] = topic["enabled"]

    return JSONResponse(content=resTopics)


@app.get("/API/topics/{topic}")
def getTopic(topic: str):
    with open("./data/topicsToCheck.json") as f:
        topics = json.load(f)

    return JSONResponse(content=topics[topic])


def recursiveJSONRemoveEmptyStrings(data):
    if type(data) is not dict:
        return data

    for key, value in data.items():
        if value == "":
            data[key] = None

        if isinstance(value, dict):
            recursiveJSONRemoveEmptyStrings(value)

        elif isinstance(value, list):
            for i in range(len(value)):
                recursiveJSONRemoveEmptyStrings(value[i])

    return data


@app.put("/API/topics/update")
async def update_item(topic_raw: Request):
    data = await topic_raw.json()
    data = recursiveJSONRemoveEmptyStrings(data)
    topic = topics_model.TopicsToCheck(**data)

    newTopic = jsonable_encoder(topic)
    name = newTopic["name"].lower()

    del newTopic["name"]

    if name == "":
        raise HTTPException(status_code=409, detail="Name can't be empty")

    with open("./data/topicsToCheck.json") as f:
        topics = json.load(f)

    topic = {}
    if name in topics:
        topic = topics[name]

    topics[name] = recursiveJSONMerger(topic, newTopic, TOPIC_TEMPLATE)

    with open("./data/topicsToCheck.json", "w") as f:
        json.dump(topics, f, sort_keys=True, indent=4)


@app.put("/API/topics/add")
def add_item(name: str):
    name = name.lower()
    with open("./data/topicsToCheck.json") as f:
        topics = json.load(f)

    topics[name] = copy.deepcopy(TOPIC_TEMPLATE)

    with open("./data/topicsToCheck.json", "w") as f:
        json.dump(topics, f, sort_keys=True, indent=4)


@app.put("/API/topics/remove")
def remove_topic(name: str):
    with open("./data/topicsToCheck.json") as f:
        topics = json.load(f)

    del topics[name]

    with open("./data/topicsToCheck.json", "w") as f:
        json.dump(topics, f, sort_keys=True, indent=4)


@app.put("/API/uploadAlready/remove")
def reset_uploadAlready(topicName: str):
    with open("./data/uploadAlready.json") as f:
        topics = json.load(f)

    del topics[topicName]

    with open("./data/uploadAlready.json", "w") as f:
        json.dump(topics, f, sort_keys=True, indent=4)


app.mount("/", StaticFiles(directory="dist"), name="static")
