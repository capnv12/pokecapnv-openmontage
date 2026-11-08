# poke.capnv plan: the Dex format ("Caught / Already caught / Upgraded")

Status: APPROVED 2026-11-08. Format settled by the user ("I like this. We can create a virtual dex. Each pokemon is added to the dex, also support cards have to be added. When a higher rarity appears we change what is already there in the dex. This is settled."), and the seven open decisions in section 12 answered the same day (answers recorded there). Section 13 lists the calls I made; override any of them at any gate.

Scope: every short filmed from now on. About 30 drum shorts are still unpublished and keep shipping daily, unchanged. The first Dex episode is a pilot filmed and published next week (week of 2026-11-09), in the middle of the drum run; its Dex log is Dex #1 and the run continues from that state whenever the next Dex sessions are filmed. The packs are from several Mega Evolution-era sets (user, 2026-11-08); the first identification pass confirms each set's pack structure and rarity marks against section 4.3 before anything is scripted.

Everything in `starting-prompt.md` still applies (VO voice and processing, word-level sync, captions, safe area, audio rules, banned lines, constraints) unless a line here overrides it. Overrides are marked **OVERRIDE**. `plan-draw-08-onward.md` (two-pack drum format) is superseded for new recordings.

Evidence this plan rests on: `analytics-checks.md` (Draws #1-#15: the spoken hook that names the result keeps viewers; vague hooks lose them; nothing after the best card is watched), `research/big-names-shorts-2026-11-07.md` (big channels run 40-80 s, every one has a standing device, premise in the first 3 s, abrupt end on the card), `research/cross-niche-openings-2026-11-07.md` (a premise at 0 s and a stake that is not luck; hands-only works; counters hold viewers across episodes), `research/funny-openings-2026-11-07.md` (in this niche the fun lives in the voice's verdicts, not in devices). Originality check: `research/dex-format-check-2026-11-08.md`.

---

## 0. Originality (checked 2026-11-08, `research/dex-format-check-2026-11-08.md`)

Twenty YouTube searches, the latest 60 videos and 60 Shorts of 16 big channels plus 23 channels surfaced by the searches, titles and counts only. Nobody gives each card a verdict, nobody has an on-screen Dex that fills in, nobody ends a run when a set's page completes. The broad idea "fill a Pokédex from packs" exists on seven tiny channels (the largest has 5,300 subscribers and 58 views on its best video; the most active, Pokédex Collector, started August 2026 and tops out at 505 views). Big channels do species-dex content only as binder projects built from bought and traded singles (Deep Pocket Monster, Joel's Gaming Adventures "Pokedex Binder upgrades") or one-off stunts (Leonhart, 151 packs for 151 Pokémon, one video). TikTok could not be checked by tool; search #pokedexchallenge, #livingdex, #packdex in the app once before launch. Conclusion: the mechanic is ours; the phrases "Pokédex challenge" and "catch them all" are not, so titles lead with the verdict words and the Dex number, not with those phrases.

## 1. Intent

A recurring show where the tension of every pack comes from one real collector goal that does not need owning anything: register every Pokémon and every trainer card once, in a virtual Dex, from pack openings. A card's worth to the run is whether it registers something new or upgrades an entry, not its rarity. That flips what a good pack is, every viewer understands it from the games without explanation, and the voice gets a personality from its verdicts instead of from a role.

## 2. Goals, non-goals, anti-goals

