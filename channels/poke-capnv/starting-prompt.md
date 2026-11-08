Read AGENT_GUIDE.md and PROJECT_CONTEXT.md first, then pick the best pipeline (likely Hybrid: my footage + supporting visuals). Inspect my source file before planning anything.

SOURCE
- File: projects/inbox/[FILL IN: file name, e.g. IMG_5878.MOV]
- One continuous take, NO speech, silent or ambient audio only.
- Content: a Pokemon TCG pack opening. A lotto drum is spun FOUR times to draw four numbers (all four draws happen first). Then the four matching numbered packs are opened, not necessarily in draw order, each card revealed one by one. The end of the take shows the hit(s).
- Episode: Draw #[FILL IN: episode number, e.g. 1]
- Channel: poke.capnv (YouTube Shorts and TikTok).

STEP 1: IDENTIFY BEFORE SCRIPTING
Sample frames and identify all four ball numbers (with the timestamp each one is shown), the order the packs are opened in, the set each pack is from (from the wrapper and card set symbols), and every card revealed (name, set number, rarity) with timestamps. Card timestamps must be the exact LANDING time of each card (the first frame where it is settled after the flip), checked on a 0.2s frame grid of each pack's card run. Rough "card is visible" times were up to 0.8s off in Draw #1 and broke the VO sync. Put it all in a table and mark the hits. If you are not sure about a card, flag it instead of guessing. Show me the table for approval before writing anything.

