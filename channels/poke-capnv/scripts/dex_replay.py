"""Rebuild dex_state.json and the four CSVs by replaying dex/episodes/*.json in order (plan 4.5/4.6).
Verdicts are never stored; they are derived here. Prints the gate-1 table for the last (or --episode N) episode.
Usage: dex_replay.py [--dex-dir DIR] [--episode N] [--upto N]"""
import json, os, sys, csv, glob, re, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dex_catalogue import Catalogue

def load_episode(path):
    ep = json.load(open(path))
    fixes = {(c["pack"], c["pos"]): c for c in ep.get("corrections", [])}
    for p in ep["packs"]:
        for c in p["cards"]:
            k = (p["pack"], c["pos"])
            if k in fixes:
                c["id"] = fixes[k]["now"]
                if "finish" in fixes[k]: c["finish"] = fixes[k]["finish"]
    return ep

def replay(dex_dir, upto=None):
    cat = Catalogue(dex_dir)
    files = sorted(glob.glob(os.path.join(dex_dir, "episodes", "dex-*.json")), key=lambda f: int(re.search(r"dex-(\d+)", f).group(1)))
    state = {"built_from": [], "pokedex_total": 0, "trainer_total": 0, "upgrades": 0, "pokemon": {}, "trainers": [], "regions": {}}
    tindex = {}  # trainer name -> entry
    history, episodes, snapshots = [], [], {}
    for f in files:
        ep = load_episode(f); n = ep["episode"]
        if upto is not None and n > upto: break
        before = copy.deepcopy(state)
        counts = {"caught": 0, "upgraded": 0, "already": 0}
        for p in ep["packs"]:
            for c in sorted(p["cards"], key=lambda c: c["pos"]):
                if c.get("kind") == "basic_energy": continue
                card = cat.cards.get(c["id"])
                if card is None: raise SystemExit(f"episode {n} pack {p['pack']} pos {c['pos']}: card id {c['id']} not in catalogue")
                kind = cat.kind(card)
                if kind == "basic_energy": continue
                finish = c.get("finish", "normal"); fi = cat.finish_index(finish); rank = cat.rank(card)
                row = {"episode": n, "pack": p["pack"], "pos": c["pos"], "landing_s": c.get("landing_s", ""), "card_id": card["id"],
                       "set": card["set"], "set_number": card["number"], "name": card["name"], "kind": kind,
                       "rank": rank, "rarity": card.get("rarity") or "None", "finish": finish, "published_date": ep.get("published") or ""}
                if kind == "pokemon":
                    nos = cat.resolve_dex(card)
                    if not nos: raise SystemExit(f"episode {n}: {card['id']} {card['name']} has no National number; add it to overrides.json")
                    verdict = None
                    for i, no in enumerate(nos):
                        e = state["pokemon"].setdefault(str(no), {"name": cat.names[no], "region": cat.region(no), "current": None, "history": [],
                                                                   "first_caught": None, "last_upgraded": None, "times_seen": 0, "tile": ""})
                        cur = e["current"]
                        if cur is None: v = "caught"
                        elif (rank, fi) > (cur["rank"], cat.finish_index(cur["finish"])): v = "upgraded"
                        else: v = "already"
                        if i == 0: verdict = v
                        e["history"].append({"episode": n, "pack": p["pack"], "pos": c["pos"], "card": card["id"], "rank": rank, "finish": finish, "verdict": v})
                        e["times_seen"] += 1
                        if v == "caught": e["first_caught"] = n
                        if v in ("caught", "upgraded"):
                            e["current"] = {"card": card["id"], "rank": rank, "finish": finish, "episode": n}
                            if v == "upgraded": e["last_upgraded"] = n
                        tile = os.path.join("tiles", f"{no:04d}.png")
                        if os.path.exists(os.path.join(dex_dir, tile)): e["tile"] = tile
                    row["dex_no_or_t_no"] = nos[0]
                else:
                    key = card["name"]
                    e = tindex.get(key)
                    if e is None:
                        e = {"t_no": len(state["trainers"]) + 1, "name": key, "type": cat.trainer_type(card), "current": None, "history": [],
                             "first_caught": None, "last_upgraded": None, "times_seen": 0, "tile": ""}
                        state["trainers"].append(e); tindex[key] = e
                    cur = e["current"]
                    if cur is None: verdict = "caught"
                    elif (rank, fi) > (cur["rank"], cat.finish_index(cur["finish"])): verdict = "upgraded"
                    else: verdict = "already"
                    e["history"].append({"episode": n, "pack": p["pack"], "pos": c["pos"], "card": card["id"], "rank": rank, "finish": finish, "verdict": verdict})
                    e["times_seen"] += 1
                    if verdict == "caught": e["first_caught"] = n
                    if verdict in ("caught", "upgraded"):
                        e["current"] = {"card": card["id"], "rank": rank, "finish": finish, "episode": n}
                        if verdict == "upgraded": e["last_upgraded"] = n
                    slug = re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")
                    tile = os.path.join("tiles", "trainer", f"{slug}.png")
                    if os.path.exists(os.path.join(dex_dir, tile)): e["tile"] = tile
                    row["dex_no_or_t_no"] = f"T-{e['t_no']:03d}"
                row["verdict"] = verdict; counts[verdict] += 1
                if verdict == "upgraded": state["upgrades"] += 1
                history.append(row)
        state["pokedex_total"] = sum(1 for e in state["pokemon"].values() if e["current"])
        state["trainer_total"] = len(state["trainers"])
        state["regions"] = {name: {"have": sum(1 for k, e in state["pokemon"].items() if lo <= int(k) <= hi and e["current"]), "of": hi - lo + 1} for name, lo, hi in cat.regions}
        state["built_from"].append(os.path.splitext(os.path.basename(f))[0])
        episodes.append({"episode": n, "session": ep.get("session", ""), "filmed": ep.get("filmed", ""), "published": ep.get("published") or "",
                         "packs": len(ep["packs"]), **counts, "pokedex_total_after": state["pokedex_total"], "trainer_total_after": state["trainer_total"]})
        snapshots[n] = (before, copy.deepcopy(state))
    return cat, state, history, episodes, snapshots

