import http.client
import urllib.parse
import unidecode,json,random,os

if not os.path.exists('uploadAlredy.json'):
    with open('uploadAlredy.json', "w") as f:
        json.dump([], f)

with open('uploadAlredy.json') as f:
    uploadAlredy=json.load(f)










url = "https://api.wallapop.com/api/v3/general/search"
def queryApi(parameters):
    conn = http.client.HTTPSConnection("api.wallapop.com")

    query_params = urllib.parse.urlencode(parameters)
    url = f"/api/v3/general/search?{query_params}"
    

    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))["search_objects"]


def check(keywords):
    resaults=[]

    item=queryApi(keywords)[0]

    

    link_producto="https://es.wallapop.com/item/"+item["web_slug"]
    
    if not link_producto in uploadAlredy:
        uploadAlredy.append(link_producto)

        title=item["title"]
        description=item["description"]
        price=item["price"]
        imageSrc=item["images"][0]["original"]

        with open("uploadAlredy.json", "w") as f:
            json.dump(uploadAlredy, f)
        
        resaults=[title,description,price,link_producto,imageSrc]
    
    return resaults

