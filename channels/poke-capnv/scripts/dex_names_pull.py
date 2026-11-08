"""Build dex/catalogue/dex_names.json: National number -> English species name (PokéAPI),
plus the region ranges and the rarity ladder (plan sections 4.3 and 4.4). Data, not code."""
import json, os, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dex", "catalogue", "dex_names.json")
N = 1025

def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "poke-capnv-dex/1.0"}), timeout=30) as r:
                return json.load(r)
        except Exception:
            if i == tries - 1: raise
            time.sleep(1.5 * (i + 1))

def name(no):
    d = get(f"https://pokeapi.co/api/v2/pokemon-species/{no}/")
    en = next((n["name"] for n in d["names"] if n["language"]["name"] == "en"), d["name"].title())
    return str(no), en

REGIONS = [["kanto", 1, 151], ["johto", 152, 251], ["hoenn", 252, 386], ["sinnoh", 387, 493], ["unova", 494, 649],
           ["kalos", 650, 721], ["alola", 722, 809], ["galar", 810, 905], ["paldea", 906, 1025]]

# TCGdex rarity string -> rank (plan 4.3). Unknown strings make the replay stop, on purpose.
LADDER = {
    "Common": 1, "Uncommon": 2, "Rare": 3, "Holo Rare": 3, "Rare Holo": 3, "Amazing Rare": 6,
    "Double rare": 4, "Double Rare": 4, "ACE SPEC Rare": 5, "Illustration rare": 6, "Illustration Rare": 6,
    "Ultra Rare": 7, "Ultra rare": 7, "Special illustration rare": 8, "Special Illustration Rare": 8,
    "Hyper rare": 9, "Hyper Rare": 9, "Shiny rare": 6, "Shiny Ultra Rare": 7, "Black White Rare": 9, "Mega Hyper Rare": 9,
    "Rare Holo V": 4, "Rare Holo VMAX": 4, "Rare Holo VSTAR": 4, "Radiant Rare": 6, "Secret Rare": 9,
}
FINISHES = ["normal", "reverse", "pokeball", "masterball"]

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=8) as ex:
        names = dict(ex.map(name, range(1, N + 1)))
    doc = {"pulled": time.strftime("%Y-%m-%d"), "source": "https://pokeapi.co/api/v2/pokemon-species/{no}/",
           "total": N, "regions": REGIONS, "rarity_rank": LADDER, "finish_order": FINISHES, "names": names}
    json.dump(doc, open(OUT, "w"), ensure_ascii=False, indent=1)
    print("names:", len(names), names["1"], names["122"], names["1025"])
