# poke.capnv plan: Draw #8 onward (two-pack shorts)

Status: APPROVED 2026-10-28 (all section-10 decisions confirmed one by one by the user). Draws #4 to #7 ship unchanged (#7 scheduled Oct 29 on both platforms). This plan applies to every short cut after that.

Evidence: `analytics-checks.md` (YouTube + TikTok, Draws #1 to #6, read 2026-10-28) and `research/reference-shorts-analysis.md` (12 top-viewed pack-opening Shorts, 8 clean openings). Every rule below names the number it comes from.

Everything in `starting-prompt.md` still applies (identification table, VO voice and processing, sync rules, script recipe, banned lines, audio, captions, constraints) unless a line here overrides it. Overrides are marked **OVERRIDE**.

---

## 1. Input and output (how many sessions, how many shorts)

| | Definition |
|---|---|
| One filmed session | Exactly what you film today: one continuous 4K take, drum spun four times, four balls shown, then the four matching packs opened one by one, hits shown at the end. No speech. |
| One short | Two packs from the inbox, 61-65s, one video. |
| Conversion | **1 session = 2 shorts. Always.** 4 packs in, 4 packs out, no pack is dropped. |
| Batch you provide | **3 to 6 sessions at a time = 6 to 12 shorts = 6 to 12 publishing days** (user, 2026-10-28: 5-6 sessions is fine). Bigger batches pair better: more packs to choose from means fewer hitless shorts. Minimum batch is 2 sessions; 1 session gives me nothing to pair against. The next batch should be in the inbox before the current one has 2 shorts left to publish. |
| What I deliver per batch | Two rendered shorts per session (6 to 12), each with title, description, hashtags, one `pairing.json` for the batch, and the per-session `card_identification.md` files. |
| Pack bank | A pack can be held back for the next batch when pairing needs it (section 4). The bank never holds more than 2 packs, so the count stays "6 in, 6 out" from batch two onward: if 2 packs go into the bank, 2 come out. Nothing is wasted; a banked pack is published one batch later. |
| Hit supply | On Draws #1 to #7: 10 Tier 1/2 hits in 28 packs (36%), per session 1 / 2 / 0 / 1 / 1 / 2 / 3. With perfect pairing that is 10 shorts with a hit and 4 without out of 14. Editing cannot change that number; only the packs can. Hitless shorts are therefore part of the plan (section 5), not an exception. |

Publishing cadence: **one short per day from Draw #8 on** (user, 2026-10-28), YouTube and TikTok the same file the same day. The first batch after this plan: Draws #8 to #13, six consecutive days.

## 2. What the data decided (one line each)

| Finding | Numbers | What it decides |
|---|---|---|
| The spoken hook decides the swipe. Lines that promise a hit in the first words kept 49-59%; lines that open on a negative or a coincidence kept 33-36%. The frame-one card did not separate episodes (#4 full-art 49%, #6 plain card 55%, #5 Crobat ex 33%). | #1 59, #2 59, #4 49, #6 55 vs #3 36, #5 33 | Hook = spoken promise of the best card, first words. Never a negative, never a coincidence opener. |
| Average viewer leaves at 25-31s, whatever the hit timing, except when the hook promised a late payoff. | AVD #1-#4,#6: 25-31s; #5: 39s, 46% at 30s, 24% at 60s | Two packs, 61-65s; best card lands at ~42s after a promise. |
| A reveal does not create a plateau. | #2 56->32 (19-29s), #4 36->25 (25-40s) | Nothing is placed after the best card except its hold. |
| The last 10-15s plays to under 10%. 0 comments on 7,400 views. | 75s: 12-17%; 90s: 4-8%; comments 0/6 | No summary section, no sign-off line. Comments prompt moves to the caption. |
| Top Shorts: voice at 0.0s, pack/drum in hand, hook names the result in words, first notable card 7-38s, 10 of 12 end on the held hit, no CTA, lineup only in the 10-pack video. | 8 clean openings, 5.5M-58M | Confirms the hook grammar and the ending. |
| Feed gives one ~1k batch on day one and stops. | all six | Judge shorts on stayed %, AVD and 30s retention, not views. Daily publishing means one fresh batch a day instead of one every two days. |
| TikTok: 5.6-8.4s average watch, 0 followers on all six. | 256-333 views each | Same file, no TikTok-specific work. Only constraint kept: the 61s floor. |

## 3. The short, second by second (target 62s, floor 61.0s, ceiling 65s)

Frames at 30fps. Durations are targets; the VO-to-footage sync rules in `starting-prompt.md` set the exact cuts. Pack A = the pack with the smaller result. Pack B = the pack with the short's best card.

| Beat | Time | Frames | Screen | VO | Audio |
|---|---|---|---|---|---|
| 1. Hook | 0.0-2.8 | 0-84 | Current hook, unchanged: pack B's best card landing, 0.5x, push-in 100->112%, full screen, no name, no tag, no glow. Caption below the card. | Voice at 0.0s. One sentence that PROMISES the best card (section 5 grammar). Finishes by 2.6s. | Silence under the voice, drum sting on the cut. |
| 2. Ball A | 2.8-6.0 | 84-180 | Hard cut to the drum; ball A leaves the drum, number pops and docks top-left. Tracker: two ball slots, slot 1 fills. Tray cropped so no other ball is in frame. | "First up, {N}. {Set}, {true four-word set hook}." | Music bed in. |
| 3. Pack A tear + run-up | 6.0-17.0 | 180-510 | Tear at 3-4x. Cards 1-9 at 0.4-0.7s each, tick per card, counter "card n/11" (energy = card 1). | At most one line naming 2-3 cards if there is something to say; otherwise VO is silent until the rare slots. | Ticks, bed. |
| 4. Pack A cards 10-11 | 17.0-23.0 | 510-690 | Riser, push-in 100->115%, reveal on impact, hold. If pack A has a Tier 1-3 card: glow + rarity tag, hold for the line. | "Rare slot, {card}. Regular holo." or the hit line if pack A has a hit. | Riser, impact, dud sting or shimmer. |
| 5. Ball B (seam + re-hook) | 23.0-26.0 | 690-780 | Cut ON ACTION (card landing or hand to the drum) to ball B leaving the drum; number pops, slot 2 fills. This is where two sessions may be joined (section 6). | "Then {N}. {Set}, {set hook}." plus a re-promise that does not name the card: "and this is the one." / "and you've already seen what was in it." | Drum sting, bed continuous across the cut. |
| 6. Pack B tear + run-up | 26.0-42.0 | 780-1260 | Tear 3-4x, cards 1-9 slower than pack A (0.6-0.9s each), every card readable. | Name list ending on the dash: "{card}, {card}, {card}... nothing yet, and then card ten-". Music drops on the dash. | Ticks; bed drops out before the reveal. |
| 7. Pack B best card | 42.0-53.0 | 1260-1590 | Slow-mo build to 0.2x, freeze on the landing, glow, rarity tag, hold for the whole line. | Hit line: reaction, name, rarity, ONE verified art detail. | Impact + shimmer. |
| 8. Behind the hit | 53.0-58.0 | 1590-1740 | Card 11 if the hit was card 10 ("and a {card} holo behind it"), or the pack's coincidence, or a second look at the hit from the end-of-take footage. | One line. | Bed back, soft. |
| 9. End | 58.0-62.0 | 1740-1860 | Hold the best card with its rarity tag 2.5s, then hard cut on motion into the spinning drum for ~1s so the last frame matches frame 0 (loop). No summary card, no ball tokens, no sign-off, no subscribe. **OVERRIDE** of the "Last ~10s: summary card ... sign-off" block in `starting-prompt.md`. | None after beat 8. | Bed out on the cut, drum sting. |

Gate: render length >= 1830 frames (61.0s) and <= 1950 (65.0s). The build fails outside that window. Fill toward 61s with beats 3 and 6 (more cards on screen, slower pack B run-up), never with a longer hold.

Why the best card is at 42s and not at 15s: #5 is the only episode where viewers held (46% at 30s vs 33-38% elsewhere) and it is the only one whose hook promised a payoff that came late. Early hits (#2 at 18s, #4 at 34s) were followed by the steepest drops. With the best card at 42s, the ~45% who are still there at 30s get it within 12s, and nothing follows it.

If pack A has the only hit and pack B is the dud (a hitless pairing is impossible to avoid in that batch): swap roles so the hit is still pack B. "Smaller result first" is the rule, whatever the tiers.

## 4. Pairing (my job, every batch)

Tiers: **T1** SIR, SAR, gold, hyper rare, full-art Ultra Rare. **T2** Illustration Rare, ex / V Double Rare. **T3** Poké Ball / Master Ball pattern, ACE SPEC. **T4** regular holo rare only.

1. Identify every pack first (balls, sets, opening order, every card with rarity, landing timestamps on the 0.2s grid) and write `card_identification.md` per session, as today. Show the table at gate 1.
2. Pair so that as many shorts as possible have a T1/T2 card. Surplus hits are spread, never stacked: two T1/T2 in one short only when every short in the batch already has one.
3. Prefer pairs from the same session (no seam, no grade match). Cross-session pairs only when a session cannot give both its shorts a hit and another session has a surplus.
4. T4+T4 is the last resort. Before shipping a T4+T4 short, check the bank; if the bank has a hit pack, use it and bank one of the T4 packs instead. Bank limit 2 packs, held for one batch at most, then published regardless.
5. Coincidences (same card twice, evolution line in one pack, wrapper Pokémon pulled) count half a tier up, because the VO can use them in beat 8.
6. Within a pair, pack B = higher tier; on equal tiers, pack B = the one with the better art detail or coincidence.
7. Output `projects/<batch>/pairing.json` with session, ball, set, cards 10/11, tier, short number, slot A/B, bank in/out. Shown at gate 1 before any scripting.

## 5. Hook (decided: keep the current hook, user 2026-10-28)

The cold open stays what it is on Draws #1 to #7: the best card's reveal footage at 0.5x with a push-in, full screen, no name, no tag, no glow, caption below the card, [conspiratorial] line, cut to the drum +0.15s after the last word. Thirteen alternatives were mocked up (`research/hook-mockup/`) and rejected as worse.

Why it stays (research + our numbers):
- It is the only hook with measured results: 59 / 59 / 55 / 49% stayed on the four promise-line episodes. The two failures (36%, 33.5%) were line failures, not footage failures; #6 held 55% with a plain card on frame one.
- It already has what all 8 big openings share: the voice names the result at 0.0s, text on screen from frame one.
- The card held up is the end frame of 10 of 12 big Shorts; ours puts the genre's strongest image on frame one. The big channels can open on the pack because a face and live reactions carry the wait; we have neither.

The LINE is the lever and gets the rules:
- Voice at 0.0s, finished by ~2.6s.
- First clause promises the best card: "had this", "had an EX", "came out of". Never names the Pokémon.
- Banned openers: negatives or duds first ("Three regular holos..."), coincidence-first ("the same card twice"), questions, tallies, "four packs".
- Rotate every short; never reuse the previous short's line. Two-pack pool: "One of these two packs had this." / "Two packs. The second one had this." / "Ball twenty's pack had this." / "This came out of the second pack." / "The ball bounced off the tray. Its pack had this."
- Hitless short: same grammar on the best true card ("One of these two packs had a Poké Ball {Pokémon}."), card shown. Expect a lower stay and record it; it is a hit-supply problem.
- Gate 2 shows 3-4 candidate lines in a table with my pick and reason, as today.

## 6. The footage and how each beat uses it

What arrives: one continuous take, 4K HEVC HLG, 30fps camera, silent/ambient. Order inside the take: drum spin and ball 1, spin and ball 2, spin and ball 3, spin and ball 4 (all four balls end up on a tray), then pack 1 tear and 11 cards flipped one by one onto the mat, pack 2, pack 3, pack 4 (not necessarily in draw order), then the hits held up / the four best cards laid out.

| Footage segment | Used in | How |
|---|---|---|
| Spin + ball leaving the drum (x4) | Beat 2 and 5 of whichever short that pack belongs to | Take the 2-3s from the spin to the number being readable. Push in / crop so the tray's other balls are out of frame; the two-slot tracker carries the numbers. Never show the full tray. |
| Pack tear (x4) | Beat 3 / 6 | 3-4x speed, dead time cut. |
| Card run, cards 1-9 (x4) | Beat 3 / 6 | Speed-ramped to the VO names; unnamed cards 0.4-0.9s each. |
| Cards 10 and 11 (x4) | Beat 4 / 7 / 8 | Landing frame from the 0.2s grid is the reveal frame. |
| Best card landing | Beat 1 (hook) and beat 7 | Same footage used twice: 0.5x in the hook, slow-mo build and freeze in beat 7. |
| End-of-take hold-ups / four-card layout | Beat 8 only, and only when the frame can be cropped to the short's own card | **Never shown as a four-card lineup.** Two of those cards belong to the other short. |

Cross-session seam (beat 5): grade both sessions to matching exposure and white balance before the cut, cut on action, keep the music bed continuous, let the "Then {N}" line bridge it, no dissolve. If the two takes cannot be matched (different mat, lighting or framing), re-pair inside the session rather than ship the mismatch, and say so in `pairing.json`.

## 7. Titles, numbering, graphics, captions

- Numbering: a running "Draw #N" per short (#8, #9, ...). The number no longer equals a filmed session.
- Title: `Draw #N: 2 balls, 2 packs - {best card}`. No dollar figures. **OVERRIDE** of the four-ball title template.
- Top-left chip "Draw #N" with a TWO-slot ball tracker (opening order, slot fills when its pack block starts). **OVERRIDE** of the four-slot tracker.
- Rarity chips only on T1-T3 cards. No prices anywhere (user, 2026-10-28); the value-chip option in `starting-prompt.md` is dropped.
- Captions, safe area, fonts unchanged.
- Description ends with the comments prompt ("Guess the next ball in the comments"); it is no longer spoken. **OVERRIDE** of the sign-off line.
- VO wording that assumed four packs is gone: no "Last one", no "four packs", no summary callbacks.

## 8. Gates (unchanged workflow, two new checks)

1. Identification + pairing table for the whole batch (before any script).
2. Script per short, line by line, with the hook candidates table.
3. One VO sample line, then the batch and a listen-through file.
4. Low-res draft per short. Before I offer it: duration gate (1830-1950 frames), every named card within 0.05s of its spoken time, hook line finished by 2.6s, no four-card frame anywhere, seam check if cross-session.
5. Final render and publish metadata.

## 9. What we measure, and when we change the plan again

Review after Draws #8, #9 and #10 are each 3+ days old, which at one short a day is the day Draw #13 publishes (retention under 3 days is provisional: #2 read 0:46 then settled at 0:30). Read the same way as `analytics-checks.md` describes. Shorts already cut by then ship as planned; changes apply from the next batch.

| Metric | Baseline (4-pack) | Target for the two-pack format |
|---|---|---|
| Stayed to watch | 49-59% on promise hooks | >= 55% |
| Average view duration | 25-31s (39s on #5) | >= 33s |
| Average % viewed | 27-40% | >= 50% (33s of 62s) |
| Retention at 30s | 33-46% | >= 45% |
| Retention at the best card (~42s) | 25-33% at 40s | >= 35% |
| Engaged views / views | 39-66% | >= 60% |

One variable changes at a time after that. The next tests, in order, if the targets are missed: (1) best card at ~30s instead of ~42s, (2) the hook footage (user to choose; mockups in `research/hook-mockup/`).

## 10. Decisions this plan makes for you (override any of them while reading)

1. Hook = the current cold open (card in slow-mo), line rotated and written as a promise. Negative and coincidence openers are banned. (User decision 2026-10-28.)
2. Smaller pack first, best card at ~42s, re-promise at ball B. (User confirmed 2026-10-28.)
3. Ending = hold the best card 2.5s, cut to the drum, loop. No summary, no sign-off, no CTA in the VO. (User confirmed 2026-10-28.)
4. No prices anywhere.
5. Running Draw #N per short, two-slot tracker, "2 balls, 2 packs" title. (User confirmed 2026-10-28.)
6. You provide 3 to 6 sessions per batch; I return two shorts per session for the daily slots; a 2-pack bank carries pairing problems to the next batch; hitless shorts are published, not held forever. (User confirmed 2026-10-28.)
7. Same-session pairing first; cross-session only to give a short a hit; re-pair rather than ship a visible seam. (User confirmed 2026-10-28.)
8. TikTok gets the same file; no TikTok-specific cut. (User confirmed 2026-10-28.)
