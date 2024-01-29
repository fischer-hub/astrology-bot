import json, random, sys, requests, os
from transformers import pipeline

from datetime import datetime, timezone

signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# Fetch the current time
# Using a trailing "Z" is preferred over the "+00:00" format
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

BLUESKY_HANDLE = os.environ["BLUESKY_HANDLE"]
BLUESKY_APP_PASSWORD = os.environ["BLUESKY_APP_PASSWORD"]


generate_horoscope = pipeline('text-generation', model="./model/", tokenizer='gpt2')


while True:
    
    horoscope_text = generate_horoscope(f"{random.choice(signs)}, ")[0]['generated_text'].lower() 

    if horoscope_text[-1] != '.':
        horoscope_text += '.'

    if len(horoscope_text) <= 300:
        break

# this doesnt do anyrthing smh..
#, truncation = False, max_length = 50, min_length = 20)

print(horoscope_text)

exit()

resp = requests.post(
    "https://bsky.social/xrpc/com.atproto.server.createSession",
    json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
)
resp.raise_for_status()
session = resp.json()
print(session["accessJwt"])

# Required fields that each post must include
post = {
    "$type": "app.bsky.feed.post",
    "text": "Hello World!",
    "createdAt": now,
    "langs": [ "th", "en-US" ]
}

resp = requests.post(
    "https://bsky.social/xrpc/com.atproto.repo.createRecord",
    headers={"Authorization": "Bearer " + session["accessJwt"]},
    json={
        "repo": session["did"],
        "collection": "app.bsky.feed.post",
        "record": post,
    },
)
print(json.dumps(resp.json(), indent=2))
resp.raise_for_status()