Goals
- Every card flipped gets an instant, two-word verdict the viewer can predict and argue with.
- The run has a visible score and a finish line (a set's Dex page complete).
- Hits still get their moment, but only when they register or upgrade; an "already caught" EX is the show's signature deadpan beat.
- Same production cost as today: hands, mat, AI voice, 2-3 packs, 45-65 s.

Non-goals
- No prices, anywhere (user, 2026-10-28 and 2026-11-07).
- No binder, no kept cards, nothing physical carried between episodes (user, 2026-11-08). The Dex is graphics only.
- No question asked to the audience in the video. The comments prompt lives in the caption.
- No drum, no balls. **OVERRIDE** of the drum beats in `starting-prompt.md`.
- No face, no official Pokémon artwork, sprites, silhouettes, logos or game audio in the Dex graphics. Dex tiles are crops of the user's own filmed cards. Cut-away footage follows decision 9 in section 12.

Anti-goals (things that would make it fail even if built correctly)
- Bookkeeping feel: long lists, numbers read out on every card, a spreadsheet on screen. The counter is seen, and spoken only at the start and the end.
- A faked verdict or a reordered pack to manufacture drama. The Dex is only interesting if it is honest and the order is the filmed order.
- The voice performing a character. It states verdicts the way a collector thinks them: fast, certain, a little unfair.
- Padding to a length. Floor and ceiling are met with card time, never with holds.

## 3. Constraints

- Hands only, AI voice (ElevenLabs voice g3gYSFX4zMCH0soBrygt, eleven_v3, settings in `starting-prompt.md`).
- 2 packs per episode; 3 when the first two register nothing new (section 6).
- 4K HEVC HLG source, Mac M1 8 GB, ffmpeg without zscale, paid generation cap $2 per video.
- Daily publishing, YouTube Shorts and TikTok, same file.
- Only original or licensed audio.

## 4. The Dex: what is in it, and the rules

### 4.1 Entries

It is a **Pokédex**, not a set checklist (user, 2026-11-08: "The plan was pokedex, not set/masterset!"). Pokémon are ordered and counted by National Pokédex number, the number printed on every Pokémon card ("NO. 0768 Hard Scale Pokémon"). Sets do not matter to the Dex; they only matter to the set-hook line in the VO.

| Kind | One entry per | Examples | Notes |
|---|---|---|---|
| Pokémon | National Pokédex number, across all sets | No. 0025 Pikachu; No. 0006 Charizard (plain, ex, Mega ex, Tera ex are all entry 0006) | Forms share the number, as in the games: Hisuian Zoroark is entry 0571 and can Upgrade it but never adds an entry (my call). Evolutions are separate numbers. |
| Trainer | card name, in a separate Trainer Dex, numbered T-001, T-002... in order of first appearance | Boss's Orders; Rare Candy; Artazon | Supporter, Item, Tool, Stadium all count. No predefined list: the Trainer Dex only grows. A full-art Boss's Orders upgrades the Boss's Orders entry and keeps its T-number. Counted and shown separately from the Pokédex total. |
| Special Energy | card name, in the Trainer Dex, same numbering | Jet Energy; Neo Upper Energy | Counted as "support cards" per the user. |
| Basic Energy | not in any Dex | Fire Energy | My call: nine entries that every first pack would fill mean nothing. They get no verdict and no stamp; the card gets a tick and ~0.3 s. |

One Pokédex for the whole channel, 1025 numbers. A Pikachu from Surging Sparks and a Pikachu from Phantasmal Flames are the same entry; the higher-rarity one is the one displayed. Progress is read by region (section 4.4); there is no "set complete" ending.

### 4.2 Verdicts

| Verdict | When | Spoken | What happens on screen |
|---|---|---|---|
| **Caught** | first time this entry appears in the run | "Caught. {Name}." | Green stamp, register ding, the card's crop flies into its Dex tile, counter +1 |
| **Already caught** | entry exists and this card is not higher on the ladder | "Already caught." (consecutive ones may be shortened to "Already.") | Grey stamp, soft tick, nothing else |
| **Upgraded** | entry exists and this card is higher on the ladder | "Upgraded. {Name}, {rarity}." | Gold stamp, shimmer, the tile swaps image, counter unchanged, upgrade count +1 |

The verdict words are the catchphrase of the show and must never vary once chosen (section 12, Q3 offers alternatives).

### 4.3 The rarity ladder (what counts as "higher")

Printed rarity decides. Finish breaks ties within the same printed rarity. Scarlet & Violet era:

| Rank | Printed rarity | Marks |
|---|---|---|
| 1 | Common | one black circle |
| 2 | Uncommon | black diamond |
| 3 | Rare (holo) | black star |
| 4 | Double Rare (ex) | two black stars |
| 5 | ACE SPEC Rare | pink star, trainers only |
| 6 | Illustration Rare | one gold star |
| 7 | Ultra Rare (full-art ex, full-art Supporter) | two silver stars |
| 8 | Special Illustration Rare | two gold stars |
| 9 | Hyper Rare (gold) | three gold stars |

Finish order inside one rank: plain < reverse holo < Poké Ball pattern < Master Ball pattern. So a Master Ball Pikachu upgrades a reverse Pikachu, but a Pikachu ex (rank 4) upgrades any Master Ball Pikachu (rank 1). A pattern variant is called out in the VO when it upgrades ("Upgraded. Pikachu, Master Ball."). Older eras (if a pack from before Scarlet & Violet turns up) map onto the same ranks: V / VMAX / VSTAR = rank 4, full-art = rank 7, rainbow/gold = rank 9, Amazing Rare = rank 6.

### 4.4 Counters and finish lines

- Big number: Pokémon registered out of 1025 ("DEX 134 / 1025"). Shown on the persistent chip, spoken at the start of every episode and at the end when it changed.
- Region: the region of the card on screen, with its count ("ALOLA 12 / 88"). Regions by National number: Kanto 1-151, Johto 152-251, Hoenn 252-386, Sinnoh 387-493, Unova 494-649, Kalos 650-721, Alola 722-809, Galar 810-905, Paldea 906-1025. Shown on the chip under the total; spoken only at a milestone.
- Milestones: a region reaching 25%, 50%, 75% and 100% is an episode's ending beat and its title ("Dex #41: Alola, half full."). The run has no finish line; a Pokédex never closes, and that is the point of the show.
- Trainer Dex: a small count ("TRAINERS 22"), shown when a trainer card is on screen and on the end frame.
- Upgrades: a small running count ("17 upgrades"), shown when an upgrade happens and on the end frame.

### 4.5 State and integrity

- The Dex is a replayable log, not a single edited file: `channels/poke-capnv/dex/episodes/dex-NNN.json` holds one episode's cards in flipped order (pack, position, card set-number, name, kind, rank, finish, tile path). `dex_state.json` is always rebuilt by replaying the logs in episode order. That lets episodes N+1 and N+2 be produced while N is still a draft (their verdicts are provisional on N's approved log) and makes any correction a replay, never a hand edit.
- A log becomes final when its episode is published. Correcting a card in a published episode is allowed only by appending a correction record (never by rewriting the log); the next episode's VO acknowledges it in one line if the counter moved.
- Identification is done by me from the 4K frames on the 0.2 s landing grid, exactly as today, with the card database (TCGdex or pokemontcg.io, chosen at build time) supplying name, kind, printed rarity and the set's entry list. The user approves the identification-plus-verdict table at gate 1. A misread caught at gate 1 costs nothing; one caught after publishing is a correction record.
- Packs are published in the exact order they were filmed (section 8). The hook (beat 1) is a flash-forward and is excepted from the order rule: it may show a card from pack B or C before pack A plays. The body never reorders.
- A disputed identification is resolved before scripting, never after.

### 4.6 Data files (what is stored where)

Everything lives in `channels/poke-capnv/dex/`, plain JSON, committed to the repo, so the whole run can be rebuilt from the files alone.

```
channels/poke-capnv/dex/
  catalogue/
    me01.json, me02.json, ...      one file per set, pulled from TCGdex and frozen (never re-fetched silently)
    dex_names.json                 National number -> species name, 1..1025, plus region ranges
  episodes/
    dex-001.json                   one append-only log per episode: every card flipped, in order
    dex-002.json
  tiles/
    0768.png, 0976.png, ...        the filmed-card crop shown in the Pokédex row for that number
    trainer/boss-s-orders.png      same for the Trainer Dex
  dex_state.json                   DERIVED: rebuilt by replaying episodes/ in order; never edited by hand
```

Catalogue record (one card): `{"id": "me01-049", "set": "me01", "number": "049", "name": "Golisopod", "category": "Pokemon", "dex": [768], "rarity": "Rare", "variants": ["normal", "reverse"]}`. Trainers carry `"category": "Trainer"` and `"trainerType"`; special energy `"category": "Energy", "energyType": "Special"`.

