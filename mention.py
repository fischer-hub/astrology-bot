import requests, json
from datetime import datetime, timezone
from dicts import zodiac_last_day, zodiac_compatibility

now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def check_and_answer_mentions(session):


    print('requesting notification list..')
    notifs = requests.get('https://bsky.social/xrpc/app.bsky.notification.listNotifications',
        headers={"Authorization": "Bearer " + session["accessJwt"]},
        ).json()['notifications']

    # filter notifs for mentions that are unseen
    mentions = [notif for notif in notifs if notif['reason'] == 'mention']
    unseen_mentions = [notif for notif in mentions if not notif['isRead']]

    for mention in unseen_mentions:
        
        if 'reply' in mention['record']:
            reply_parent = mention['record']['reply']['parent']
        else: 
            continue
        
        parent_uri = reply_parent['uri']
        # leave me alone i know its stupid
        parent_did = 'did:' + parent_uri.split('did:')[1].split('/')[0]
        parent_profile_creation_date = requests.get('https://bsky.social/xrpc/app.bsky.actor.getProfile',
            headers={"Authorization": "Bearer " + session["accessJwt"]},
            params={"actor": parent_did}
            ).json()['createdAt']
        print('parent records profile was created at:\n', parent_profile_creation_date)
        
        mention_profile = requests.get('https://bsky.social/xrpc/app.bsky.actor.getProfile',
            headers={"Authorization": "Bearer " + session["accessJwt"]},
            params={"actor": mention['author']['did']}
            ).json()
            
        mention_profile_creation_date = mention_profile['createdAt']
            
        if 'kinderpingui' in mention['record']['text'] or 'kinderpingui' in mention_profile['handle']:
            kinderpingui = True
            
        print(mention_profile['handle'])
            
        print('profile of persion tagging the bot was created at:\n', mention_profile_creation_date)
    #print(unseen_mentions[0]['record']['reply']['parent'])
    #print(json.dumps(resp.json(), indent=2))
        resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": "Bearer " + session["accessJwt"]},
            json={
                "repo": session['did'],
                "collection": "app.bsky.feed.post",
                "record": {
                    "text": "i summon you cyndi lauper",
                    "reply": mention['record']['reply'],
                    "createdAt": "2024-11-18T12:34:56.789Z"
                }
                }
        )
        print(resp.json())
        # set notification to seen
        /xrpc/app.bsky.notification.updateSeen
    resp.raise_for_status()

    #/xrpc/app.bsky.notification.listNotifications