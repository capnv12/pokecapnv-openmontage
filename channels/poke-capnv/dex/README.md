# Dex data: how it runs

- `catalogue/` frozen card data. `../scripts/dex_catalogue_pull.py` (TCGdex, one JSON per set; skips sets already pulled, `--refresh` to re-pull), `../scripts/dex_names_pull.py` (`dex_names.json`: National numbers 1-1025, regions, rarity ladder), `overrides.json` (hand fixes per card id).
- `episodes/dex-NNN.json` one append-only log per episode, written at identification, approved at gate 1. Facts only (card id, finish, landing time); never verdicts. Mistakes after publishing go in `corrections`, never into the card line.
- `tiles/NNNN.png`, `tiles/trainer/<slug>.png` the filmed-card crops shown in the Pokédex row.
- `../scripts/dex_replay.py` rebuilds everything derived: `dex_state.json`, `dex_state_pokedex.csv`, `dex_state_trainers.csv`, `dex_history.csv`, `episodes.csv`, and prints the gate-1 table for the last episode (`--episode N` for another, `--upto N` to stop early).

```
.venv/bin/python channels/poke-capnv/scripts/dex_replay.py
```
Open the CSVs in Numbers; the JSON is for the render scripts.
