import http.client
import urllib.parse
import unidecode,json,random,os



try:
    with open('./data/uploadAlredy.json') as f:
        uploadAlredy=json.load(f)
except:
    uploadAlredy={}
    with open('./data/uploadAlredy.json',"w") as f:
        json.dump({}, f)










url = "https://api.wallapop.com/api/v3/general/search"
def queryApi(parameters):

    conn = http.client.HTTPSConnection("api.wallapop.com")

    query_params = urllib.parse.urlencode(parameters)
    url = f"/api/v3/search?source=quick_filters&{query_params}"
    

    payload = ""

    #Dont ask me why but this header is nedded for the API to repond lol
    headers = { 'X-DeviceOS': "0" }


    conn.request("GET", url, payload, headers)
    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))["data"]["section"]["payload"]["items"]


def check(topicName,parameters):

    uploadAlredy.setdefault(topicName, [])

    

    resaults=[]
    item=queryApi(parameters)[0]

    

    link_producto="https://es.wallapop.com/item/"+item["web_slug"]
    
    
    
    if not link_producto in uploadAlredy[topicName]:
        uploadAlredy[topicName].append(link_producto)

        with open("./data/uploadAlredy.json", "w") as f:
            json.dump(uploadAlredy, f)

        title=item["title"]
        description=item["description"]
        price=item["price"]["amount"]
        imageSrc=item["images"][0]["urls"]["medium"]

        
        
        resaults=[title,description,price,link_producto,imageSrc]
    
    return resaults

