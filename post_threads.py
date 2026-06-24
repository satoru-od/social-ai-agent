import csv
import os
import requests
import json

CSV_FILE = "posts.csv"

THREADS_USER_ID = os.environ["THREADS_USER_ID"]
ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

target = None

for row in rows:
    if row["posted"] == "no":
        target = row
        break

if target is None:
    print("No posts")
    exit()

print("Posting text:")
print(target["text"])

r = requests.post(
    f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads",
    data={
        "media_type": "TEXT",
        "text": target["text"],
        "access_token": ACCESS_TOKEN,
    },
)

print("Create response status:", r.status_code)
print("Create response body:", json.dumps(r.json(), ensure_ascii=False, indent=2))

r.raise_for_status()

response_json = r.json()

if "id" not in response_json:
    raise Exception("No creation id returned from Threads API")

creation_id = response_json["id"]

publish = requests.post(
    f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish",
    data={
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    },
)

print("Publish response status:", publish.status_code)
print("Publish response body:", json.dumps(publish.json(), ensure_ascii=False, indent=2))

publish.raise_for_status()

target["posted"] = "yes"

with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["date", "text", "posted"],
    )
    writer.writeheader()
    writer.writerows(rows)