Episode log (`episodes/dex-014.json`):
```
{ "episode": 14, "filmed": "2026-11-12", "session": "S03", "published": null,
  "packs": [
    { "pack": 1, "set": "me01", "cards": [
      { "pos": 1,  "id": "me01-energy-fire", "kind": "basic_energy" },
      { "pos": 2,  "id": "me01-049", "finish": "normal", "landing_s": 7.40 },
      { "pos": 10, "id": "me01-120", "finish": "normal", "landing_s": 19.86 },
      ...
    ]},
    { "pack": 2, ... }
  ],
  "corrections": [] }
```
The log records only facts from the footage: which card, which finish, when it landed. It never stores the verdict. Verdicts are computed at replay time from the state before that card, so a correction anywhere in the run re-derives every verdict after it.

State (`dex_state.json`, derived). Every Pokédex number keeps its full history, not just the card on display:
```
{ "built_from": ["dex-001", ..., "dex-014"], "pokedex_total": 134, "trainer_total": 22, "upgrades": 17,
  "pokemon": {
    "768": { "name": "Golisopod", "region": "alola",
             "current": { "card": "me01-049", "rank": 3, "finish": "normal", "episode": 14 },
             "history": [
               { "episode": 14, "pack": 1, "pos": 2, "card": "me01-049", "rank": 3, "finish": "normal", "verdict": "caught" },
               { "episode": 19, "pack": 2, "pos": 6, "card": "me02-031", "rank": 1, "finish": "reverse", "verdict": "already" },
               { "episode": 27, "pack": 1, "pos": 10, "card": "me03-077", "rank": 6, "finish": "normal", "verdict": "upgraded" } ],
             "first_caught": 14, "last_upgraded": 27, "times_seen": 3, "tile": "tiles/0768.png" } },
  "trainers": [
    { "t_no": 1, "name": "Boss's Orders", "type": "Supporter", "current": {...}, "history": [...], "first_caught": 1, "times_seen": 4 },
    { "t_no": 2, "name": "Rare Candy", "type": "Item", ... } ],
  "regions": { "alola": { "have": 13, "of": 88 }, ... } }
```

Worked Trainer Dex example (card ids illustrative; the real ids come from the catalogue at identification). Every trainer kind and special energy goes into the same list, same numbering, told apart only by the `type` column:
```
"trainers": [
  { "t_no": 1, "name": "Boss's Orders", "type": "Supporter",
    "current": { "card": "me01-131", "rank": 2, "rarity": "Uncommon", "finish": "normal", "episode": 1 },
    "history": [ { "episode": 1, "pack": 1, "pos": 5, "card": "me01-131", "rank": 2, "finish": "normal", "verdict": "caught" } ],
    "first_caught": 1, "last_upgraded": null, "times_seen": 1 },
  { "t_no": 2, "name": "Rare Candy", "type": "Item",
    "current": { "card": "me01-140", "rank": 2, "rarity": "Uncommon", "finish": "reverse", "episode": 3 },
    "history": [ { "episode": 1, "pack": 2, "pos": 3, "card": "me01-140", "rank": 2, "finish": "normal",  "verdict": "caught" },
                 { "episode": 3, "pack": 1, "pos": 8, "card": "me01-140", "rank": 2, "finish": "reverse", "verdict": "upgraded" } ],
    "first_caught": 1, "last_upgraded": 3, "times_seen": 2 },
  { "t_no": 3, "name": "Rescue Board", "type": "Tool",
    "current": { "card": "me01-144", "rank": 2, "rarity": "Uncommon", "finish": "normal", "episode": 2 },
    "history": [ { "episode": 2, "pack": 1, "pos": 4, "card": "me01-144", "rank": 2, "finish": "normal", "verdict": "caught" } ],
    "first_caught": 2, "last_upgraded": null, "times_seen": 1 },
  { "t_no": 4, "name": "Artazon", "type": "Stadium",
    "current": { "card": "me01-148", "rank": 2, "rarity": "Uncommon", "finish": "normal", "episode": 2 },
    "history": [ { "episode": 2, "pack": 2, "pos": 6, "card": "me01-148", "rank": 2, "finish": "normal", "verdict": "caught" },
                 { "episode": 5, "pack": 1, "pos": 7, "card": "me01-148", "rank": 2, "finish": "normal", "verdict": "already" } ],
    "first_caught": 2, "last_upgraded": null, "times_seen": 2 },
  { "t_no": 5, "name": "Jet Energy", "type": "Special Energy",
    "current": { "card": "me01-152", "rank": 2, "rarity": "Uncommon", "finish": "normal", "episode": 4 },
    "history": [ { "episode": 4, "pack": 2, "pos": 9, "card": "me01-152", "rank": 2, "finish": "normal", "verdict": "caught" } ],
    "first_caught": 4, "last_upgraded": null, "times_seen": 1 },
  { "t_no": 6, "name": "Lillie's Determination", "type": "Supporter",
    "current": { "card": "me01-175", "rank": 7, "rarity": "Ultra Rare", "finish": "normal", "episode": 9 },
    "history": [ { "episode": 6, "pack": 1, "pos": 5,  "card": "me01-133", "rank": 2, "finish": "normal", "verdict": "caught" },
                 { "episode": 9, "pack": 2, "pos": 11, "card": "me01-175", "rank": 7, "finish": "normal", "verdict": "upgraded" } ],
    "first_caught": 6, "last_upgraded": 9, "times_seen": 2 }
]
```
Reading it: Rare Candy was caught as a plain uncommon, then its reverse holo upgraded it (same rank, finish breaks the tie). Artazon's second copy did nothing. Lillie's Determination was caught as an uncommon Supporter and upgraded by its full-art Ultra Rare print; it keeps T-006. Basic Energy never appears here.

The same six rows in `dex_state_trainers.csv`:
```
t_no,name,type,current_card,current_rank,current_rarity,current_finish,first_caught_episode,last_upgraded_episode,times_seen
1,Boss's Orders,Supporter,me01-131,2,Uncommon,normal,1,,1
2,Rare Candy,Item,me01-140,2,Uncommon,reverse,1,3,2
3,Rescue Board,Tool,me01-144,2,Uncommon,normal,2,,1
4,Artazon,Stadium,me01-148,2,Uncommon,normal,2,,2
5,Jet Energy,Special Energy,me01-152,2,Uncommon,normal,4,,1
6,Lillie's Determination,Supporter,me01-175,7,Ultra Rare,normal,6,9,2
```
and their sightings in `dex_history.csv` (one line per flip, verdict included):
```
episode,pack,pos,landing_s,card_id,set,set_number,name,kind,dex_no_or_t_no,rank,rarity,finish,verdict,published_date
1,2,3,11.20,me01-140,me01,140,Rare Candy,Item,T-002,2,Uncommon,normal,caught,2026-11-13
3,1,8,16.04,me01-140,me01,140,Rare Candy,Item,T-002,2,Uncommon,reverse,upgraded,2026-11-15
5,1,7,14.90,me01-148,me01,148,Artazon,Stadium,T-004,2,Uncommon,normal,already,2026-11-17
9,2,11,49.33,me01-175,me01,175,Lillie's Determination,Supporter,T-006,7,Ultra Rare,normal,upgraded,2026-11-21
```

