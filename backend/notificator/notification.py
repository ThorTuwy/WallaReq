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
        print("Number of resaults: ", len(resaults))
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
                            "url": f"{link_producto}",
                            "description": f"{description}",
                            "color": 5814783,
                            "fields": [],
                            "image": {"url": f"{imageSrc}"},
                        }
                    ],
                    # El mensaje que quieres enviar
                    "username": "Wallareq",  # Nombre del bot que aparecerá en Discord
                }
                print("webhook_mes: ", webhook_mes)
                requests.post(self.discord["webhook"], json=webhook_mes)