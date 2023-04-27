import requests

response = requests.get("http://127.0.0.1:8790/films/6")

print(response.json())


