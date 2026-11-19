# TA GuruLabs — Retail Opportunity Discovery Desk

**Status:** proposed GitHub Actions research workflow; not a live continuously running agent. Schedule becomes operative only if this branch is approved/merged and GitHub Actions enables it. Runs **weekdays**, not 24/7. Automated output is a research queue, never a sales forecast.

## Mission
Find original, easy-to-deliver, low-support, repeatable digital retail offers for TikTok, Instagram, YouTube Shorts, Telegram and other permissible channels, while protecting the founder's priority of the **first verified paid customer**. No new subscriptions, paid ads, stock, unsolicited outreach, or extra ChatGPT scheduled-task slots.

## Team: one shared queue, clear accountability
- **Retail Scout**: collect public trend signals (with URLs and access dates), compare with customer problem discussions; search beyond UK only where rights/payment eligibility is confirmed.
- **Opportunity Analyst (AUREUS Finance + ARCHON)**: document real buyer, perceived pain, alternatives, expected price, fee-adjusted contribution and confidence. Stop projects with poor margins.
- **Product Inventor (ATLAS + Codex)**: prototype one extremely simple digital deliverable using existing TA GuruLabs rights and tools; prefer reuse rather than rebuilding.
- **Trend-to-Video Desk (Maestro + CUTLASS + Sales Genius)**: create original/licensed 15–45s demonstrations with understandable outcome and one validated action.
- **Commerce & Compliance (Compliance + Public Learning Desk + Haven)**: check copyright, privacy, UK consumer rights/VAT, accessibility, TikTok product rules, Telegram Stars for in-app digital purchases, checkout/delivery/test receipts and publishing rights.
- **Continuity Guardian**: ensure versions, provenance, approved originals and recoverability.

**No individual agent is continuously running merely because a role is described.** Only the GitHub research workflow runs when deployed; other roles are accountable handoffs to existing teams.

## Opportunity evidence card (required before green-light)
1. Trend/source link and retrieval date (not just viral views).
2. Actual buyer + recurring frustration + at least two independent intent signals, ideally real spending evidence.
3. Specific product, actual readiness, rights and scope; target channel and its rules.
4. Price, processing/platform fees, refund reserve, expected support/minutes, estimated margin (label estimates).
5. Original sample/working demo; one clear CTA and eligible Payhip or Telegram checkout.
6. 7-day small pilot: measured video views, product clicks, verified checkouts, refunds, cash received and feedback.
7. Decision: **test / improve / stop**. Do not auto-launch, charge, buy or advertise.

## Read-only scanner
Run `cd retail_desk && python -m unittest -v test_scout.py`, then `python retail_desk/scout.py`.
It attempts two publicly accessible feeds (Google Trends UK and Product Hunt), records source errors when sites block access and emits a JSON file of **unverified trend mentions**. Does not scrape logins, use private APIs, store customer details, publish, create products or take payments. Treat search titles as untrusted. No source availability guarantee, no claim that a result is commercially viable. Report is stored as a workflow artifact for 30 days, not permanent memory.

**Protocol:** read findings -> independent market validation -> approved product proof -> compliance + checkout QA -> Public Learning Desk launch -> actual purchase receipt. Do not mix x402 automated buyer payments with consumer social checkout until independently validated.
