from datetime import datetime, timezone
import random, requests, json

def check_on_maggie(session):
    
    random.seed(None)

    skeets = ["Still dead", "Rotting in hell", "Having her grave pissed on, cause shes dead",
            "as dead as you can be", "will never see any daylight again", 'margaret thatcher the cum snatcher mhh still rotting',
            "as dead as pokemon go", "Dead dead dead", 'consistently unliving', 'not snatching any cum anymore, cause shes dead',
            "Urine speaks louder than words, so piss on her grave when you get the chance to", 
            "Holding hands with Ronald Reagan in the deepest Level of hell", 'resting in everything but peace, hopefully',
            "Dead or Alive? No she's dead", 'cutting taxes? no, cutting ties with the living world - permanently',
            'five feet under with her stiff upper lip peaking out', 'currently taking a permanent nap at the mortlake crematorium',
            'dismantling the walfare state, in hell', 'destroying unions in the afterlife',
            'trying to bulldoze her way out of death - unsuccessfully', 'currently privatizing her way into the abyss',
            'still freezing hell with her cold heart', 'dead', 'not living', 'very much unalive',
            'thank god shes dead', 'today is a good day, she still hasnt come back', 'being eaten by worms in her grave',
            'A spectre is haunting Europe - the spectre of maggie thatcher, because shes still dead', 
            'if i had a dime for every time maggie came back from the dead, i would have 0 dimes', 'wiping the floors of hell with her face',
            'the iron lady is melting - in the eternal flames of hell', 'roses are red, violets are blue and margaret thatcher is still dead',
            'dead, deader, deadest, margaret thatcher', 'doing penance for all of the miners lives she destroyed',
            'enjoying the free market of hell', 'trickling down to hell', 'shit talking about dead people is never okay, unless its margaret thatcher',
            'Eeny, meeny, miny, moe, maggies still 5 ft down below', 'rotating in her grave like a rotisserie chicken', 'discussing politics with mother teresa and ronald raegan',
            'at least she will never have to buy sunscreen again', 'taking golden showers in hellfire', 'expired', 'perished', 'gone', 'slain', 'she is no more',
            'chilling with churchill', 'forever asleep', 'buried', 'bereft of life', 'still pushing up the daisies']

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