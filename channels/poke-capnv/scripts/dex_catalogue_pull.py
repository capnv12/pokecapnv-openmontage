"""Pull the Mega Evolution-era card catalogue from TCGdex and freeze it under dex/catalogue/.
One JSON per set, in the plan's record shape (section 4.6). Re-run only on purpose: a set file
that already exists is skipped unless --refresh is given."""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(ROOT, "dex", "catalogue")
API = "https://api.tcgdex.net/v2/en"
SERIES = "me"

def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "poke-capnv-dex/1.0"}), timeout=30) as r:
                return json.load(r)
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(1.5 * (i + 1))

def record(c):
    v = c.get("variants") or {}
    variants = [k for k in ("normal", "reverse", "holo", "firstEdition", "wPromo") if v.get(k)]
    return {
        "id": c["id"], "set": c["set"]["id"], "number": c.get("localId"), "name": c.get("name"),
        "category": c.get("category"), "dex": c.get("dexId") or [], "rarity": c.get("rarity"),
        "trainerType": c.get("trainerType"), "energyType": c.get("energyType"),
        "stage": c.get("stage"), "suffix": c.get("suffix"), "evolveFrom": c.get("evolveFrom"),
        "regulationMark": c.get("regulationMark"), "illustrator": c.get("illustrator"),
        "variants": variants, "image": c.get("image"),
    }

def pull_set(sid, refresh=False):
    out = os.path.join(CAT, f"{sid}.json")
    if os.path.exists(out) and not refresh:
        print(f"{sid}: exists, skipped"); return
    meta = get(f"{API}/sets/{sid}")
    ids = [c["id"] for c in meta["cards"]]
    with ThreadPoolExecutor(max_workers=8) as ex:
        cards = list(ex.map(lambda i: record(get(f"{API}/cards/{i}")), ids))
    doc = {"set": sid, "name": meta["name"], "abbreviation": (meta.get("abbreviation") or {}).get("official"),
           "releaseDate": meta.get("releaseDate"), "cardCount": meta.get("cardCount"),
           "pulled": time.strftime("%Y-%m-%d"), "source": f"{API}/sets/{sid}", "cards": cards}
    json.dump(doc, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"{sid}: {len(cards)} cards -> {out}")

if __name__ == "__main__":
    refresh = "--refresh" in sys.argv
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    series = get(f"{API}/series/{SERIES}")
    sets = want or [s["id"] for s in series["sets"]]
    for sid in sets:
        pull_set(sid, refresh)
    # index of sets
    json.dump({"series": SERIES, "pulled": time.strftime("%Y-%m-%d"),
               "sets": [{"id": s["id"], "name": s["name"], "cardCount": s["cardCount"]} for s in series["sets"]]},
              open(os.path.join(CAT, "sets.json"), "w"), ensure_ascii=False, indent=1)
    print("done")
