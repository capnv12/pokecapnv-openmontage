# poke.capnv analytics checks

Direction review for the channel. Run the full check when **Draw #6's analytics have landed and Draw #7 is published**. The output of that review is the brief for the next, improved approach (episode structure, pack count, hook, pacing).

## Baseline (read 2026-10-21 from YouTube Studio)

| | Draw #1 (HfgQd_wSJII) | Draw #2 (UYp9nW4Wtqg) |
|---|---|---|
| Length | 1:42 | 1:38 |
| Views at read | 1,225 | ~800, 3 days old |
| Stayed to watch / swiped away | 59% / 41% | 58-60% / 42% |
| Average view duration | 0:31 | 0:46 |
| Average % viewed | 30.7% | 47.4% |
| Retention @5s / 10s / 19s | 89 / 62 / 48 | ~100 / 84 / 68 |
| Retention @30s / 40s / 60s | 34 / 29 / 22 | 49 / 42 / 39 |
| Retention @75s / 90s | ~16 / 12 | 32 / 21 |
| First hit lands at | 55s (Deerling) | 18s (Farigiraf) |
| Likes / comments / shares | 20 / 0 / 0 | 0 / 0 / 0 at read |
| Traffic | 96.6% Shorts feed | 96.9% Shorts feed |

What the baseline showed:

- No 40s cliff. Both curves are front-loaded bleeds.
- Swipe rate is the same on both (same cold-open line), so the hook line did not separate them.
- Time-to-first-hit did: 68% vs 48% still watching at 19s.
- Draw #2 is flat 40-60s (viewers past the first hit stay), then bleeds 60-90s across the Ditto dud, the 11s gap from Ball 20 to the Serperior reveal, and the summary.
- Working hypothesis: a real pull inside the first 20s, never two dud packs before a hit, under 10s from ball draw to rare slot.

## How to read each video (YouTube Studio)

1. Video > Analytics > **Engagement** tab. Note Stayed to watch %, Average view duration, Unique viewers.
2. Scroll to **Audience retention**. Hover the chart and record % still watching at 5s, 10s, 19s, 30s, 40s, 60s, 75s, 90s and the end. Screenshot the chart and the "Key moments" panel.
3. **Reach** tab: Shorts feed share, search terms if any.
4. Advanced Mode (channel level, dimension = Content, range covering the publish date): Views, Engaged views, Average view duration, Average percentage viewed, Likes, Comments added, Shares, Subscribers. Note: the 28-day table can lag the per-video page by a day or more.
5. Map every retention timestamp to the final VO placement: `projects/poke-capnv-draw-NN/artifacts/props.json` has `vo[].from` in frames at `fps` (30), and `script.json` gives each section's label. Note where the first hit lands and how long each ball-to-rare gap is.
6. TikTok per video: retention graph screenshot, average watch time, watched full video %, new followers, For You share.

## Questions the review must answer (Draws #1 to #7)

- Does the hook line change move Stayed-to-watch? Compare the swipe rate across episodes with different cold-open lines.
- Does retention at 19s track time-to-first-hit across all episodes?
- Is there a plateau after the first hit on every episode, and where does the second bleed start?
- Which ball-to-rare gaps are longer than 10s, and do they line up with drops?
- Seconds watched per episode, not just %. Do shorter or reordered episodes hold more seconds?
- Comments per 1k views: has the "guess tomorrow's ball" prompt produced anything yet?
- Followers/subscribers per 1k views by episode.
- Views in the first 48h vs tail per episode; is the feed cutting off at the drop point?
- TikTok vs YouTube: same curve shape, or does one platform hold the 4-pack format better?

## Decision to make after the review

Pick the next approach from the evidence, one variable per episode after that:

- 4 packs vs 2 packs (at 61-65s to keep the TikTok Creator Rewards floor) vs 1 pack YouTube-only.
- Lead pack = best pull, always, or keep drum order.
- Mid-video re-hook before the second half, yes or no.
- Hook line family that produced the best swipe rate.

## Read 2026-10-23 (Draws #1 to #3, YouTube Studio via Claude in Chrome)

Draw #3 = PjS87edzyzw, published 2026-10-21. Draws #4 to #7 are rendered but not published yet.