def write_outputs(dex_dir, cat, state, history, episodes):
    json.dump(state, open(os.path.join(dex_dir, "dex_state.json"), "w"), ensure_ascii=False, indent=1)
    def w(name, header, rows):
        with open(os.path.join(dex_dir, name), "w", newline="", encoding="utf-8") as fh:
            wr = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore"); wr.writeheader(); wr.writerows(rows)
    rows = []
    for no in range(1, cat.total + 1):
        e = state["pokemon"].get(str(no)); cur = e["current"] if e else None
        rows.append({"no": no, "name": cat.names[no], "region": cat.region(no), "status": "caught" if cur else "empty",
                     "current_card": cur["card"] if cur else "", "current_rank": cur["rank"] if cur else "",
                     "current_rarity": (cat.cards[cur["card"]].get("rarity") or "None") if cur else "", "current_finish": cur["finish"] if cur else "",
                     "first_caught_episode": e["first_caught"] if e else "", "last_upgraded_episode": (e["last_upgraded"] or "") if e else "",
                     "times_seen": e["times_seen"] if e else 0, "tile": e["tile"] if e else ""})
    w("dex_state_pokedex.csv", ["no", "name", "region", "status", "current_card", "current_rank", "current_rarity", "current_finish", "first_caught_episode", "last_upgraded_episode", "times_seen", "tile"], rows)
    w("dex_state_trainers.csv", ["t_no", "name", "type", "current_card", "current_rank", "current_rarity", "first_caught_episode", "last_upgraded_episode", "times_seen"],
      [{"t_no": f"T-{e['t_no']:03d}", "name": e["name"], "type": e["type"], "current_card": e["current"]["card"], "current_rank": e["current"]["rank"],
        "current_rarity": cat.cards[e["current"]["card"]].get("rarity") or "None", "first_caught_episode": e["first_caught"],
        "last_upgraded_episode": e["last_upgraded"] or "", "times_seen": e["times_seen"]} for e in state["trainers"]])
    w("dex_history.csv", ["episode", "pack", "pos", "landing_s", "card_id", "set", "set_number", "name", "kind", "dex_no_or_t_no", "rank", "rarity", "finish", "verdict", "published_date"], history)
    w("episodes.csv", ["episode", "session", "filmed", "published", "packs", "caught", "upgraded", "already", "pokedex_total_after", "trainer_total_after"], episodes)

def gate1_table(cat, history, snapshots, n):
    before, after = snapshots[n]
    lines = [f"GATE 1  ·  Dex #{n}  ·  Pokédex {before['pokedex_total']} -> {after['pokedex_total']}  ·  Trainers {before['trainer_total']} -> {after['trainer_total']}  ·  Upgrades {before['upgrades']} -> {after['upgrades']}",
             f"{'pack':>4} {'pos':>3}  {'card':<12} {'name':<28} {'kind':<14} {'no':<6} {'rank':<4} {'rarity':<26} {'finish':<10} verdict"]
    for r in history:
        if r["episode"] != n: continue
        lines.append(f"{r['pack']:>4} {r['pos']:>3}  {r['card_id']:<12} {r['name'][:28]:<28} {r['kind']:<14} {str(r['dex_no_or_t_no']):<6} {r['rank']:<4} {r['rarity'][:26]:<26} {r['finish']:<10} {r['verdict'].upper()}")
    return "\n".join(lines)

if __name__ == "__main__":
    args = sys.argv[1:]
    def opt(name, default=None):
        if name in args: i = args.index(name); return args[i + 1]
        return default
    dex_dir = opt("--dex-dir", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dex"))
    upto = opt("--upto"); upto = int(upto) if upto else None
    cat, state, history, episodes, snapshots = replay(dex_dir, upto)
    write_outputs(dex_dir, cat, state, history, episodes)
    if episodes:
        n = int(opt("--episode", episodes[-1]["episode"]))
        print(gate1_table(cat, history, snapshots, n))
    print(f"\nreplayed {len(episodes)} episode(s): Pokédex {state['pokedex_total']} / {cat.total}, trainers {state['trainer_total']}, upgrades {state['upgrades']} -> {dex_dir}/dex_state.json + 4 CSVs")
