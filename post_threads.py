import csv
import os
import requests

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

r = requests.post(
    f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads",
    data={
        "media_type": "TEXT",
        "text": target["text"],
        "access_token": ACCESS_TOKEN,
    },
)

creation_id = r.json()["id"]

requests.post(
    f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish",
    data={
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    },
)

target["posted"] = "yes"

with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["date", "text", "posted"],
    )
    writer.writeheader()
    writer.writerows(rows)
