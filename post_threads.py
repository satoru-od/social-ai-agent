import os
import requests
import json

INSTAGRAM_ACCESS_TOKEN = os.environ["INSTAGRAM_ACCESS_TOKEN"]

r = requests.get(
    "https://graph.instagram.com/me",
    params={
        "fields": "id,username",
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    },
)

print("Status:", r.status_code)
print(json.dumps(r.json(), ensure_ascii=False, indent=2))

r.raise_for_status()
