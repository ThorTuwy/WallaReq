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
            data=description.encode('utf-8'),
            headers={
                "title": f"{price} € | {title}".encode('utf-8'),
                "click": link_producto,
                "attach": imageSrc,
                "authorization": f"Basic {noti["ntfyToken"]}"
            }
        )

if __name__ == "__main__":
   ntfySendPush(("test","test","-1","https://ntfy.tuwy.win/test","https://www.adams.es/blogs/alumno/examen-tipo-test-las-mejores-tecnicas-para-superarlo-con-exito/"),[{"ntfyURL":"https://ntfy.tuwy.win/test","ntfyToken":"***REMOVED***"}])