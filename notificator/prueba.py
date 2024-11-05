import http.client
import urllib.parse

def send_request():
    conn = http.client.HTTPSConnection("api.wallapop.com")
    
   

    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

# Definir los parámetros en un diccionario


# Enviar la solicitud con los parámetros
response = send_request()

print(response)
