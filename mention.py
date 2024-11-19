import requests, json, random
from datetime import datetime, timezone
from dicts import zodiac_last_day, zodiac_compatibility, good_compatibility, medium_compatibility, bad_compatibility

now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def check_and_answer_mentions(session):

    request_header = {"Authorization": "Bearer " + session["accessJwt"]}

    print('requesting notification list..')
    notifs = requests.get('https://bsky.social/xrpc/app.bsky.notification.listNotifications',
                            headers = request_header).json()['notifications']

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
        parent_profile = requests.get('https://bsky.social/xrpc/app.bsky.actor.getProfile',
            headers = request_header,
            params={"actor": parent_did}
            ).json()
        parent_profile_creation_date = parent_profile['createdAt']
        print('parent records profile was created at:\n', parent_profile_creation_date)
        
        mention_profile = requests.get('https://bsky.social/xrpc/app.bsky.actor.getProfile',
            headers = request_header,
            params={"actor": mention['author']['did']}
            ).json()
            
        mention_profile_creation_date = mention_profile['createdAt']
            
        if 'kinderpingui' in mention['record']['text'] or 'kinderpingui' in parent_profile['handle'] or 'kinderpingui' in mention_profile['handle']:
            print('kinderpigui found')
            kinderpingui = True
        else:
            kinderpingui = False
            
        if 'hourlyhoroscope' in parent_profile['handle'] or 'hourlyhoroscope' in mention_profile['handle']:
            print('bot got tagged')
            selftag = True
        else:
            selftag = False
            
        print('profile of persion tagging the bot was created at:\n', mention_profile_creation_date)

        user_signs = []
        
        for creation_date in [mention_profile_creation_date, parent_profile_creation_date]:
            # hope there is no index out of bounds but too lazy to check rn
            last_day_zodiac = list(zodiac_last_day.keys())[int(creation_date.split('-')[1].strip('0'))-1]
            birth_day_user  = int(creation_date.split('-')[2].split('T')[0])
            
            if birth_day_user > int(last_day_zodiac.split(' ')[1]):
                if int(creation_date.split('-')[1].strip('0')) >= len(list(zodiac_last_day.keys())):
                    next_zodiac = list(zodiac_last_day.keys())[0]
                else:
                    next_zodiac = list(zodiac_last_day.keys())[int(creation_date.split('-')[1].strip('0'))]
                user_signs.append(zodiac_last_day[next_zodiac])
            else:
                user_signs.append(zodiac_last_day[last_day_zodiac])
        
        mention_handle = mention['author']['handle'].split('.')[0]
        parent_record_handle = parent_profile['handle'].split('.')[0]
        compatibility = zodiac_compatibility[user_signs[0]][user_signs[1]]['compatibility'] if not kinderpingui else 100
        attributes = zodiac_compatibility[user_signs[0]][user_signs[1]]['attributes'][0]

        # reinitialize random seed
        random.seed(None)

        print(compatibility)
        if selftag:
            reply_text = 'all of the birds died in 1986 due to reagan killing them and replacing them with spies that are now watching us. the birds work for the bourgeoisie'
        else:
            if compatibility >= 66:
                fill_good = random.choice(['additionally', 'also', 'which matches because', 'luckily'])
                fill_bad = random.choice(['however', 'but be careful', 'beware though'])
                reply_text = random.choice(good_compatibility).format(mention_handle = mention_handle, parent_record_handle = parent_record_handle, compatibility = compatibility)
                just_words = random.choice(['take this as a sign of the stars.', 'the universe is on your side with this one!', 'this might just be your moment to shine, dont ruin it!', 'the stars are shining just for you, make the best of it!', 'take a chance, it might be worth this time!'])

            elif compatibility >= 33:
                fill_good = random.choice(['there is hope', 'try it', 'make it work'])
                fill_bad = random.choice(['sometimes its best not to engage with things', 'be careful', 'beware though', "accept what resonates, leave behind what doesn't"])
                reply_text = random.choice(medium_compatibility).format(mention_handle = mention_handle, parent_record_handle = parent_record_handle, compatibility = compatibility)
                just_words = random.choice(['some things are not pre determined. dont ruin this one!', 'if this one doesnt work out, there is no one else to blame but you.', 'good luck!', 'the universe seems to not care about this connection.'])

            else:
                fill_good = random.choice(['sadly', 'which is sad because', 'buckle up'])
                fill_bad = random.choice(['however', 'still', 'keep your head up because', 'there is hope since'])
                reply_text = random.choice(bad_compatibility).format(mention_handle = mention_handle, parent_record_handle = parent_record_handle, compatibility = compatibility)
                just_words = random.choice(['good luck next time.', 'take this as a sign of the stars.', 'the universe is on your side, and its trying to protect you.', 'keep calm, there is many fish in the sea!'])
            
            reply_text += ' ' + attributes.format(fill_good = fill_good, fill_bad = fill_bad)
            reply_text += ' ' + just_words
            
        reply_text = reply_text.lower()
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        resp = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers = request_header,
            json={
                "repo": session['did'],
                "collection": "app.bsky.feed.post",
                "record": {
                    "text": reply_text,
                    "reply": {
                        "parent": { 'cid': mention['cid'], 'uri': mention['uri'] },
                        "root"  : mention['record']['reply']['root']
                    },
                    "createdAt": now
                }
                }
        )
        print(f"posting reply to user {mention_handle}\n\n {resp.json()}")
        

    # mark notifs as seen
    resp = requests.post("https://bsky.social/xrpc/app.bsky.notification.updateSeen",
        headers = request_header,
        json={'seenAt': now})

    print(resp.status_code)
    resp.raise_for_status()