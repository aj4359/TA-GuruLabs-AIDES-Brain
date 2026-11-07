# TA GuruLabs — Cinematic Sound Standard (v1)
**Owner:** Maestro (creative sound direction), supported by FilmOS, video/game directors, engineering, compliance and Continuity Guardian.
**Watchword:** FAT • FULL • CINEMATIC • CLEAN • INTELLIGIBLE.
**Scope:** All TA GuruLabs and JingWuMedia output containing sound: films, social videos, trailers, music, spoken explainers, product demos, animations, games, apps and notifications.

## Creative purpose
Audio must make the story or product feel intentional, immersive and emotionally compelling. "Fat" means controlled bass weight, body in the midrange and clear transients—not indiscriminate bass boosts, clipping, over-compression or deafening loudness. Product sounds should be restrained when appropriate; loud cinematic treatment is not suitable for every notification, accessibility scenario or spoken instruction.

## Canon-first starting rule
Preserve the ORIGINAL approved soundtrack, dialogue and sound-effects stems, raw captures, sample rate, tempo/timecode, timeline, source hashes, licences and previous approved mix. An editor must not silently replace approved music, create two simultaneous songs, strip requested sound effects or change their timing. The continuity source manifest includes the final approved mix's hash and target format. Where stems are unavailable, do not claim to separately adjust music vs FX from a single merged track.

## Audio production chain
1. **Source audit:** record file versions, source provenance, third-party licences, sample rates/channels, expected usage and rights status. Keep raw sources intact.
2. **Editorial sync:** map every foreground sound event to visible action. Gunfire, footfalls, physical contacts and transitions require a cue sheet with frame/time reference. Avoid false or redundant Foley.
3. **Mix architecture:** separate music, dialogue/VO, ambience, combat/FX, and transition stems; remove low-end rumble and mud where needed. Preserve intelligibility of speech, stereo clarity and mono compatibility.
4. **Cinematic weight:** use tasteful low-frequency control, dynamic contrast, punch, depth and atmosphere. Protect transients and avoid excessive pumping. Use automation/ducking to reveal important dialogue or dramatic hits. Select sounds for emotional impact, never generic synthetic fillers.
5. **Master for destination:** TikTok/mobile, streaming video, music master, podcast, live gameplay and app UX may require different deliverables. Start with platform specifications where published, not one fixed universal loudness preset. A sample screening reference can be auditioned around -16 to -14 LUFS integrated for loud short-form content when appropriate, with true peak around or below -1 dBTP, but these are **starting targets**, not guaranteed platform specifications and do not override artistic intent, measured program dynamics or broadcast requirements. Music distributors may request original dynamic masters.
6. **QA:** confirm true peak/no clipping, integrated and short-term loudness, left-right balance, phase/mono, intelligibility, noise, transient clarity, gaps, abrupt changes, stereo compatibility, start/end tails, codec/bitrate and complete decode. Blind compare against approved baseline at matched perceived loudness.
7. **Device acceptance:** listen on iPhone speaker, earbuds/headphones and normal speakers when possible. Do not claim device validation from FFmpeg tests alone.
8. **Version and provenance:** protect approved mixes, emit new WAV/FLAC stems where appropriate plus audience delivery format, with hashes, cue sheet and change log. Require user/director approval for substantial creative changes before replacing a locked mix.

## Role-specific rules
- **Maestro:** owns overall sonic identity, song mastering and mix-stem continuity; sign off music/FX balance.
- **FilmOS / Director:** maintain picture-to-sound cue sheet, effect timing, matching continuity, sound transitions and end titles.
- **Game audio AIDE:** preserve player-action feedback, positional/spatial cues and useful variation; respect device and accessibility volume preferences.
- **Product demo AIDE:** clear VO above background music, subtle UI cues, sensible default volumes.
- **Continuity Guardian:** check presence/version/hashes of required mix and cues where actual assets are available, flag missing signoffs, do not pretend acoustic quality can be certified from hashes.
- **Compliance/Publishing:** verify licences, artist contributions, volume-sensitive accessibility, platform specs and published media rights.

## Sicario locked reference
V26 iPhone-fixed picture + V26 cinematic audio preview are approved references. The original Deadman Walking song remains the **only** music; approved gunshots retain their relative prominence. The full premix measured approx -17.9 LUFS in the approved cinematic preview. That figure describes **that one mix**, not a master setting for other work. To lift music without raising the gunshots, edit independently from the separated stems; don't just normalise the composite. Keep V26 untouched and produce a new version for review.

## Quality gate (attach to every sound release)
- [ ] Original master and source/rights inventory present
- [ ] One intended music bed, no accidental duplicated song
- [ ] Dialogue understandable / music dynamic and impactful
- [ ] Effect contact points match video and remain physically credible
- [ ] Objective level/peak/dynamics/phase/mono/noise checks recorded
- [ ] Destination-specific delivery verified
- [ ] Device review recorded or explicitly pending
- [ ] Approved version kept, derivative and mix metadata documented
- [ ] Rights and IP evidence checked

**Status is never "cinematic QC passed" based solely on volume or an encoder exit code.**
