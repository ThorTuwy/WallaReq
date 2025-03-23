import requests


# The notificationManager is PER TOPIC
class notificationManager:
    # Here we parse the topic and configs to get the notification methods
    def __init__(self, topic, configs):
        noti_topic = topic["notifications"]
        noti_config = configs["notifications"]

        # NTFY
        if noti_topic["ntfy"]["channels"] != []:
            self.ntfy = []

            if (
                noti_config["ntfy"]["domain"] == ""
                or noti_config["ntfy"]["token"] == ""
            ):
                raise Exception("Ntfy is not configured (configs.json)")

            # NtfyChannels by default is a list/tuple
            ntfyChannels = noti_topic["ntfy"]
            if isinstance(ntfyChannels, str):
                ntfyChannels = [ntfyChannels]
            elif not isinstance(ntfyChannels, (list, tuple)):
                raise Exception("Invalid ntfy value (topicsToCheck.json)")

            for channel in ntfyChannels:
                self.ntfy.append(
                    {
                        "ntfyURL": f"{noti_config['ntfy']['domain']}/{channel}",
                        "ntfyToken": noti_config["ntfy"]["token"],
                    }
                )

        # Discord
        if noti_topic["discord"]["enabled_webhook"]:
            if noti_config["discord"]["webhook"] == "":
                raise Exception("Discord is not configured (configs.json)")

            self.discord = noti_config["discord"]

    # Using the resault data and parse notifications send the notifications imself
    def sendNotifications(self, resaults):
        for data in resaults:
            title, description, price, link_producto, imageSrc = data

            if hasattr(self, "ntfy"):
                for noti in self.ntfy:
                    requests.post(
                        noti["ntfyURL"],
                        data=description.encode("utf-8"),
                        headers={
                            "title": f"{price} € | {title}".encode("utf-8"),
                            "click": link_producto,
                            "attach": imageSrc,
                            "authorization": f"Basic {noti['ntfyToken']}",
                        },
                    )

            if hasattr(self, "discord"):
                webhook_mes = {
                    "content": "",
                    "embeds": [
                        {
                            "title": f"{price} € | {title}",
                            "description": f"{description}",
                            "color": 5814783,
                            "fields": [],
                            "image": {"url": f"{imageSrc}"},
                        }
                    ],
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 2,
                                    "style": 5,
                                    "label": "Enlace Wallapop",
                                    "url": f"{link_producto}",
                                }
                            ],
                        }
                    ],
                    # El mensaje que quieres enviar
                    "username": "Wallareq",  # Nombre del bot que aparecerá en Discord
                }
                requests.post(self.discord["webhook"], json=webhook_mes)


# if __name__ == "__main__":
#   ntfySendPush(("test","test","-1","https://ntfy.tuwy.win/test","https://www.adams.es/blogs/alumno/examen-tipo-test-las-mejores-tecnicas-para-superarlo-con-exito/"),[{"ntfyURL":"https://ntfy.tuwy.win/test","ntfyToken":"***REMOVED***"}])
