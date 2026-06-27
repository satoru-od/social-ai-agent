import os
import json
import requests

INSTAGRAM_ACCESS_TOKEN = os.environ["INSTAGRAM_ACCESS_TOKEN"]

response = requests.get(
    "https://graph.instagram.com/me",
    params={
        "fields": "id,username",
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    },
)

print("Status:", response.status_code)
print(json.dumps(response.json(), ensure_ascii=False, indent=2))

response.raise_for_status()