| | Draw #1 | Draw #2 | Draw #3 |
|---|---|---|---|
| Views (per-video page) | 1,231 | 1,023 | 1,031 |
| Daily views | ~1,070 on Oct 16, then 18 / 108 / 18 / 9 | 90 (Oct 19) / 654 / 279 | 958 (Oct 21) / ~73 |
| Engaged views | 812 (66%) | 664 (65%) | 408 (43%) |
| Stayed to watch / swiped | 59.3 / 40.7 | 58.7 / 41.3 | **36.9 / 63.1** |
| Average view duration | 0:31 | 0:30 | 0:28 |
| Average % viewed | 30.6% | 30.8% | 30.8% |
| Retention @5s / 10s / 19s | 80 / 62 / 48 | ~88 / 69 / 56 | 80 / 55 / 49 |
| Retention @29s / 39s / 59s | 33 / 29 / 21 | 32 / 23 / 18 | 38 / 29 / 17 |
| Retention @75s / 90s | 14 / 12 | 14 / 8 | 14 / 4 |
| Likes / comments / shares / subs | 21 / 0 / 0 / 0 | 6 / 0 / 0 / 2 | 6 / 0 / 0 / 2 |
| Shorts feed share | 97.0% | 96.8% | 97.6% |
| Cold open | "had this card" + Deerling IR on screen | "had this card" + Farigiraf IR on screen | "had the same card twice" + Archeops Poké Ball card on screen |
| First real pull | 55s Deerling IR | 18s Farigiraf IR | none (Archeops x2 at 18-22s, three regular holos) |

Draw #3 extra points: 14s 50%, 22s 46%, 25s 43%, 45s 25%, 50s 21%, 84s 7%.

Changes vs the 2026-10-21 read:

- Draw #2 moved a lot once the data settled: AVD 0:46 -> 0:30, 29s retention 49% -> 32%, 60s 39% -> 18%. The "40-60s plateau" from the baseline is gone; the current curve is a steady bleed like #1. Swipe rate did not move (58-60 -> 58.7). Treat any read younger than ~3 days as provisional; Draw #3's curve is 2 days old and may shift the same way.
- Draw #1 is unchanged.

What the three episodes say:

- **Swipe rate is the only metric that separated the three, and it tracks the cold-open card, not the line.** #1 and #2 share the same line and a full-art IR on frame one: 59% stay. #3 changed the line to "same card twice" and shows a plain Poké Ball-pattern card: 37% stay. That cost ~230 engaged views on the same ~1,000-view feed batch.
- **Seconds watched are flat at ~30s on all three** (30.6 / 30.8 / 30.8% viewed). Hit at 18s, hit at 55s, or no hit: the average viewer leaves around 30s regardless. The first-hit timing did not change seconds watched once the data settled.
- **The hit does not create a plateau.** #2's Farigiraf at 18s: 56% at 19s -> 32% at 29s, the steepest 10s drop of any episode after the swipe. #3's Archeops double at 18-22s: 49 -> 38 over the same window. Viewers see the reveal and leave; the reveal is a release, not a hold.
- **The second half is dead on all three.** 14% at 75s on every episode, 4-12% at 90s. The summary + sign-off (last 10-15s) plays to under 10% of starters. The "guess tomorrow's ball" prompt has produced 0 comments on ~3,300 views.
- **The feed gives each episode one ~1,000-view batch inside 24-48h and then stops**, and it stopped at the same point for 59% stay and for 37% stay. None of the three earned a second push. 48h views ≈ lifetime views on all three.
- Likes per 1k views: 17 (#1), 5.9 (#2), 6.3 (#3). Subscribers: 0 / 2 / 2. Too small to read.
- Thumbnail impressions are 46 / 73 / 7: irrelevant for Shorts, ignore CTR.

Open items for the Draw #4-#7 batch: TikTok numbers not read yet; the 10s ball-to-rare gap check needs the per-pack timing table, not just the VO starts.

### TikTok (read 2026-10-23, TikTok Studio)

Draws #4 to #7 are already scheduled on TikTok: Oct 23, 25, 27, 29 at 10:05 PM.

| | Draw #1 | Draw #2 | Draw #3 |
|---|---|---|---|
| Views | 296 | 331 | 260 |
| Average watch time | 6.83s | 8.54s | 7.77s |
| Watched full video | 0.3% | 0.6% | 0.8% |
| Retention @2s / 5s / 10s | 40 / 20 / 12 | 53 / 23 / 19 | 43 / 27 / 14 |
| Retention @19s / 30s / 60s / 90s | 9 / 6 / 3 / 1 | 14 / 7 / 2 / 1 | 12 / 8 / 3 / 0 |
| Likes / comments / shares / saves / new followers | 3 / 0 / 0 / 0 / 0 | 4 / 0 / 0 / 1 / 0 | 3 / 0 / 0 / 0 / 0 |
| For You share | 99.7% | 99.7% | 100% |
| Views window | all on day 1 | all on day 1 | all inside the first 5 hours |

- TikTok is a different curve, not a worse version of YouTube's. 47-60% are gone by 2s, 73-80% by 5s, and under 15% remain at 19s on every episode. Average watch is 7-9s against YouTube's 30s. The episodes are being judged on frame one and the first spoken line only; nothing after 10s is reaching a measurable audience there.
- The Draw #3 cold-open penalty does not show up on TikTok (2s retention 43% sits between #1 and #2). On TikTok all three covers fail equally.
- 260-330 views per post, 100% For You, no second batch, 0 comments, 0 followers. The 61-65s Creator Rewards floor is moot while 1% reach the end.
- Four-pack TikTok episodes are not being watched past the first ball. If TikTok stays in the plan it needs its own cut: a sub-15s open that lands the hit, not the 4-pack edit.

## Read 2026-10-28 (Draws #4 to #6 + refresh of #1 to #3)

Source: YouTube Studio (per-video Overview/Engagement/Reach pages plus Advanced mode, Content breakdown, last 28 days) and TikTok Studio per-post analytics, read via Claude in Chrome on 2026-10-28. Daily tables end at Oct 27 (the Oct 28 column was not in the Advanced-mode table yet).

Video IDs and publish dates (YouTube):

| | ID | Published | Length |
|---|---|---|---|
| Draw #4 Emboar IR | c2j56fy9or8 | 2026-10-23 | 1:34 |
| Draw #5 Team Rocket's Crobat ex | TM_fLQGud6Y | 2026-10-25 | 1:38 |
| Draw #6 Reshiram ex and Koraidon ex | tT9jttYgGT0 | 2026-10-27 | 1:36 |
| Draw #7 Palafin ex SIR | 3SlfpOyw0i4 | NOT published: Scheduled, Oct 29, 2026 (time of day not read); TikTok copy scheduled Oct 29, 10:05 PM | 1:48 |

Draw #6 is ~1 day old and Draw #5 is ~3 days old: #6 readings are provisional, and its audience-retention curve is not available yet ("Not enough information to display audience retention data").

### YouTube, Draws #4 to #6

| | Draw #4 | Draw #5 | Draw #6 (provisional) |
|---|---|---|---|
| Views (per-video page) | 1,532 | 1,176 | 1,077 (869 on Oct 27, rest on Oct 28 so far) |
| Daily views | Oct 23: 1,095 / Oct 24: 163 / Oct 25: 107 / Oct 26: 59 / Oct 27: 101 | Oct 25: 969 / Oct 26: 81 / Oct 27: 125 | Oct 27: 869 |
| Engaged views | 832 (54%) | 454 (39%) | 647 (60%) |
| Stayed to watch / swiped | 49.3 / 50.7 | **33.5 / 66.5** | 54.6 / 45.4 |
| Average view duration | 0:25 | **0:39** | 0:31 |
| Average % viewed | 27.0% | **40.0%** | 33.3% |
| Unique viewers | 779 | 395 (at Oct 27 table) | not shown |
| Retention @5s / 10s / 15s | 78 / ~62 (read at 0:09) / 54 | 80 / 67 / 57 | not available |
| Retention @19s / 25s / 30s | 48 / 36 / 33 | 54 / 48 / 46 | not available |
| Retention @40s / 50s / 60s | 25 / 17 / 15 | 33 / 28 / 24 | not available |
| Retention @75s / 90s / end | 12 / 4 / 3 (1:34) | 17 / 7 / 2 (1:38) | not available |
| Likes / comments / shares / subs | 30 / 0 / 0 / +2 | 11 / 0 / 0 / +2 | 15 / 0 / 0 / +1 (likes from the Oct 27 table; 869 views at that point) |
| Shorts feed share | 96.9% | 96.4% | 98.3% |
| Cold open | Emboar Illustration Rare full-art on frame one (0.1s) | "Four packs. Three regular holos. And then this." with Crobat ex on screen | "Two of these four packs had an EX." (frame one is a green regular card, not the hit) |
| First real pull | 19.3s Butterfree holo (rare slot), 33.9s Emboar IR hit | 66.7s Crobat ex (cold open already showed it) | 50.0s Reshiram ex, 74.1s Koraidon ex |

Extra retention points (hover readings, tooltip rounds to whole seconds):
- Draw #4: 18s 50%, 9s 62%. Beat map: 19s (rare slot Butterfree) 48 -> 25s (White Flare ball 17) 36 -> 30s (run-up) 33 -> 40s (Tepig/Emboar coincidence, hit was at 33.9s) 25 -> 50s (Ball 29 Black Bolt) 17 -> 60s (Timburr/Haxorus) 15 -> 75s (Zapdos holo) 12 -> 90s (sign-off) 4.
- Draw #5: 5s 80, 10s 67, 15s 57 (Eternatus holo lands 15.1s), 19s 54, 25s 48 (Ball 16 at 21.5s), 30s 46 (Milotic 28.4s), 40s 33, 50s 28, 60s 24 (run-up 58.9s), 75s 17 (hit at 66.7s), 90s 7, end 2.
- Draw #6: no curve. Engagement-page note only; nothing to map to the 50.0s / 74.1s hits.

### Refresh of Draws #1 to #3 (read 2026-10-28)

| | Draw #1 (HfgQd_wSJII) | Draw #2 (UYp9nW4Wtqg) | Draw #3 (PjS87edzyzw) |
|---|---|---|---|
| Views | 1,237 (was 1,231) | 1,030 (was 1,023) | 1,349 (was 1,031) |
| Daily views | Oct 16: 1,075 / 17: 18 / 18: 108 / 19: 18 / 20: 9 / 21: 3 / 23: 5 / 24: 1 | Oct 19: 89 / 20: 654 / 21: 279 / 22: 1 / 23: 5 / 24: 2 | Oct 21: 957 / 22: 72 / **23: 319** / 24: 1 |
| Engaged views | 817 (66%) | 671 (65%) | 563 (42%) |
| Stayed to watch | 59.4% | 58.9% | 36.4% |
| Average view duration | 0:31 | 0:30 | 0:27 (was 0:28) |
| Average % viewed | 30.6% | 30.7% | 30.2% |
| Likes / comments / shares / subs | 21 / 0 / 0 / 0 | 6 / 0 / 0 / 2 | 8 / 0 / 0 / 3 |

Draws #1 and #2 are unchanged. Draw #3 gained 318 views since Oct 23 (Oct 23 had 319 views, after a 72-view Oct 22), which is a second small batch.

### TikTok, Draws #1 to #6 (read 2026-10-28, TikTok Studio per-post analytics)

Posted 10:05 PM on Oct 16 (11:05 PM), 19, 21, 23, 25, 27. Draw #7 is scheduled Oct 29 10:05 PM (0 views).

| | Draw #1 | Draw #2 | Draw #3 | Draw #4 | Draw #5 | Draw #6 (provisional) |
|---|---|---|---|---|---|---|
| Views | 297 | 333 | 261 | 256 | 258 | 266 |
| Average watch time | 6.7s | 8.41s | 7.75s | 6.33s | 5.64s | 7.15s |
| Watched full video | 0.3% | 0.6% | 0.8% | 0% | 0.4% | 0.4% |
| Retention @2s / 5s / 10s | 40 / 20 / 12 | 53 / 23 / 19 | 43 / 27 / 14 | 46 / 23 / 13 | 33 / 20 / 10 | 48 / 23 / 12 |
| Retention @19s / 30s / 60s / 90s | 9 / 6 / 3 / 1 | 14 / 7 / 2 / 1 | 12 / 8 / 3 / 0 | 9 / 5 / 1 / 0 | 6 / 5 / 1 / 1 | 9 / 5 / 2 / ~0 |
| Likes / comments / shares / saves | 3 / 0 / 0 / 0 | 4 / 0 / 0 / 1 | 3 / 0 / 0 / 0 | 5 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 2 / 0 / 0 / 0 |
| New followers | 0 | 0 | 0 | 0 | 0 | 0 |
| For You share | 99.7% | 99.7% | 100% | 100% | 100% | 100% |
| Views window | day 1 | day 1 | first hours | first hours | first hours | all in first 5h (peak hour 1 ~90 views, hours 2-4 ~45-70, zero after 5h) |

TikTok retention reads were hovers on the small post-level graph; each reading was taken from a tooltip showing the time and percent. The 90s value for #6 was read at 1:30 in an earlier pass as 0%.

### What changed (facts only)

- Draw #4's full-art Emboar IR on frame one did NOT hold the ~59% stay of #1/#2: 49.3% stayed (50.7% swiped). It is better than #3's 36.4% and worse than #1/#2's 59%.
- Draw #5 has the lowest stayed-to-watch of all six (33.5%) but the highest average view duration (0:39) and average % viewed (40.0%), and still has 46% at 30s, 24% at 60s and 17% at 75s (the other episodes are at 12-14% at 75s). Viewers who stay past the opening hold much longer on #5 than on any earlier episode.
- Draw #5 and #4 each lost ~18-20 points between 40s and 60s (#4 25 -> 15, #5 33 -> 24); #5's decline is shallower through its 66.7s hit (24% at 60s to 17% at 75s) than #4's through its 33.9s hit (36% at 25s to 25% at 40s).
- Draw #6 reached 54.6% stayed and 0:31 AVD at ~1 day old, with 33.3% average viewed (provisional). No retention curve is available yet, so the "plateau after 50s with two hits" question cannot be answered; recheck after ~Oct 30.
- Second batches: Draw #3 got a second small batch of 319 views on Oct 23, two days after publishing (72 views on Oct 22). None of #4, #5 or #1/#2 did: #4 fell 1,095 -> 163 -> 107 -> 59 -> 101, #5 969 -> 81 -> 125. Draw #6 has 208 views on Oct 28 so far (869 on day 1).
- Likes: #4 30 (19.6 per 1k views, the best so far), #5 11 (9.4 per 1k), #6 15 (13.9 per 1k at 1,077 views), #1 21, #2 6, #3 8. Comments: 0 on all six episodes. Shares: 0. Subscribers: #4 +2, #5 +2, #6 +1.
- Shorts feed share is 96-98% on all six (96.9 / 96.4 / 98.3 for #4 / #5 / #6), search is ~1-2%.
- TikTok is flat across all six: 256-333 views per post, 100% For You, 0 new followers, 0 comments, 0-1 saves. 2s retention ranges 33% (#5, the Crobat ex cold open) to 53% (#2); 19s retention is 6-14%. #5 has the lowest 2s, 5s, 10s and 19s retention of the six and the shortest average watch time (5.64s), the opposite of its YouTube result.

### Readings not obtained

- Draw #6 YouTube audience retention (page says not enough data yet), unique viewers for #6, and exact #5 unique viewers beyond the Oct 27 table.
- The 10s point on Draw #4 is the 0:09 tooltip (62%); the tooltip does not land on exact seconds in all cases.
- Draw #7's scheduled time of day on YouTube.
- Channel-level Advanced-mode Oct 28 daily column (not yet in the table).

### What the six episodes say (conclusions, 2026-10-28)

Stayed-to-watch by cold-open LINE, six episodes:

| Line family | Episodes | Stayed |
|---|---|---|
| Promise of a hit in the first words ("had this card", "had an EX") | #1 59.4, #2 58.9, #4 49.3, #6 54.6 (prov.) | 49-59% |
| Opens on a negative or a coincidence ("Three regular holos. And then this.", "the same card twice") | #5 33.5, #3 36.4 | 33-36% |

- The LINE, not the frame-one card, is what separates the swipe rates. #4 had a full-art IR on frame one and the old line and got 49%; #6 had a plain card on frame one and a promise line and got 55%; #5 had a Crobat ex on frame one and a negative line and got 33%. The 2026-10-23 conclusion ("swipe rate tracks the card") was wrong with three episodes; with six it is the first spoken words that matter. This matches the top Shorts: the voice names the result at 0.0s.
- Seconds watched: 25-31s on five episodes, 39s on #5. #5 is the only episode whose hook promised a LATE payoff ("And then this.") with the hit at 66.7s, and it held 46% at 30s / 24% at 60s / 17% at 75s vs 33% / 15% / 12% on #4. Viewers who accept a promise of a late payoff wait for it. Early hits still do not plateau (#4: 36% at 25s to 25% at 40s across the 33.9s Emboar).
- The feed behaviour is unchanged on all six: one batch of ~870-1,100 views on day one, 60-160 a day after, no second push (except #3's 319 on day three). Lifetime views 1,030-1,530.
- 0 comments and 0 shares on 7,400 YouTube views and 1,670 TikTok views across six episodes. The "Guess tomorrow's ball" prompt has not worked once.
- TikTok: 256-333 views, 5.6-8.4s average watch, 0 followers on every post. The 61s Creator Rewards floor is the only reason TikTok constrains the format.

Decision taken from this: two packs per short, 61-65s, the hook is a spoken promise of the best card in the first words, the best card lands at ~42s with the first pack's result before it, the short ends on the held card with no summary and no sign-off, and the comments prompt moves to the caption. Full plan: `plan-draw-08-onward.md`.

## Read 2026-11-07 (Draws #8 to #15, two-pack format, vs #1 to #7)

Source: YouTube Studio Advanced mode (Content, last 28 days, Oct 10 to Nov 6) plus per-video Engagement/Reach/Audience pages; TikTok Studio post list. Read via Claude in Chrome on 2026-11-07. #14 and #15 are 1-2 days old (provisional). #16 (Nov 7) and #17 (Nov 8) not yet public.

Video IDs: #8 qClOItxRM4w, #9 OmsCzhRepfM, #10 _eDNP7UVzyY, #11 Ad-RzaSuuvk, #12 L5OY7dQ84BA, #13 RWS_aenlarM, #14 jWJPijKbFd0, #15 VuJnhvHJ9fg, #16 Lzhef27k3yM, #17 1oivlJwG07w.

### YouTube, all Draws

| Draw | Format | Views | Unique viewers | Stayed to watch | AVD | Avg % viewed | Likes | Top geo | Hook line |
|---|---|---|---|---|---|---|---|---|---|
| #1 | 4-pack 1:42 | 1,242 | — | 59% | 0:31 | 31.1% | 21 | worldwide | (promise, card named) |
| #2 | 4-pack 1:38 | 1,036 | — | 59% | 0:30 | 31.0% | 6 | worldwide | (promise, card named) |
| #3 | 4-pack 1:32 | 1,350 | — | 36% | 0:27 | 30.2% | 8 | worldwide | (coincidence opener) |
| #4 | 4-pack 1:34 | 1,528 | 816 | 49% | 0:25 | 27.2% | 29 | US 33%, ID, BR, PH, AU | (promise) |
| #5 | 4-pack 1:38 | 1,182 | — | 33.5% | 0:39 | 39.8% | 11 | worldwide | (negative opener) |
| #6 | 4-pack 1:36 | 1,199 | — | 55% | 0:33 | 34.5% | 17 | worldwide | (promise) |
| #7 | 4-pack 1:48 | 843 | 443 | 47.6% | 0:39 | 36.8% | 12 | US 42%, ID, CA, BR | (promise) |
| #8 | 2-pack 1:02 | 149 | 49 | 33.3% | 0:25 | 40.5% | 0 | Romania 71% | "Two packs. The second one had this." |
| #9 | 2-pack 1:02 | 125 | 21 | 16.3% | 0:36 | 59.0% | 0 | Romania 90% | "This came out of the second pack." |
| #10 | 2-pack 1:03 | 201 | 78 | 39.1% | 0:19 | 31.7% | 2 | Romania 78% | "Two Journey Together packs. One of them had this." |
| #11 | 2-pack 1:02 | 91 | 46 | 46.9% | 0:25 | 41.7% | 3 | Romania 53%, US 18% | "The second pack had the Pokémon on its wrapper." |
| #12 | 2-pack 1:04 | 581 | 316 | 52.5% | 0:28 | 44.6% | 11 | ID 16%, PH 9%, IT 8%, RO 8%, US 6% | "An EX came out of the second pack." |
| #13 | 2-pack 1:02 | 198 | 48 | 21.7% | 0:17 | 28.3% | 1 | (not enough data) | "Temporal Forces, and this came out of it." |
| #14 | 2-pack 1:02 | 42 | 14 | n/a | 0:23 | 38.7% | 1 | not enough data | "The second pack had an Illustration Rare, and here it is." |
| #15 | 2-pack 1:04 | 84 | — | n/a | 0:24 | 39.1% | — | not enough data | "Two packs. The second one had a V card." |

Retention at 0:30 (Studio's note on the Engagement page): #8 32%, #9 56%, #10 20%, #12 36%, #13 18%, #7 42%.
Traffic: Shorts feed 92% (#8) and 97% (#4); the rest is search noise. Subscribers: #10 +1, all other two-packs 0. Comments 0, shares 0 on all two-packs. Channel total last 28 days: 9,861 views, 46 watch hours, +11 subs.

### TikTok, Draws #9 to #15 (post list, 2026-11-07)

255 / 261 / 268 / 264 / 269 / 282 / 255 views; likes 12 / 1 / 8 / 2 / 2 / 5 / 3; comments 0. Same ~260-view batch as every post since #1; nothing escaped it.

### What changed (facts only)

- Views per short fell from 843-1,528 (4-pack) to 42-581 (2-pack). Unique viewers fell from 443-816 to 14-316.
- Every two-pack short except #12 stayed inside a small Romanian test batch (53-90% Romania, 14-78 unique viewers). All 4-pack shorts and #12 went worldwide (US/ID/PH/BR-led).
- #12 is the only two-pack that escaped: 52.5% stayed to watch, 316 unique viewers, 581 views. It is also the only hook that names the rarity in the first words ("An EX came out"). The hooks that say "had this" / "this came out" stayed 16-39%.
- But the 4-pack shorts with weak hooks (#3 36%, #5 33.5%) still reached ~1,200-1,350 views, so stayed-to-watch alone does not explain the smaller first batch. Other things that changed at #8: length 1:32-1:48 -> 1:02-1:04, daily cadence instead of every 2 days, scheduled 10:00 PM EET publish, 2 packs instead of 4 in the title.
- Average % viewed rose (27-40% -> 28-59%) because the shorts are shorter; AVD did not rise (25-39s -> 17-36s). Viewers still leave at roughly the same second, not the same fraction.
- The targets in plan-draw-08-onward.md section 9: stayed >= 55% missed on all (best 52.5%); AVD >= 33s missed on all but #9 (0:36, 21 viewers); avg % viewed >= 50% hit only by #9; engaged/views >= 60% missed on all (#12 56%).
- The channel's July-Aug 2025 challenge shorts (no drum, 31-82s) got 240-1,119 views each: the same ~1k ceiling as the 4-pack drum shorts. Two different formats, same ceiling.

### What it says

1. The two-pack format did not fix the swipe (stayed 16-52% vs 33-59%) and did not lift AVD. Shorter did not mean "watched more of it" in seconds.
2. The hook grammar finding holds and got stronger: name the hit in the first words (EX, the wrapper Pokémon) and the stay goes to 47-53%; say "this" and it drops to 16-39%. The daily-rotation lines drifted into vague "had this" wording.
3. Something at the Oct 30 switch shrank YouTube's first batch from ~1k worldwide to ~50-100 local. Candidates: short length, daily cadence, scheduled publishing, two-pack title. Not separable from this data; needs an A/B on the remaining drum stock.
4. TikTok ignores all of it: every post gets ~260 views and dies. If TikTok matters, it needs its own first-3-seconds, not the YouTube file.
5. Neither of the channel's two formats so far (challenge 2025, drum 2026) has broken ~1.5k views. The ceiling is the format's shareability/rewatch, not pack count.