The JSON and the CSVs carry the same information, nothing is dropped in either direction: JSON for the scripts, CSV for the user to open and look at. The Trainer Dex has no predefined numbering. Supporters, Items, Tools, Stadiums and Special Energy go into one list in the order they first appear in the run: the first trainer ever caught is T-001, the next new one T-002, and so on. A trainer's number never changes; a higher-rarity print of the same name upgrades the entry in place (same T-number). In the video the Trainer row therefore always shows the tail of the list, with the new entry appended at the end ("T-021, T-022, T-023 NEW"), and the header reads "TRAINER DEX 23".

CSV, always, next to the JSON. `scripts/dex_replay.py` writes both formats from the same replay, so they can never disagree:
- `dex_state_pokedex.csv`: one row per National number 1-1025: `no, name, region, status (empty/caught), current_card, current_rank, current_rarity, current_finish, first_caught_episode, last_upgraded_episode, times_seen, tile`.
- `dex_state_trainers.csv`: one row per trainer in first-appearance order: `t_no, name, type, current_card, current_rank, current_rarity, first_caught_episode, last_upgraded_episode, times_seen`.
- `dex_history.csv`: one row per card ever flipped, the complete past: `episode, pack, pos, landing_s, card_id, set, set_number, name, kind, dex_no_or_t_no, rank, rarity, finish, verdict, published_date`.
- `episodes.csv`: one row per episode: `episode, session, filmed, published, packs, caught, upgraded, already, pokedex_total_after, trainer_total_after`.
UTF-8, comma-separated, header row, one file per table, openable in Numbers or Excel without any setup.

Rules
- Only `episodes/*.json` and `tiles/` are hand-touched (by the identification pass, approved at gate 1). `dex_state.json` and the four CSVs are regenerated by `scripts/dex_replay.py` every time, and the gate-1 table is printed from the diff between the state before and after the new episode.
- A log is final when `"published"` gets a date. After that, a mistake is fixed by appending to `"corrections"` (`{"pack": 2, "pos": 7, "was": "me01-052", "now": "me01-053", "reason": "misread set number", "date": ...}`), never by editing the card line, so the published videos and the files always agree about what was claimed and when.
- Episodes produced ahead of publishing replay against the previous episode's log whether or not it is published yet; if an earlier episode changes, the later ones are re-verified before their render.
- The rarity ladder (section 4.3) and the region ranges are data in `catalogue/dex_names.json`, not code, so a new era or a new region is a data edit.

## 5. The episode, second by second

Target 58-63 s. Floor 61.0 s stays while the user keeps the TikTok Creator Rewards floor (section 12, Q1); ceiling 65 s. 30 fps. Pack A = the first pack in filmed order; pack B = the second. Each Scarlet & Violet pack is one energy (card 1, no verdict) plus ten cards (cards 2-11).

| Beat | Time | Screen | VO | Audio |
|---|---|---|---|---|
| 1. Hook | 0.0-2.8 | Moving footage of the episode's key card landing (the biggest Caught/Upgraded, or the "already caught" hit), 0.5x, push-in 100->112%, full screen, no stamp yet. Caption below the card. | Voice at 0.0 s, done by 2.6 s. Names the result (section 7). | Silence under the voice, register ding or flat tick on the cut, matching the verdict the hook describes. |
| 2. Today's packs | 2.8-5.5 | **Entrance first:** the pack comes up into frame from below, face to camera (the user's hand, as in every Draw), and stops centred. The moment it is still, the Pokédex scans it: a yellow scan beam sweeps the pack top to bottom (0.45 s), the scanned part lights faintly, a yellow rim pulses once on completion. The pack's own frame then shrinks out of the footage into slot 1 of the line-up band (the same move a card makes into its Pokédex tile), the band and header fade in under it, and the remaining packs slide in from the right. Mock-ups: `dex/mockups/v6/entrance_storyboard.jpg`, `entrance_scan_2packs.mp4`, `entrance_scan_3packs.mp4`. No flip, no back of the pack shown: the reveal is the scan, not a turn. **Then the line-up:** built from each pack's own pack-front frame (no extra filming): one small framed still per pack, "PACK 1 · set name" under each, the pack about to be opened gets the yellow frame; header line "POKÉDEX 134 / 1025" left and "TODAY 2 PACKS" right in yellow. Fades as the tear starts. When pack 2 (or 3) is reached the band returns for 1 s with that pack framed. Mock-ups: `dex/mockups/v5/lineup_storyboard.jpg`, `lineup_2packs.mp4`, `lineup_3packs.mp4`. | "Dex at one thirty-four. {Set}, {true four-word set hook}." (two or three packs named in one breath when they differ) | Bed in. |
| 3. Pack A tear + cards 1-9 | 5.5-20.0 | Tear at 3-4x. Energy at 0.3 s, tick only. Cards 2-9: stamp on each landing, 0.8-1.2 s per card (Caught/Upgraded 1.2-1.6 s, Already 0.7-0.9 s). | Verdict per card, name on Caught/Upgraded only. A run of Already: "Already caught. Already. Already." | Ding / tick / shimmer per stamp, under the VO per the ducking rules. |
| 4. Pack A cards 10-11 | 20.0-26.0 | Riser, push-in 100->115%, reveal on impact. Hit tag only if rank 4+. Stamp after the reveal, not before. | If the hit registers: "Card ten- {reaction}. {Name} EX. Caught." If it does not: "{Name} EX. ... Already caught." flat, [sighs] or deadpan. Regular holo: "Rare slot, {card}. Caught/Already." | Music drops before a rank 4+ reveal; dud sting on a flat Already. |
| 5. Pack A total | 26.0-27.5 | Dex chip ticks "+3", the three new tiles glow once. | None, or "Three new." | Tick-up SFX. |
| 6. Pack B tear + cards 1-9 | 27.5-44.0 | As beat 3, 0.1 s slower per card so every card is readable. | As beat 3. | As beat 3. |
| 7. Pack B cards 10-11 | 44.0-54.0 | As beat 4, with the episode's key beat landing here when pack B holds it (slow-mo build to 0.2x, freeze, glow, hold for the line). | Hit line as in the script recipe: reaction, name, rarity, verdict, ONE verified art detail only on an Upgraded/Caught hit. | Impact + shimmer, or dud sting. |
| 8. End | 54.0-61.0 | Dex chip ticks to the new total; the Pokédex strip (section 9) shows the episode's new tiles glowing once in number order; hold the key card 2 s with its stamp; hard cut to black on the last tick. No outro, no CTA, no loop. | "Dex at one thirty-nine." (only if it changed) or nothing. | Bed out on the cut. |

