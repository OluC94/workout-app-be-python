import requests
from my_secrets import url, key, host

headers = {
	"X-RapidAPI-Key": key,
	"X-RapidAPI-Host": host
}

querystring = {'muscle': 'glutes'}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)