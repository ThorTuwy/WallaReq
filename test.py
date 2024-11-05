import requests

url = "https://ntfy.tuwy.win/"

payload = "{\"topic\":\"test\",\"message\":\"a\"}"
headers = {
    "authorization": "Basic ***REMOVED***"
}


response = requests.post(url, data=payload, headers=headers)

print(response.text)

def dentro_de_rango_horario(inicio, fin):
    ahora = datetime.datetime.now().time()
    hora_inicio = datetime.time(*inicio)
    hora_fin = datetime.time(*fin)

    if hora_inicio <= ahora <= hora_fin:
        return True
    else:
        return False