Rules
- The key card goes in pack B's slot when the filmed order allows it (it is either in pack A or pack B; if it is in pack A, the episode keeps the filmed order and the hook promises "the first pack", so the second pack's job is the counter).
- With three packs (user's choice for that video), beats 6-7 repeat for pack C at 0.7-0.9 s per card and the ceiling moves to 70 s. **OVERRIDE** of the 65 s ceiling in that case.
- Nothing is placed after the key card except the counter tick and the 2 s hold.
- Fill toward the floor with cut-aways (section 5.1), never with longer holds or slower cards beyond the per-card range. A short episode is never shipped under the floor while the floor exists.

### 5.1 Cut-aways (how the time to 61 s is filled, and where the jokes live)

A cut-away is a 1-2.5 s insert over the footage, with the VO continuing or a one-line joke, the way the big channels cut to a reaction or a meme. They do two jobs: fill a two-pack episode to the floor without stretching anything, and give the voice its comic timing on duds.

Where a cut-away may go, and where never
- After a hit-slot card that is "Already caught": the signature deadpan beat. The reveal, the flat verdict, then 1-2 s of cut-away (a bored or unimpressed reaction clip), then the next pack.
- During a run of three or more "Already caught" in a row: one cut-away replaces the middle of the run; the stamps still tick under it.
- Before pack B's or C's rare slots, as a tension beat: 1-1.5 s, only when the episode is under the floor.
- Beat 2, the line-up, may hold a 1 s cut-away when the VO names the sets.
- Never over a Caught or Upgraded animation, never inside the hook, never two in a row, never on the end frame.

Budget per episode: at most two cut-aways, and only where there is a joke or a beat to land (user, 2026-11-08: "don't force them. 3 in a short sound too much"). Zero is fine. A cut-away is never placed just to reach a length. The 61 s floor therefore becomes a target, not a gate: an episode whose packs and natural cut-aways come to 52 s ships at 52 s, and the publish notes say so (that video alone may miss TikTok Creator Rewards). The duration gate now checks only the ceiling (65 s, 70 s with three packs) and that nothing was stretched. **OVERRIDE** of the floor rule in section 5 and of decisions 1 and 11.

Two kinds, one library, reused across every episode so nothing is refilmed
- Reaction and meme clips: faceless or generic (hands, animals, objects, cartoons where licensed). Tagged by feeling: `bored`, `again`, `nothing`, `waiting`, `suspicious`, `jackpot`, `upgrade`, `tiny-win`. Sourced only under a written licence (decision 9, option (a) chosen): Pexels, Pixabay, Mixkit or a paid library; no anime, game footage or official artwork; every file in the library carries its source URL and licence in `dex/broll/library.csv`.
- Pokémon-themed cut-aways built from the channel's own footage: a slow push on a card's illustration, the card's printed Pokédex line ("NO. 0768 Hard Scale Pokémon") read by the voice, this run's pulls fanned, the Pokédex row scrolling through a region. Zero filming; they come from frames already in the episodes.

The voice over a cut-away: one short line at most, in the script recipe's register ("Lovely. Useless." / "Third Artazon. The stadium is complete, nobody asked."), never a tally, never a price. Cut-aways are scripted at gate 2 like any line, with the clip named from the library, and the user sees them in the low-res draft.

## 6. Pack count and sessions

- 2 or 3 packs per episode, the user's call per video, told with the file (section 8). 60 packs = 20-30 episodes. A third pack is never added by me for length; length comes from cut-aways (section 5.1).
- A session is however many packs the user films in one sitting.
- Packs are opened and published in filmed order. No pairing, no bank, no re-ordering (section 4.5). **OVERRIDE** of section 4 of `plan-draw-08-onward.md`.
- Mixed sets are fine: the Dex does not care which set a card is from; a Pokémon seen in set A is "already caught" when it appears in set B.

## 7. The voice

Persona unchanged: first person, past tense, spoken not read, one or two delivery tags per line, no filler, banned lines from `starting-prompt.md` still banned. New rules:

Hook line (beat 1), rotated every episode, 3-4 candidates at gate 2
- Must name the result: the new total, the biggest new entry, the upgrade, or the deadpan beat. Never a question, never "two packs" alone, never a negative.
- Pool to start from: "Dex at one thirty-four, and the second pack had an upgrade." / "Umbreon EX came out of the second pack. Already caught." / "Seven new ones. One of them is a Charizard." / "The first pack registered nothing. The second one registered this." / "Prismatic Evolutions, three left. One came out at card ten."

Verdict lines
- Caught: "[upbeat] Caught. Sprigatito." Name every Caught card. The name is the sync anchor for that card.
- Already caught: flat, short, no name. Three or more in a row: "Already caught. Already. Already." then silence until the next Caught (the stamps and ticks carry the rest).
- Upgraded: "[excited] Upgraded. Pikachu, Illustration Rare." Always rarity or pattern.
- A hit (rank 4+) that is Already caught: the signature line. Reaction cut short, then the verdict, then nothing: "Card ten- Umbreon EX. ... Already caught." Max one small aside per episode ("Lovely. Useless."), never a tally.
- A hit that registers or upgrades: the full hit line from the script recipe, verdict first or last, one verified art detail.
- Set hook line (beat 2): the true four-word hook, as today.
- Spoken numbers: the Dex total at the start, and at the end only when it changed. Region numbers only at a milestone ("and that's half of Alola").
- Still banned: tallies of hits, counting filler, callbacks to the hook, prices, "numbered past the set", number trivia.

## 8. Filming protocol (what to record, every session)

Order is the whole format. Film packs in the order they will be published, and never open a pack off camera.

The printable version is `dex/filming-checklist.md`; this section is the reasoning behind it. Cards are shown in hand to camera, as in every Draw so far; there is no mat, no drum, no slate and no extra holds (user, 2026-11-08: "I won't hold anything. It will be 2-3 packs per video, and the videos will always be in order"). The user guarantees the order; the per-video pack count is told with the file.

Presenting the packs: nothing extra is filmed for it. Each pack enters the same way (below, section 8 step 1), and its own 1.5 s pack-front frame is cut out and animated into the episode's pack line-up (beat 2), so a new stock never needs a new shot.

Pack entrance (user's choice, 2026-11-08: option 1, lift from below): the pack is brought up into frame from below the bottom edge, face to camera, in one smooth lift, and stops centred and still. The scan graphic fires on the stop. Alternatives considered: slide in from the side (alternating sides per pack; graphic identical) and a second hand covering the artwork that pulls away as the beam passes (a real reveal, but the closest to ShortPocketMonster's hidden-then-shown flip, so not recommended).

Per pack
1. Pack lifted into frame from below, face to camera, one smooth move, then steady and centred for 1.5 s (the scan fires on the stop; this frame is the set identification and the cut-out for the line-up). Never shown back first, never flipped.
2. Tear.
3. Every card shown one at a time, held steady, straight and centred, fingers clear of the art, for at least 0.8 s before the next card. That still frame is both the landing frame the stamp lands on and the crop that becomes the card's Pokédex tile, so a card shown too briefly or at an angle has no tile.
4. Cards of rank 3 and up (every holo, ex, Illustration Rare and above) and any Poké Ball / Master Ball pattern card: the same hold, 1.5 s instead of 0.8 s, because that tile may sit in the Pokédex for the rest of the run.
5. No separate best-card hold: the hook and the end hold reuse the card's own 0.8-1.5 s frame.

No stock footage. Dex #1 opens on its own packs like every other episode.

Same camera, framing, light and background as Draws #1-#17. Nothing else changes.

## 9. Graphics

- Persistent chip top-left: "DEX 134" (replaces "Draw #N" and the ball tracker). **OVERRIDE**. Set chip under it.
- Verdict stamp: lower band inside the safe area, under the card, never over art. CAUGHT (green), ALREADY (grey, smaller), UPGRADED (gold). On Caught/Upgraded the stamp carries the entry name in the display spelling.
- Dex tiles: crops of the user's own filmed cards (tile shots, section 8), masked to the card shape, small. Empty tiles: flat dark rounded squares with the entry's set number, no silhouette, no art.
- Pokédex strip: the six numbers around the card's National number, in order, as tiles; filled numbers show their filmed card, empty numbers show only "No. 0767". Shown while a Caught or Upgraded plays and on the end frame. Never a full-screen grid mid-episode.
- Fly-in: on Caught, the card's crop (from the landing frame, not the tile shot, which is swapped in afterwards) shrinks into its tile in 0.4 s. On Upgraded, the tile flips and shows the new crop with a shimmer.
- Captions, safe area, fonts unchanged. No official artwork anywhere; the tile for an entry is always a filmed card.

### 9.1 The Dex animation, frame by frame (30 fps)

Mock-ups (v4, two design directions for the user to choose from; v1-v3 in `dex/mockups/` are superseded, they used pills, boxes and a permanent corner HUD, all rejected 2026-11-08): `dex/mockups/v4/A_preview.mp4` and `B_preview.mp4` (each: Caught, Upgraded, Already in sequence), `A_storyboard_*.jpg`, `B_storyboard_*.jpg`, `compare_A_vs_B.jpg`. Generator: `dex/mockups/make_mockups_v4.py`. Rendered on Draw #16/#17 frames with Pillow and the channel's Fredoka font; production builds the chosen one in the Remotion timeline with the same timings.

Shared rules for both directions
- **No persistent HUD.** Nothing sits in a corner during the opening. The Dex is visible only while a Caught or Upgraded plays, and on the end frame.
- **Type, not boxes.** Verdicts, names and counts are letter-spaced Fredoka type with a black stroke or on a soft dark scrim; no pills, no chips, no panel boxes. The only strokes are a 1 px hairline on filled tiles and a 2 px yellow frame on the target slot while the card is in flight. Everything anti-aliased.
- **The Pokédex row:** an edge-to-edge row of tiles with faded ends, the card's National number in the centre slot, neighbours in order. Filled numbers show their filmed card; empty numbers show "No. 0767" on a faint tile. Header line above the row: "POKÉDEX 134 / 1025" left (the total; it rolls on a Caught), region and its count right ("ALOLA 13 / 88"); on an Upgraded the right side reads "UPGRADES 18". A soft dark gradient scrim sits behind the row so the type reads on any footage.
- Colours: yellow #FFCB05 for the Dex numbers and target frame, green for CAUGHT, gold for UPGRADED, grey for ALREADY CAUGHT, white for names.

**Chosen (user, 2026-11-08): Direction B, inline**, with the row and its header enlarged for readability ("B is better only the hud should be bigger and readable a little more"). Direction A (take-over: footage dims, card lifts to centre, big type, then fades back) stays in the mock-ups as a rejected alternative.

The inline design, as rendered in `v4/B_preview.mp4` and the `B_storyboard_*.jpg` sheets
- Footage is never dimmed, blurred or interrupted.
- Verdict type under the card's art, centred on the card: CAUGHT in 68 px green (UPGRADED gold, ALREADY CAUGHT 50 px grey), letter-spaced, 7 px black stroke; the name under it in 50 px white with a 6 px stroke. Positioned from the card box so it sits over the text area, about 345 px above the card's bottom edge.
- The Pokédex row: five tiles 162x227 px, centred, 23 px gaps, ends fading into the frame, row centre at y 1400 (tiles 1287-1513, number labels to 1545, inside the safe area). The card's National number is the middle tile. Empty tiles: faint white fill at 10% with "No." and the four-digit number; filled tiles: the filmed card with a 1 px hairline rim and a soft shadow.
- Header line 34 px SemiBold, letter-spaced, 70 px above the tiles: left "POKÉDEX 133 / 1025" (the total, ticks on a Caught), right in yellow 40 px Bold "ALOLA 12 / 88" (region count, ticks on a Caught) or "UPGRADES 17" on an Upgraded.
- A dark gradient scrim at 74% behind header and row, fading in over 90 px above and out over 110 px below. No box.
- Only strokes: the hairline on filled tiles and a 2 px yellow frame on the target tile while the card is in flight.

| Verdict | Frames (30 fps) | What happens | Sound |
|---|---|---|---|
| **Caught** (1.3 s to the tick, 2.5 s total) | 0-5 | CAUGHT and the name rise 26 px and fade in. | register ding on frame 0 |
| | 4-12 | Row and header fade in and settle up 30 px; the target tile's yellow frame starts pulsing. | |
| | 12-32 | A copy of the card lifts off the footage, rotates from -10° to 0°, shrinks to tile size along an upward arc with a three-ghost motion trail, and lands on the middle tile. The footage card stays where it is. | soft whoosh |
| | 32-40 | Tile flashes white, bounces 1.14x and settles, one ring expands and fades. "NEW" tag inside the tile's corner from frame 35. "POKÉDEX 133" ticks to "134" at frame 36, the region count ticks with the landing. | counter tick |
| | 40-64 | Row holds. If the next card is also Caught or Upgraded the row stays and the next flight starts at its own frame 12. | |
| | 64-74 | Row, header and verdict type fade out. | |
| **Upgraded** (1.6 s to the tick, 2.9 s total) | 0-5 | UPGRADED in gold and the name with its rarity ("VELUZA EX"). | shimmer tone on frame 0 |
| | 4-12 | Row in; the middle tile already holds the old card, dimmed; header right reads "UPGRADES 17". | |
| | 12-32 | Same flight as Caught. | soft whoosh |
| | 32-38 | The old tile squashes to zero width (a flip on its vertical axis). | |
| | 38-44 | The new tile grows from zero width to full. | |
| | 44-58 | A gold band with a white edge sweeps across the new tile; bounce and gold ring; "UPGRADED" tag from frame 46; "UPGRADES 17" ticks to "18" at frame 48. The Pokédex total does not move. | upgrade chime |
| | 58-76 | Hold. | |
| | 76-86 | Row and type fade out. | |
| **Already caught** (1.3 s) | 0-5 | ALREADY CAUGHT in grey type rises and fades in. No name, no row, nothing else on screen. | soft tick on frame 0 |
| | 5-40 | Holds until the next card lands; the next card's landing fades it. Three or more in a row: the type only changes its position with each card. | |

Rules
- The flight always starts from where the card actually is in the footage (card box from the identification table), so it reads as that card leaving the hand.
- The row's five slots are the National numbers around the card's number, so the row moves through the Pokédex as the run progresses; the card's number is always the middle slot. For a trainer card the row shows the tail of the Trainer Dex in first-appearance order with the new entry appended last ("T-021, T-022, T-023 NEW"); for an already-caught or upgraded trainer, the slots around its own T-number. Header left "TRAINER DEX 23".
- When two Caught/Upgraded cards follow each other, the second flight begins as soon as the first tile has flashed; the panel never closes between them.
- Per-card durations in section 5 include these animations: a Caught card occupies 1.2-1.6 s of screen time, which is the stamp, the flight and the tick with the next card landing during the panel hold.
- The end frame (beat 8) reuses the panel at full width with the episode's new tiles glowing once, then cuts.

## 10. Audio

- Three new signature sounds, generated once (ElevenLabs SFX, original): register ding (Caught), soft tick (Already), shimmer (Upgraded). Never a game sound. Same three sounds in every episode; they are part of the brand.
- Counter tick-up sound for beats 5 and 8.
- Bed, riser, impact, dud sting, ducking and loudness rules unchanged from `starting-prompt.md`.

## 11. Titles, captions, publishing

- Series number: "Dex #N" per episode, starting at #1 the day after the last drum short. **OVERRIDE** of "Draw #N" for new recordings (section 12, Q2).
- Title grammar: `Dex #N: {key event}`. The key event is the deadpan beat, the biggest Caught/Upgraded, or a page milestone. Examples: "Dex #14: Umbreon EX. Already caught." / "Dex #3: seven new, Dex at 41" / "Dex #41: Prismatic Evolutions complete". No dollar figures, no questions.
- Description: one line on the episode's verdicts, the new total, the region milestone if any, then the comments prompt (caption only, never spoken): "Which entry should be upgraded next?" Hashtags as today plus #pokedex.
- TikTok: same file, same caption shape, AI-generated content label on. YouTube: altered/synthetic disclosure on. Daily slots unchanged (YouTube 10:00 PM, TikTok 10:05 PM local), the user presses Schedule.
- First episode extra: the description explains the three verdicts in one sentence each.

## 12. Decisions the user made (2026-11-08)

1. **61-second floor: kept.** Episodes run 61-65 s (70 s with a third pack).
2. **Series name: "Dex #N"**, starting at #1 with the pilot. The first description introduces the three verdicts in one sentence each.
3. **Verdict words: "Caught / Already caught / Upgraded."** Fixed for the run.
4. **Sets: several Mega Evolution-era sets**, mixed. The Dex is a National Pokédex, so the set mix only changes which regions fill fastest; the gate-1 table reports the region counts after each episode.
5. **Drum stock: about 30 shorts left**, shipping daily. The Dex pilot goes out next week regardless, between drum shorts; the Dex run then continues whenever Dex sessions are filmed, with the state carried over.
6. **Mixed-set episodes: allowed.**
7. **Dex starts empty.** Dex #1 opens at zero.
8. **Packs per video: random, 2 or 3**, user's choice per video (2026-11-08). The 61 s floor becomes a target: the gap is filled with at most two unforced cut-aways, never with longer holds, and a shorter episode ships at its natural length (section 5.1). Original reasoning: "the content can be filled with pokemon stock footage and meme joke stock footages, as other big channels do". Honest count at the per-card times in section 5: a pack is about 14-16 s late in the run (mostly Already) and 20-23 s early (mostly Caught); two packs plus hook, line-up and end come to 40-55 s, three packs to 55-75 s. So a two-pack episode needs 6-20 s of cut-aways, a three-pack episode 0-6 s. Section 5.1 defines them.
9. **Decided (a), 2026-11-08: licensed stock and own-footage cut-aways only; no anime, game footage or official artwork.** Kept for the record: anime clips and official artwork in the cut-aways. `starting-prompt.md` bans official Pokémon artwork, anime clips, game footage and AI-generated Pokémon, and the user wrote that rule. Allowing "Pokémon stock footage" means loosening it. The risk is concrete: anime and game footage is owned by The Pokémon Company and Content ID matches it; a claim blocks Shorts over 60 s worldwide (the channel's own note in `starting-prompt.md`), and three strikes end the channel. Big channels run that risk and absorb claims; this channel is at the stage where one claim costs the whole 61 s strategy. Two ways: **(a)** the safe set: meme and reaction footage only from libraries with a written licence (Pexels, Pixabay, Mixkit are free for commercial use; Storyblocks or Artgrid if paid), plus Pokémon-themed cut-aways made from the channel's own filmed cards (slow pushes on a card's art, the card's Pokédex line, a stack of this run's pulls); **(b)** also anime or game clips, accepting claims and strikes as a cost. My recommendation: (a), and revisit (b) once the channel has escaped the local test batch and can afford a claim. The AI-generated Pokémon ban stays either way.

## 13. Decisions I made for you (override any while reading)

1. One channel-wide National Pokédex keyed by Pokédex number (forms share their number); a separate Trainer Dex by card name for trainers and special energy; basic energy excluded.
2. Printed rarity decides upgrades, finishes (reverse, Poké Ball, Master Ball) only break ties within a rank.
3. Packs publish in filmed order, no pairing, no bank; the pack count per video is the user's, never changed for length.
4. Consecutive "Already caught" shortened to "Already." and silent after three; names spoken only on Caught/Upgraded.
5. Counter spoken only at start and end; region spoken only at a milestone.
6. No drum, no loop ending; episodes end on the counter tick and a 2 s hold.
7. Dex tiles are filmed card crops (landing-frame crops for commons and uncommons, tile shots only for rank 3+ and pattern cards); empty tiles are blank numbered squares.
8. Dex state is a replayable per-episode log; verdicts are computed from the replay, shown at gate 1, and corrected only by appended correction records after publishing.
9. The hook is a flash-forward and exempt from the filmed-order rule; the body is not.
10. Identification stays my job from the 4K frames with a card database behind it; the user approves at gate 1 as today.
11. When the packs alone fall short of 61 s: at most two cut-aways from the library, only where a joke lands; if still short, the episode ships at its natural length and the publish notes flag it. Never a longer hold, never a forced insert.

## 14. Left to the builder (me, at production time)

- Exact per-card durations inside the ranges, the speed ramps, and the sync to the ElevenLabs word timings (same method as today).
- The card data: source confirmed 2026-11-08, TCGdex API (`https://api.tcgdex.net/v2/en/series/me`), which lists the Mega Evolution era: Mega Evolution (132 official cards), Phantasmal Flames (94), Ascended Heroes (217), Perfect Order (88), Chaos Rising (86), Pitch Black (84), 30th Celebration (128), Delta Reign (103), plus promos and the energy set. Each card record carries its National Pokédex number(s), printed rarity and category, which is all the Dex needs; the printed "NO." on the card is the cross-check at identification.
- Stamp, chip and tile design within the safe area; the three signature sounds.
- The identification-to-verdict script and the gate-1 table layout. **BUILT 2026-11-08:** `scripts/dex_catalogue_pull.py` (froze all 11 Mega Evolution-era sets, 1439 cards, into `dex/catalogue/`), `scripts/dex_names_pull.py` (`dex_names.json`: 1025 names from PokéAPI, regions, rarity ladder as data), `scripts/dex_catalogue.py` (lookup; resolves the 114 Delta Reign cards TCGdex ships without a National number from their names; `overrides.json` for hand fixes), `scripts/dex_replay.py` (replays `dex/episodes/`, writes `dex_state.json` + the four CSVs, prints the gate-1 table with the before/after totals; corrections applied at load). Tested on a two-episode fixture: caught / already / upgraded incl. Master Ball finish upgrade, trainer numbering T-001.., correction re-derivation, region counts. Ladder additions for rarity strings the plan did not list, my calls, noted in `dex_names.json`: Mega Hyper Rare 9, Mega Attack Rare 7, Futuristic Rare 7, RGB Rare 7, Pikachu Rare 6, 30th Classic reprints 3, Promo 4 if ex else 3.
- Hook candidates per episode, 3-4 at gate 2, user picks.

## 15. Gates (unchanged workflow, one new table)

1. Identification table per pack with landing timestamps on the 0.2 s grid, PLUS the computed verdict column and the Dex deltas for the episode. Approved before any script.
2. Script per episode with the hook candidates table. Model switch requested before scripting and again after, as always.
3. One VO sample line, then the batch and a listen-through file.
4. Low-res draft. Checks before I offer it: duration gate, every named card within 0.05 s of its spoken time, hook done by 2.6 s, stamps on settled frames only, Dex deltas on screen match the gate-1 table, no official art anywhere.
5. Final render and publish metadata; `dex_state.json` updated on publish.

## 16. What we measure

Read after the first three Dex episodes are each 3+ days old, the same way as `analytics-checks.md`.

| Metric | Two-pack drum baseline (#8-#15) | Dex target |
|---|---|---|
| Stayed to watch | 16-52% | >= 55% |
| Average view duration | 14-30 s | >= 33 s |
| Average % viewed | 23-47% | >= 50% |
| Unique viewers, first 3 days | 14-316 (one escaped the local batch) | the batch escapes Romania on at least 1 of 3 |
| Comments | 0 | > 0 on at least 1 of 3 (verdict disagreement is the engine) |
| Returning viewers (YouTube "returning" in Audience) | not tracked | tracked from episode 1 |

If stayed stays under 45% on all three, the first lever is the hook footage (deadpan beat vs biggest Caught), the second is per-card time in beats 3 and 6. The verdict words and the Dex rules do not change inside the run.
