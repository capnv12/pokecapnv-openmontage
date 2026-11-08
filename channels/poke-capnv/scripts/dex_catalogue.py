"""Catalogue access for the Dex: card lookup, National-number resolution, rarity rank.
Data lives in dex/catalogue/ (pulled by dex_catalogue_pull.py / dex_names_pull.py); hand fixes in overrides.json."""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIC_ENERGY = re.compile(r"^(Basic )?(Grass|Fire|Water|Lightning|Psychic|Fighting|Darkness|Metal|Fairy|Dragon) Energy$")

class Catalogue:
    def __init__(self, dex_dir=None):
        self.dir = os.path.join(dex_dir or os.path.join(ROOT, "dex"), "catalogue")
        names = json.load(open(os.path.join(self.dir, "dex_names.json")))
        self.names = {int(k): v for k, v in names["names"].items()}
        self.total = names["total"]
        self.regions = [(r[0], r[1], r[2]) for r in names["regions"]]
        self.rank_of = names["rarity_rank"]
        self.finishes = names["finish_order"]
        self._rev = {v.lower(): k for k, v in self.names.items()}
        ov_path = os.path.join(self.dir, "overrides.json")
        self.overrides = json.load(open(ov_path)) if os.path.exists(ov_path) else {}
        self.sets, self.cards = {}, {}
        for f in sorted(glob.glob(os.path.join(self.dir, "*.json"))):
            if os.path.basename(f) in ("dex_names.json", "sets.json", "overrides.json"): continue
            d = json.load(open(f)); self.sets[d["set"]] = d["name"]
            for c in d["cards"]:
                c = dict(c); c.update(self.overrides.get(c["id"], {}))
                self.cards[c["id"]] = c

    def region(self, no):
        for name, lo, hi in self.regions:
            if lo <= no <= hi: return name
        return None

    def resolve_dex(self, card):
        if card.get("dex"): return list(card["dex"])
        n = card["name"]; s = n
        s = re.sub(r"^(Mega|Alolan|Galarian|Hisuian|Paldean|Origin Forme|Shadow|Dark|Light|Radiant|Shining) ", "", s)
        s = re.sub(r"^(Heat|Wash|Frost|Fan|Mow) Rotom", "Rotom", s)
        s = re.sub(r"^[A-Z][a-zA-Z' .]*?'s ", "", s)
        s = re.sub(r" ?(ex|EX|GX|V|VMAX|VSTAR|LEGEND|BREAK|Prime|LV\.X)$", "", s)
        if n.startswith("Mega"): s = re.sub(r" [XY]$", "", s)
        no = self._rev.get(s.lower())
        return [no] if no else []

    def kind(self, card):
        cat = card.get("category")
        if cat == "Pokemon": return "pokemon"
        if cat == "Trainer": return "trainer"
        if cat == "Energy": return "basic_energy" if BASIC_ENERGY.match(card["name"] or "") else "special_energy"
        raise ValueError(f"unknown category for {card['id']}: {cat}")

    def trainer_type(self, card):
        if card.get("category") == "Energy": return "Special Energy"
        return card.get("trainerType") or "Trainer"

    def rank(self, card):
        r = card.get("rarity")
        if r in (None, "None"): r = "None"
        if r == "Promo": return 4 if re.search(r" ex$", card["name"] or "") else 3
        if r not in self.rank_of: raise ValueError(f"rarity '{r}' on {card['id']} has no rank in dex_names.json; add it")
        return self.rank_of[r]

    def finish_index(self, finish):
        if finish not in self.finishes: raise ValueError(f"unknown finish '{finish}'; one of {self.finishes}")
        return self.finishes.index(finish)
