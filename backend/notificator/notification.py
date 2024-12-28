import requests


#The notificationManager is PER TOPIC
class notificationManager():
    #Here we parse the topic and configs to get the notification methods
    def __init__(self, topic,configs):
        if topic["ntfy"]:
            self.ntfy=[]

            if not configs["ntfy"]:
                raise Exception("Ntfy is not configured (configs.json)")

            #NtfyChannels by default is a list/tuple
            ntfyChannels=topic["ntfy"] 
            if isinstance(ntfyChannels,str):
                ntfyChannels=[ntfyChannels]
            elif not isinstance(ntfyChannels,(list,tuple)):
                raise Exception("Invalid ntfy value (topicsToCheck.json)")

            for channel in ntfyChannels:
                self.ntfy.append({
                    "ntfyURL":f"{configs["ntfy"]["domain"]}/{channel}",
                    "ntfyToken":configs["ntfy"]["token"]
            })
    #Using the resault data and parse notifications send the notifications imself
    def sendNotifications(self,resaults):
        for data in resaults:
            title,description,price,link_producto,imageSrc=data
            

            if self.ntfy:
                for noti in self.ntfy:
                    requests.post(noti["ntfyURL"],
                        data=description.encode('utf-8'),
                        headers={
                            "title": f"{price} € | {title}".encode('utf-8'),
                            "click": link_producto,
                            "attach": imageSrc,
                            "authorization": f"Basic {noti["ntfyToken"]}"
                        }
                    )
                













#if __name__ == "__main__":
#   ntfySendPush(("test","test","-1","https://ntfy.tuwy.win/test","https://www.adams.es/blogs/alumno/examen-tipo-test-las-mejores-tecnicas-para-superarlo-con-exito/"),[{"ntfyURL":"https://ntfy.tuwy.win/test","ntfyToken":"***REMOVED***"}])