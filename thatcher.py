from datetime import datetime, timezone
import random, requests

def check_on_maggie(session):
    
    random.seed(None)

    skeets = ["Still dead", "Rotting in hell", "Having her grave pissed on, cause shes dead",
            "as dead as you can be", "will never see any daylight again", 'margaret thatcher the cum snatcher mhh still rotting',
            "as dead as pokemon go", "Dead dead dead", 'consistently unliving', 'not snatching any cum anymore, cause shes dead',
            "Urine speaks louder than words, so piss on her grave when you get the chance", 
            "Holding hands with Ronald Reagan in the deepest Level of hell", 'resting in everything but peace, hopefully',
            "Dead or Alive? No she's dead", 'only thing she’s cutting are her ties with the living world - permanently',
            'five feet under with her stiff upper lip peaking out', 'currently taking a permanent nap at the mortlake crematorium',
            'dismantling the walfare state, in hell', 'destroying unions in the afterlife',
            'trying to bulldoze her way out of death - unsuccessfully', 'currently privatizing her way into the abyss',
            'still freezing hell with her cold heart', 'dead', 'not living', 'very much unalive',
            'thank god shes dead', 'today is a good day, she still hasnt come back', 'being eaten by worms in her grave']

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    post = {
        "$type": "app.bsky.feed.post",
        "text": random.choice(skeets).lower(),
        "createdAt": now,
        "langs": [ "th", "en-US" ]
    }

    print(post)

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