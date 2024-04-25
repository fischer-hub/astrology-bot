import json, random, sys, requests, os, zipfile, glob
from transformers import pipeline
#import gdown

from datetime import datetime, timezone

signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# Fetch the current time
# Using a trailing "Z" is preferred over the "+00:00" format
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

BLUESKY_HANDLE = os.environ["BLUESKY_HANDLE"]
BLUESKY_APP_PASSWORD = os.environ["BLUESKY_APP_PASSWORD"]

selected_signs = random.sample(signs, 2)

url = f"https://drive.google.com/uc?id={os.environ['MODEL_ID']}"
model_zip = 'model_355.zip'

if not glob.glob('./model/model*'):
    gdown.download(url, model_zip, quiet=False)
    
    with zipfile.ZipFile(model_zip, 'r') as zip_ref:
        zip_ref.extractall('model')

#import subprocess
#print(subprocess.run('ls;ls model', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
print(glob.glob('./model/model*'))
generate_horoscope = pipeline('text-generation', model=glob.glob('./model/model*')[0], tokenizer='gpt2')


while True:
    
    horoscope_text = generate_horoscope(f"{selected_signs[0]},")[0]['generated_text'].lower().strip()

    # last sentence was cut off probably
    if horoscope_text[-1] != '.' and horoscope_text[-1] != '!':
        horoscope_text = horoscope_text.rsplit('.', 1)[0] + '.'

    if '_' in horoscope_text:
        horoscope_text = horoscope_text.replace('_', selected_signs[1], 1)
        horoscope_text = horoscope_text.replace('_', '')

    if len(horoscope_text) <= 300:
        break

# this doesnt do anyrthing smh..
#, truncation = False, max_length = 50, min_length = 20)

print(horoscope_text)


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
    "text": horoscope_text,
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
