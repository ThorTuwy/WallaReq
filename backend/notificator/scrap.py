import http.client
import urllib.parse
import json,time



with open('./data/uploadAlready.json') as f:
    uploadAlready=json.load(f)








url = "https://api.wallapop.com/api/v3/general/search"
def queryApi(parameters):

    conn = http.client.HTTPSConnection("api.wallapop.com")

    goodParameters={}

    for key, value in parameters.items():
        if value is not None:
            goodParameters[key]=value

    query_params = urllib.parse.urlencode(goodParameters)
    
    url = f"/api/v3/search?source=quick_filters&{query_params}"

    payload = ""

    #Dont ask me why but this header is nedded for the API to repond lol
    headers = { 'X-DeviceOS': "0" }


    conn.request("GET", url, payload, headers)
    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))["data"]["section"]["payload"]["items"]


def check(topicName,parameters):

    #Defaults the first time to search with 10m before the actual time (UNIX ms)
    uploadAlready.setdefault(topicName, int(((time.time())-(1000*60))*1000))

    resaults=[]
    products=queryApi(parameters)

    
    for product in products:

        if product["modified_at"]<=uploadAlready[topicName]:
            continue

        
        
        link_producto="https://es.wallapop.com/item/"+product["web_slug"]
        title=product["title"]
        description=product["description"]
        price=product["price"]["amount"]
        imageSrc=product["images"][0]["urls"]["medium"]

        resaults.append((title,description,price,link_producto,imageSrc))
        
    print(resaults)
    return resaults

def restartTopicTime(topicName):

    uploadAlready[topicName]=int((time.time())*1000)

    with open("./data/uploadAlready.json", "w") as f:
        json.dump(uploadAlready, f)