FORMAT
Vertical 1080x1920, 30fps, English. Four packs per episode, all in ONE video. Target 75-90s total (hard floor 61s so TikTok Creator Rewards applies). 90s is a soft target, not a hard cap: going a bit over is fine when the content earns it (Draw #1 ran ~1:46). Trim dead time and speed up commons before cutting good lines. Never pad.

TIMELINE (placeholders like {N} and {set name} are filled in by you from Step 1)
- 0.0-~2.8s: COLD OPEN TEASE. MOVING footage of the best hit being revealed (never a still image), 0.5x slow-mo with a slow push-in (100% -> 112%), full screen, no name, no rarity tag, no glow, caption below the card. VO: "So, one of these four packs had this card." Cut to the spinning drum only AFTER the VO line has finished (+0.15s), never mid-sentence. Drum sting on the cut. NO-HIT EPISODE HOOK (agreed on Draw #3, 2026-10-17): if there is no ex / Illustration Rare / Special Illustration Rare / Master Ball pattern, do NOT fake hype. Tease in this priority order: 1) a visible coincidence (the same card twice in one pack, a Pokémon and its evolution, a legendary at uncommon), 2) the best non-hit card (Poké Ball pattern, a holo with striking art), 3) a drum moment (ball 1, the same ball twice). The tease stays [conspiratorial] and literally true, and the claim must be ON SCREEN: if no single shot shows it, cut two moving reveal clips back to back inside the 2.8s (e.g. Draw #3: Poké Ball Archeops landing, hard cut on the word 'same' to the holo Archeops landing, push-in continuing across the cut) with the line "So, one of these four packs had the same card twice." Still propose the options as a table and let me pick.
- PACK ORDER RULE: the video follows the order the packs are OPENED in the footage (Draw #2: 46, 47, 22, 20), not the order the balls left the drum and not the tray order. The pack blocks, the 4-ball tracker (left to right), the summary tokens, the VO and the description all use this order. Each ball's reveal clip is taken from the draw section and placed in front of its pack. In the VO, don't say "first ball out" (that implies drum order); use "First up, ..." / "Then ..." / "Last one, ...".
- Then the packs in OPENING ORDER. Each pack block: its ball reveal, then its pack, ~17-19s each:
  - Ball reveal: number pops on screen and docks into the top-left chip.
  - Set chip: "#{N} - {set name}". VO: one specific line about this set.
  - Pack tear at 3-4x speed with foil-tear foley and whoosh. Cut all dead time (fumbling, pauses).
  - Commons/uncommons ~0.4-0.7s each with a tick SFX per card and a counter chip "card 3/11". The counter COUNTS THE ENERGY CARD as card 1 (so it matches VO lines like "Probopass at card seven" / "Card ten"). Reverse holo slot ~1s. If the VO uses a set number (e.g. "Bulbasaur, number one"), say "number", not "card", so it can't clash with the counter.
  - Rare slot: music ducks, riser, slow push-in 100% to 115% over ~1.5s, reveal on an impact SFX with a subtle flash. If hit: music drops out before the reveal, a slow-mo build (down to 0.2x) under the "card ten and- no way" line, freeze-frame, glow, rarity tag, hold for the whole hit line. If a standard holo rare: hold ~1.5s, "HOLO RARE" tag.

VO <-> FOOTAGE SYNC (mandatory)
- The FOOTAGE FOLLOWS THE VO, never the other way round. Every card name spoken in the VO must appear on screen exactly when its name is said, and every rare-slot name must land on the reveal frame.
- Do it with the ElevenLabs word timings: for each named card, take its on-screen time from the Step 1 card table and its spoken time from the line's alignment, then speed-ramp the card footage between named cards to hit them (unnamed stretches stay at normal speed; ramps up to ~3x are fine, that is still ~0.4s per card). Ball numbers land on their ball reveals the same way.
- If a line would overlap the previous one, stretch footage (slow-mo build, longer freeze hold) rather than letting the VO drift off its card.
- Before rendering, measure and print every named card's offset (spoken time vs on-screen time). Target <= 0.05s; anything over 0.25s is a bug to fix, not to ship. (channels/poke-capnv/build_timeline_reference.py next to this prompt, also projects/poke-capnv-draw-01/scripts/build_timeline.py: card_run() and the SFX/ducking code are a working reference.)
- Last ~10s: summary card of the hit(s) with rarity tag, the four ball tokens in opening order, left to right (hit ball(s) glowing), "{N} PACKS · {N} HIT". Then sign-off and a hard cut on motion back into the spinning drum so the last frame matches frame 0 (seamless loop). No subscribe card, no fade-out.

VOICEOVER (ElevenLabs)
- Voice: ElevenLabs voice ID g3gYSFX4zMCH0soBrygt (my designed voice: energetic young British Pokemon YouTuber). Never switch voices without asking.
- Model and settings: eleven_v3, stability 0.0, similarity 0.8, seed 1611, with_timestamps=true (keep the ElevenLabs .alignment.json for every line; captions are timed from it).
- Generate ONE LINE PER FILE (per script section). Do NOT generate continuous multi-line takes unless I ask.
- Every line starts with (or contains) a delivery tag that fits the moment, otherwise v3 reads plain statements like an ad: [conspiratorial] on the cold open, [upbeat] or [excited] on each new ball, [laughs] on a funny coincidence, [sighs] on dud rare slots, [gasps] + [excited] on the hit, [warmly] on the summary, [playful] on the sign-off. One or two tags per line, never stacked, never ALL-CAPS shouting. Lines with built-in reactions work best ("and- wait, Latios?", "Card ten and- no way."). Target energy: "a tiny bit below max", lively but not an ad voice.
- Post-processing (eleven_v3 ignores the speed setting): keep the raw file + its alignment, then make every edit at KNOWN positions and remap the ElevenLabs word timings through the same edits (channels/poke-capnv/process_vo.py (next to this prompt; also in projects/poke-capnv-draw-01/scripts/), does exactly this; copy it into the new project's scripts/ folder and run `python scripts/process_vo.py assets/audio/<vo dir>`):
  1. trim leading silence to 0.03s before the first word,
  2. shorten every internal pause longer than 0.15s to 0.15s,
  3. cut the tail glitch: ElevenLabs often leaves a 25-90ms burst after the final silence that follows the last word; cut at that silence (+0.06s) and make sure the last word is intact,
  4. speed up 1.15x with pitch preserved (atempo), 40ms fade-out.
  Write the processed alignment as <line>.mp3.alignment.json with the script's display spellings and the audio tags removed. Do NOT re-time captions with Whisper; the ElevenLabs alignment is the source of truth. Whisper is only for checking that the spoken words are right.
- Persona: FIRST PERSON, me (capnv) telling viewers about the draw. PAST TENSE ("had", "was"), because the video shows something that already happened. Spoken, not read: light interjections are fine ("okay", "wait", "and- no way", "oh, and"), run-on sentences are fine.
- Every line must say something specific that is visible in THIS footage: card names, card numbers, rarities, sets, odd coincidences (e.g. a Pokemon and its evolution in the same pack, a legendary printed as an uncommon, a secret rare numbered past the set, identical commons in two packs). Facts only from my footage; no prices, no made-up history about me.
- Reactions must sound natural, not patterned: at most ONE art/flavour description per episode (on the hit), at most one or two light jokes elsewhere; dud rare slots stay plain ("Rare slot was {card}. Regular holo."); commons lines just name the cards with the counter position where needed for sync. Any art detail spoken must be verified on a FULL-RESOLUTION frame first (a thumbnail read put Ditto "in a pile of Exeggcute"; it was a pile of stones).
- Scarlet & Violet pack structure: the last TWO cards are both hit slots (card 10 = reverse-holo slot that can be an Illustration Rare / Special Illustration Rare, card 11 = rare slot). Never call card 11 "the actual rare slot" or treat a card-10 hit as coming before the rare slot; a holo rare after a card-10 hit is just "and a {card} holo behind it".
- BANNED in VO: generic YouTuber filler ("here we go", "let's go", "come on, give me something", "I'll take that", "please, I'm asking nicely", "nine cards of nothing"); hit tallies ("zero for one", "zero for two", "one for three"); counting filler ("third of four", "third pack"); hints or callbacks to the cold-open tease ("not the one I showed you"); stale facts (e.g. calling a set "the newest" when it isn't, check release dates); "numbered past the set" as a selling point (the user finds it boring and meaningless for collecting; describe the art or the rarity instead); card-number trivia and counting coincidences (Pokédex-number matches, consecutive numbers, "one up from forty-six": the user finds all of it boring; name the card and its rarity, or describe the art); trivia that sounds forced ("so Fighting type, not Fire"); lines that only work with a setup the viewer won't remember. When in doubt, keep a dud line plain: "Rare slot was {card}. Regular holo."
- Sign-off (current test line): "Guess tomorrow's ball in the comments. The drum doesn't take requests, but it does take guesses." The drum draws randomly: viewers can only GUESS, never pick or request a number.
- Pronunciation: write "Pokémon" and "Ogerpon" plainly (respellings like "Poke-ay-mon" or "Oh-gur-pon" came out wrong). Respellings that worked: Floette -> Flo-ett, Hisuian -> Hiss-oo-ee-an, Kyogre -> Kai-ogre, Feraligatr -> Feraligator, Minccino -> Min-cheeno. Draw #2: Farigiraf -> Farry-jiraf; "ex" must be written "EX" (caps) or it is read as "x"; write "Paldea, Evolved" (comma) or the British voice inserts a linking R ("Paldea Revolved"); plain spelling was fine for Girafarig, Snivy, Silicobra, Orthworm, Iono, Misdreavus, Gothita, Maschiff, Tyranitar, Piloswine. Respellings with capitals or hyphens (Eye-OH-no, E X) get spelled out as letters; keep respellings lowercase and joined (eeyohno). Verify pronunciation clips with Whisper before asking the user to listen; it catches things like the linking R. For any NEW tricky name, generate 2-3 short pronunciation options and let me pick before batching. Draw #3 (2026-10-18): Zweilous -> zwylus, Wattrel -> wotrel, Haxorus -> haksorus; plain spelling was fine for Archeops, Dewott, Blitzle, Patrat, Sewaddle, Reshiram, Klang, Rookidee, Amoonguss, Eevee, Dudunsparce and "Poké Ball". Bulbapedia-style respellings (AR-kee-ahps, DOO-waht, puh-TRAT) read WORSE on this voice than plain spelling; don't feed them to v3. Captions always show the real spelling.
- Show me the script for approval before generating audio, then generate ONE sample line and wait for my OK before batching. After batching, give me a single listen-through file of all lines in order.

SCRIPT RECIPE (approved on Draw #2, 2026-10-17: "It has facts, entertaining, jokes, everything. Keep it for future runs")
- Ball line + a TRUE four-word hook for the set, in the style of "Twilight Masquerade, the Ogerpon mask set": "Paldea Evolved, the Iono set", "Journey Together, the Trainer's Pokémon set", "Black Bolt, the Zekrom set". The hook is the set's signature chase card, box legend or mechanic. Verify it.
- Expectations come from the SET, never from my mood: "One fifty-one, so there's a shot at the Charizard", "Mega Evolution, so there's a shot at a Mega ex". Never invent feelings ("I wasn't expecting much", "the one I wanted a hit from").
- Where the hook is visible in the pack, pay it off: "And there's one, Hop's Silicobra at card four."
- Run-up into a hit = fast name list ending on the dash: "Misdreavus, Sneasel, Gothita, Maschiff, Corviknight... nothing yet, and then card ten-" (music drops on the dash).
- Hit line: reaction, name, rarity, then ONE "look at it" art detail verified on a full-res frame: "No way. Farigiraf! Illustration Rare. Look at it, the whole herd of Girafarig down in the grass, and Farigiraf keeping watch."
- Card behind a card-10 hit: "Oh, and an Orthworm holo behind it. Poor Orthworm."
- A pack that builds: "Then Shelgon, Piloswine, and it kept building right up to the rare slot-" / "Tyranitar. All that armour, and still a regular holo." (one touch of colour from the card itself, e.g. its printed category).
- One joke per episode that ties the set hook to the card: "Rare slot, Ditto. Could've turned into a Charizard. Turned into a regular holo."
- Visible coincidences stay: "Servine at card ten, and right behind it- wait. Serperior ex! Snivy didn't make it, but the other two did."
- Packs where nothing happens get NO commons line: ticks and music carry the cards, VO returns at the rare slot.
- Summary calls back inside this video: "A Serperior ex. And a Farigiraf with its whole herd."
- Rejected on the way here (don't repeat): number trivia, "numbered past the set", art descriptions on every card, plain enumeration, invented feelings, stripping it down to bare statements ("you absolutely destroyed the script").
- Full approved Draw #2 script: projects/poke-capnv-draw-02/artifacts/script.json

PRICES
No prices on screen. (Optional later: value chip only on hits over ~$5-10, "${value} - TCGplayer Market, {Mon YYYY}", plus an end line "Pack ${cost} -> Pulled ${value}".) Never use the words bet, odds, jackpot, gamble or lottery in VO, captions or titles.

CAPTIONS & GRAPHICS
- Keep all text inside the centered 900x1400 safe area: nothing in the bottom 350px or the right 160px.
- VO captions burned in, word-level, 2-4 words per chunk, max ~5 words/sec, bold rounded sans, white with a thick black stroke, active word in #FFCB05, placed above the card.
- Rarity chips in a lower band, only on hits. Small persistent chip top-left: "Draw #{episode}", next to the 4-ball tracker row (opening order, left to right; each ball fills its slot when its pack block starts).
- Card fills 55-70% of frame width during reveals; never cover card art.
- Do NOT use official Pokemon artwork, logos, anime clips, stock footage or AI-generated Pokemon. Only the cards in my footage may appear.

B-ROLL
Motion graphics, plus AI-generated clips/images via fal.ai where they add value (never AI-generated Pokemon, official artwork or logos). Ask me before each paid generation; fal.ai cap $0.50 per video.

AUDIO
- Only original or provably licensed audio. No Pokemon game/anime audio, no Content ID-claimable music (a claim blocks Shorts over 60s globally).
- Layers: foley (tear, slide, flip), branded drum/ball sting, low royalty-free bed under commons, riser before the rare slot, impact + shimmer on hits, separate dud sting. ElevenLabs for SFX. Music always ducked under the VO.
- SFX may play under the VO ONLY if properly ducked: while a word is spoken, SFX sit ~8-12 dB below the voice (impacts on reveal words ducked hardest); between lines they return to full level. The VO must always stay clearly intelligible. Measure the overlaps before showing me a draft, don't just eyeball the volume numbers.
- How: measure each SFX/music/VO file's max momentary loudness (ffmpeg ebur128) once, set each SFX's volume from a target loudness (not a guessed 0.5-0.8: in Draw #1 the riser and dud sting peaked LOUDER than the voice that way), then duck per frame from a speech envelope built from the VO word timings (3-frame attack with look-ahead, 8-frame release) so every SFX under a word ends up >=10 dB below the VO. Music bed ~16 dB under the VO while speaking.
- If the music bed is shorter than the video, pause it during the silent music-drop before the hit and resume from the same point afterwards, rather than looping or stretching it.
- Check every VO file for a glitch/burst after the last word and trim it before mixing.

CONSTRAINTS
- Running on a Mac (Apple M1, 8 GB RAM): no local AI image/video models (not enough memory). Use VideoToolbox hardware decoding (`-hwaccel videotoolbox`) for the 4K HEVC source. This ffmpeg build has no `zscale`, so tonemap the HLG HDR footage to SDR another way and show me a frame comparison before the draft. Render a low-res draft for my review before the final render.
- Total paid generation cap (ElevenLabs + fal.ai): $2 per video; ask before any paid generation.

DELIVERABLES
- Final MP4.
- Title: "Draw #{episode}: 4 balls, 4 packs - {best hit or intriguing detail}". No dollar figures in titles.
- Description and hashtags for YouTube Shorts and TikTok, branded for poke.capnv (end the description with a "next draw" comment prompt). Remind me to toggle the AI-generated content label on TikTok and the altered/synthetic disclosure on YouTube.
- NO THUMBNAIL (my decision, 2026-10-18, from Draw #5 on): don't propose, build or compare thumbnails/covers. Publishing uses the platform's default frame picker.

When you get to scripting let me know to change the model. Once the script is ready let me know again before doing anything else, as I want to change the model again