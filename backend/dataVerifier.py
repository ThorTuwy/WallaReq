import tomllib,json,os,shutil
dataDirectory="./data"
templatesDirectory="./dataTemplates"


def makeConfig() -> dict:
    configsFile = os.path.join(templatesDirectory, "configs.toml")
    
    with open(configsFile, 'rb') as f:
        configs=tomllib.load(f)
    

    configDic={}

    for categorieKey, categorie in configs.items():
        configDic[categorieKey]={}
        for configKey, config in categorie.items():
            if "defaultValue" in config:
                configDic[categorieKey][configKey]=config["defaultValue"]
                continue

            match config["type"]:
                case "text" | "select":
                    configDic[categorieKey][configKey]=""
                case "number":
                    configDic[categorieKey][configKey]=0
                case "checkbox":
                    configDic[categorieKey][configKey]=False
                case "stringArray":
                    configDic[categorieKey][configKey]=[]
                case _:
                    raise ValueError("Not a valid type")
    
    return configDic
            
def verifyData():
    print("Verifying data...")
    for dataName in ["configs","topicsToCheck","uploadAlready"]:

        dataFile = os.path.join(dataDirectory, dataName+".json")

        try:
            with open(dataFile) as f:
                json.load(f)
        except:
            with open(dataFile,"w") as f:
                if dataName=="configs":
                    json.dump(makeConfig(), f)
                    continue
                json.dump({}, f)
verifyData()