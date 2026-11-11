# TA GuruLabs — Plain English First

**Status:** Approved public-communications policy. Applies to every TA GuruLabs and JingWuMedia podcast, LinkedIn post, social caption, video title/card, website, demonstration and customer-facing description.

## The first-time visitor test
Within the first two sentences, tell an unfamiliar reader:
1. **Who is speaking?** TA GuruLabs is an independent technology/product studio; JingWuMedia is its music and creative production arm.
2. **What does it do?** Describe the work or problem in ordinary words.
3. **Why should I care?** Show the tangible benefit, example or story, and link to real work where relevant.

Explain specialist terms on first use, or replace them. Do not force the audience to learn our internal naming conventions.

## Preferred public words
| Internal term | First public mention |
| --- | --- |
| TA GuruLabs | TA GuruLabs, our independent technology and product studio |
| JingWuMedia | JingWuMedia, our music and creative production studio |
| AIDE / AIDEs | specialist digital assistants that help with research, production and other work; optionally: 'we call them AIDEs' |
| GMCH | our music creation and editing system; **do not invent an unverified formal expansion** |
| Agentic workforce | digital assistants working together on different tasks |
| HUNTR-X | our recruitment technology project; explain current product status |
| SIGMA | our experimental automated trading system (research, not proven profits) |
| Sicario: Dead Man Walking | an original crime-action story developed as a comic, cinematic project and game concept |
| MVP | first working version |
| API | a way for software services to exchange information |
| QA | quality checks |

Never use **AIDS** to mean our digital assistants. Use 'digital assistants' on first mention.

## Spoken / published content checklist
- [ ] First 5 seconds or opening line makes sense to a person who has never met us
- [ ] Plain-language summary precedes technical background
- [ ] Unfamiliar names/abbreviations are explained at first use
- [ ] A working product is clearly distinguished from a prototype, concept or planned feature
- [ ] The content does not invent customer outcomes, awards, partner endorsements, revenue or performance data
- [ ] Every promoted link works and points to the promised page or demonstration
- [ ] A relevant, strong image or **audible** video is attached and mobile-legible
- [ ] Sound is checked on a phone, and there is no duplicated music/voice track
- [ ] The introduction does not repeat unnecessarily; visuals and words match
- [ ] Music, clips, voices and faces are authorised for use
- [ ] Any personal or private founder material was approved for publication
- [ ] Caption, subtitle and voice pronunciation of names are checked
- [ ] A human confirms first-time channel connection, audience and publication result
- [ ] The post invites useful engagement rather than bulk unsolicited outreach

**Automation gate:** The text checker is advisory: it catches some jargon but cannot verify factual claims, media quality, platform availability or real-world publish status. Do not let a green automated check substitute for editorial review.

## An example
**Avoid:** "AIDES use GMCH with agentic workflows to optimise multimodal assets."

**Prefer:** "Our specialist digital assistants help us make and edit music videos using tools we've built ourselves. We're testing how to make the process faster and less expensive."

## Podcast format
- Introduce each host as a digital assistant, not as an undisclosed human.
- Open with the problem and personal stakes, then discuss what was tried, what worked and what failed.
- Use actual approved notes, public articles, and evidence. Do not read private conversations verbatim.
- Explain each branded product or acronym at first mention, even if an earlier episode explained it.
- Close with one concrete lesson and one relevant, optional way to explore or contribute.

## Implementation
Run `node scripts/check-public-copy.mjs <path-to-draft>` as a local editorial preflight (Node.js built-in modules only). Repair flagged expressions or deliberately explain them in context before publishing. No audience targeting or messaging is authorised by this rule.
