import requests

url = "https://ntfy.tuwy.win/"

payload = "{\"topic\":\"test\",\"message\":\"a\"}"
headers = {
    "authorization": "Basic ***REMOVED***"
}


response = requests.post(url, data=payload, headers=headers)

print(response.text)