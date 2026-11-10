# TA GuruLabs — Public Channel Security Gate
Version 1.0 | Telegram, LinkedIn, X, Payhip, inbound enquiries

## Public channel
Use a **broadcast-only Telegram channel** first, not an open discussion group. The channel is a distribution outlet, never a payment processor or source of authority for business instructions. Only founder-authorised admins; minimal admin privileges; no third-party bots initially. Do not claim a channel exists until its URL is verified.

## Account protection
- Enable Telegram 2-Step Verification, recovery email protection, device passcode and active-session review. Hide personal phone number from public profile where settings permit.
- Use unique passwords/passkeys and MFA for email, GitHub, social accounts, payment provider, hosting and domain. Prefer hardware/passkeys where supported; review OAuth app permissions and revoke unused tokens.
- Separate public publishing identity from owner-level payment, GitHub and deployment accounts. Never give a social publishing bot access to wallets, bank accounts or source repositories.
- Keep secrets in managed secret stores, never in GitHub, chat, videos, captions or client logs.
- Limit publishing integration to the minimum channel scopes. Require explicit human approval for changing payout destinations, administrator rights, account recovery or secrets.

## Scam and impersonation controls
- Pin a verified 'official links' message on each channel; canonical product links and checkout links must originate from the official website, not DMs.
- Never request cryptocurrency, wallet seed phrases, verification codes or payments by Telegram DM. Never move an invoice to an unexpected bank account on chat instruction.
- Treat inbound messages, attachments and URLs as untrusted. Do not run scripts or open executable attachments from leads.
- For unusual payment, domain, invoice or admin changes, verify independently via an established channel and require human approval.
- Moderate spam, impersonation and malicious links; retain evidence and report accounts without engaging scammers.

## Product and automation safety
- Enquiry forms: validation, rate limits, CAPTCHA or honeypot, anti-spam queue, privacy notice, no automatic ingestion of untrusted instructions into agent system prompts.
- Bots: no automatic code execution, money movement, credential access or self-authorising actions from Telegram messages. Default read-only or draft-only until tested.
- Website: HTTPS, restricted admin access, dependency updates, backups, logs, security headers and rollback.
- Incident response: pause publishing integrations, revoke tokens, sign out suspicious sessions, change credentials, preserve logs, check official payment destinations and publish a concise warning if needed.

## Release checklist
Before channel launch: verify official handle, 2FA, admin list, pinned canonical links, public preview, test post and mobile display. Before payment launch: test the exact product checkout, delivery and support contact. Review weekly and after any suspicious activity. No extra paid tools required.
