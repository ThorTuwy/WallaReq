import json,os,shutil
dataDirectory="./data"
templatesDirectory="./dataTemplates"
def verifyData():
    print("Verifying data...")
    for templateFilename in os.listdir(templatesDirectory):

        templateFile = os.path.join(templatesDirectory, templateFilename)
        dataFile = os.path.join(dataDirectory, templateFilename)

        try:
            with open(dataFile) as f:
                json.load(f)
        except:
            shutil.copy(templateFile, dataFile)
verifyData()