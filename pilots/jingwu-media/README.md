# Jingwu Media Release Command (pilot)

A zero-dependency mobile-friendly prototype for managing release **evidence and approval stages**, not a live payment or publishing system.

## Run
Serve this directory using any static web server (ES modules need HTTP rather than file://):
```sh
python3 -m http.server 8080 --directory pilots/jingwu-media
```
Then open http://localhost:8080. On phone, host this as a private static preview first. Manifest is stored in browser localStorage. Do not treat localStorage evidence as authenticated approval or actual validation.

## Test
```sh
node --test pilots/jingwu-media/release-engine.test.mjs
```
Tests cover gated transitions, evidence presence, HTTPS publication URLs and settlement math. **These tests are not reported as executed by CI until a run is verified.**

## Limits / next engineering steps
- No connected Payhip, Spotify, YouTube, TikTok, distributor, database, queue or AIDE jobs yet.
- UI collects manually entered evidence labels, it does not independently validate ownership, authenticity of links, payment, or rights.
- Do not put secret credentials in fields. Public static hosting would disclose all JS code, so no private implementation or personal information.
- Add server-side authenticated approvals, durable datastore, API adapters with OAuth and scoped permissions, real media QA and successful purchase/download tests before public launch.
