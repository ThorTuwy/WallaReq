import requests,base64,os

from dotenv import load_dotenv
load_dotenv()

def sendNotifications(data,notificationMethods):
    #notificationMethods[String]=[{data to process the noti},...]
    if "ntfy" in notificationMethods:
        ntfySendPush(data,notificationMethods["ntfy"])

def ntfySendPush(data,ntfyNotifications):
    title,description,price,link_producto,imageSrc=data

    for noti in ntfyNotifications:

        
        requests.post(noti["ntfyURL"],
            data=description,
            headers={
                "Title": f"{price} € | {title}".encode('utf-8'),
                "Click": link_producto,
                "Attach": imageSrc,
                "Authorization": f"Basic {noti["ntfyToken"]}"
            }
        )

