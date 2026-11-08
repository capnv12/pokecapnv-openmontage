Read AGENT_GUIDE.md and PROJECT_CONTEXT.md first, then pick the best pipeline (likely Hybrid: my footage + supporting visuals). Inspect my source file before planning anything.

SOURCE
- File: projects/inbox/[FILL IN: file name, e.g. IMG_5878.MOV]
- One continuous take, NO speech, silent or ambient audio only.
- Content: a Pokemon TCG pack opening. A lotto drum is spun FOUR times to draw four numbers (all four draws happen first). Then the four matching numbered packs are opened, not necessarily in draw order, each card revealed one by one. The end of the take shows the hit(s).
- Episode: Draw #[FILL IN: episode number, e.g. 1]
- Channel: poke.capnv (YouTube Shorts and TikTok).

STEP 1: IDENTIFY BEFORE SCRIPTING
Sample frames and identify all four ball numbers drawn (with timestamps), the order the packs are opened in, the set each pack is from (from the wrapper and card set symbols), and every card revealed (name, set number, rarity) with timestamps. Put it all in a table and mark the hits. If you are not sure about a card, flag it instead of guessing. Show me the table for approval before writing anything.

FORMAT
Vertical 1080x1920, 30fps, English. Four packs per episode, all in ONE video. Target 75-90s total (hard floor 61s so TikTok Creator Rewards applies; hard cap 90s). If it runs long, speed up commons rather than exceed 90s. Never pad.

TIMELINE (placeholders like {N} and {set name} are filled in by you from Step 1)
- 0.0-1.2s: drum already spinning at frame 0 (no static intro, no logo card). Branded drum sting, identical every episode.
- 1.2-~8s: draw montage. All four ball reveals cut tight (~1.5s each). VO calls each number exactly on its reveal ("Ball twenty-four!"). Each number pops on screen and docks into a 4-ball tracker row at the top.
- Then the four packs in the order they are opened in the footage, ~17-19s each:
  - Chip: "Pack 2/4 - Ball {N} - {set name}". VO: one specific line about this set or its chase card.
  - Pack tear at 3-4x speed with foil-tear foley and whoosh. Cut all dead time (fumbling, pauses).
  - Commons/uncommons ~0.4-0.7s each with a tick SFX per card and a counter chip "card 3/11". Reverse holo slot ~1s.
  - Rare slot: music ducks, riser, slow push-in 100% to 115% over ~1.5s, reveal on an impact SFX with a subtle flash. If hit: freeze-frame, glow, rarity tag, hold 2s, full hype. If a standard holo rare: hold ~1.5s with a quick witty line.
  - When the pack is done, tick its ball off in the tracker row.
- Last 6-8s: 2x2 summary grid of the four rare-slot cards (from freeze-frames), hits glowing with rarity tags, plus the hits tally ("1 hit from 4 packs"). VO comment prompt about the next draw. Hard cut on motion back into the spinning drum so the last frame matches frame 0 (seamless loop). No subscribe card, no fade-out.

VOICEOVER (ElevenLabs)
- Always use ElevenLabs voice ID j5tCCNLGgyfbSDLRDXEi (custom British host voice, energetic and cheeky). Never switch voices.
- Persona: a third-person host/announcer character. Hype on the draw and on hits, cheeky British wit on duds. Short sentences, written for a British speaker.
- Never claim first-person feelings about the pulls.
- Every script must name this episode's sets, specific cards, rarities and the running hits tally. No reusable template body (YouTube "inauthentic content" policy).
- Fixed ritual lines: opener "The drum decides...", number calls "Ball {N}!" in the draw montage, sign-off "Pick tomorrow's four balls in the comments - the drum is waiting."
- Show me the script for approval before generating audio.

PRICES
No prices on screen. (Optional later: value chip only on hits over ~$5-10, "${value} - TCGplayer Market, {Mon YYYY}", plus an end line "Pack ${cost} -> Pulled ${value}".) Never use the words bet, odds, jackpot, gamble or lottery in VO, captions or titles.

CAPTIONS & GRAPHICS
- Keep all text inside the centered 900x1400 safe area: nothing in the bottom 350px or the right 160px.
- VO captions burned in, word-level, 2-4 words per chunk, max ~5 words/sec, bold rounded sans, white with a thick black stroke, active word in #FFCB05, placed above the card.
- Rarity chips in a lower band, only on hits. Small persistent chip top-left: "Draw #{episode}", next to the 4-ball tracker row.
- Card fills 55-70% of frame width during reveals; never cover card art.
- Do NOT use official Pokemon artwork, logos, anime clips, stock footage or AI-generated Pokemon. Only the cards in my footage may appear.

B-ROLL
Motion graphics, plus AI-generated clips/images via fal.ai where they add value (never AI-generated Pokemon, official artwork or logos). Ask me before each paid generation; fal.ai cap $0.50 per video.

AUDIO
- Only original or provably licensed audio. No Pokemon game/anime audio, no Content ID-claimable music (a claim blocks Shorts over 60s globally).
- Layers: foley (tear, slide, flip), branded drum/ball sting, low royalty-free bed under commons, riser before the rare slot, impact + shimmer on hits, separate dud sting. ElevenLabs for SFX. Music always ducked under the VO.

CONSTRAINTS
- Running on a Raspberry Pi 5 (CPU only, no GPU): no local AI image/video models. Render a low-res draft for my review before the final render.
- Total paid generation cap (ElevenLabs + fal.ai): $2 per video; ask before any paid generation.

DELIVERABLES
- Final MP4.
- Title: "Draw #{episode}: 4 balls, 4 packs - {best hit or intriguing detail}". No dollar figures in titles.
- Description and hashtags for YouTube Shorts and TikTok, branded for poke.capnv (end the description with a "next draw" comment prompt). Remind me to toggle the AI-generated content label on TikTok and the altered/synthetic disclosure on YouTube.
