import requests,base64,os

from dotenv import load_dotenv
load_dotenv()

def sendPush(data,ntfyURL):

    title,description,price,link_producto,imageSrc=data
    requests.post(ntfyURL,
    data=description,
    headers={
        "Title": f"{price} € | {title}".encode('utf-8'),
        "Click": link_producto,
        "Attach": imageSrc,
        "Authorization": f"Basic {os.getenv('TOKEN')}"
    })