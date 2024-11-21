import requests
from datetime import datetime, timezone, timedelta


def repost_fus(session):

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat().replace("+00:00", "Z")

    request_header = {"Authorization": "Bearer " + session["accessJwt"]}

    # how ther fuyck do u search with boolean operators in this thing
    posts_fus = requests.get('https://bsky.social/xrpc/app.bsky.feed.searchPosts',
                headers = request_header,
                params={"q": "fus", 'since': one_hour_ago}
                ).json()

    #posts_fuss = requests.get('https://bsky.social/xrpc/app.bsky.feed.searchPosts',
    #            headers = request_header,
    #            params={"q": "fuss", 'since': one_hour_ago}
    #            ).json()

    posts_fusz = requests.get('https://bsky.social/xrpc/app.bsky.feed.searchPosts',
                headers = request_header,
                params={"q": "fuß", 'since': one_hour_ago}
                ).json()

    posts_Fusz = requests.get('https://bsky.social/xrpc/app.bsky.feed.searchPosts',
                headers = request_header,
                params={"q": "Fuß", 'since': one_hour_ago}
                ).json()

    posts = posts_fusz["posts"] + posts_Fusz["posts"] #  + posts_fuss["posts"] + posts_fus["posts"]

    unique_posts = []
    unique_str = ''

    for post in posts:

        if post['uri'] not in unique_str and not 'fusverbot' in post['author']['handle']:
            unique_posts.append(post)


    print(len(unique_posts))

    for post in unique_posts:

        record = {
            "$type": "app.bsky.feed.repost",
            "subject": {
                "uri": post['uri'],
                "cid": post['cid']
            },
            "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }

        resp = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers = request_header,
            json={
                "repo": session['did'],
                "collection": "app.bsky.feed.repost",
                "record": record
                }
        ).json()

        print(resp)