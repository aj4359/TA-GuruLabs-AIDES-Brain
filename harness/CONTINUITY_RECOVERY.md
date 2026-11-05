# TA GuruLabs — Emergency Recovery & Durable Continuity (v1)
Owner: Anthony Johnson, Founder & Executive Producer
Created: 2026-11-05

## Accessible without ChatGPT
1. Private Google Drive Vault:
   https://drive.google.com/drive/folders/1w4C4v5sXJzsXSQ8E-MOTgLgGwtTn-UJ4
2. Private source repositories:
   https://github.com/aj4359/TA-GuruLabs-AIDES-Brain
   https://github.com/aj4359/TA-GuruLabs-Studio
3. Restorable Git history archives:
   https://github.com/aj4359/TA-GuruLabs-AIDES-Brain/releases/tag/continuity-AIDES-Brain-latest
   https://github.com/aj4359/TA-GuruLabs-Studio/releases/tag/continuity-TA-GuruLabs-Studio-latest

## If ChatGPT fails
- Open Drive and verify the vault files. Download original audio/video files (some large files are split into .part01, etc; see reassembly.json).
- Open GitHub independently, download the latest continuity ZIP from each Release.
- Check downloaded ZIP with .sha256. Extract. Run:
  git clone AIDES-Brain.bundle restored-AIDES-Brain
  git clone TA-GuruLabs-Studio.bundle restored-TA-GuruLabs-Studio
- If no Git installed, use each repository's Code > Download ZIP (latest sources only, no full history).
- Keep originals, third-party license data and creative briefs together. Rebuild from approved sources, not chat logs.
- Do not store recovery credentials or decryption keys in GitHub repos or public links.

## Current verified scope
- Google Drive: independent private folder contains selected JingWu master audio, portrait, important film cuts, seven+ supplied media sources, FilmOS source ZIP and inventory. This is an INITIAL partial creative backup, not an exhaustive TA GuruLabs archive.
- GitHub: code repositories remain independent; snapshot workflows trigger on push to main and daily; first release assets were verified present through GitHub.
- ChatGPT: current and past chat messages are NOT automatically exported; a new ChatGPT-only asset requires an explicit Drive transfer until a dedicated authenticated upload service exists.
- IPFS: NOT CONNECTED or pinned. IPFS is not a backup until encrypted, pinned and recoverability verified.
- Database: live Supabase/hosting database dumps and environment secret storage are NOT included. Back them up separately.

## Durability rules
- Follow a 3-2-1 approach: three verified copies, two storage systems, one independently accessible.
- Hash each file and build a manifest; new edits produce new hashes, not overwritten history.
- Verify backups at least daily; actually restore a representative file and Git bundle on a recurring schedule.
- Never expose unreleased intellectual property or personal/customer information on public IPFS.
- Preserve contracts and source licenses securely and separately from public media.

## Next technical integration
1. Select a durable off-ChatGPT media intake method, e.g. authenticated Google Drive API or a restricted storage bucket with service-account access.
2. Connect GitHub Actions upload to that second storage service using scoped credentials kept in GitHub Actions secrets, not chat.
3. Every new AIDE artifact uploads privately, records SHA256 and obtains server receipt before announcing 'backed up'.
4. Add signed C2PA and independent time-stamping to appropriate finished media (not blanket claims of authorship).
5. Test real restore on an independent device.
