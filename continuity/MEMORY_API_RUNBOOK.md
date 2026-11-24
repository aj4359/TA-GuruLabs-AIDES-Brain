# Private TA GuruLabs AIDE Memory Service, executable implementation
**Current status:** code + actual HTTP tests available, **not a durable hosted deployment**.

## Architecture
- `continuity/memory_api.py` exposes loopback-only HTTP JSON server; it cannot bind to a public interface.
- Token SHA256 digests and project scopes come from `TA_MEMORY_IDENTITIES_JSON` on the trusted host. An AIDE cannot select another identity through a request body. Tokens themselves are not committed.
- `GET /v1/context?project=SICARIO` gives approved memories for authenticated AIDE and same-project approved team knowledge, with a nonconfidential asset index.
- `POST /v1/memories/draft` records a sourced memory as draft; can be private or team.
- `POST /v1/memories/approve` requires founder role and a memory belonging to an authorised project.
- SQLite file is created outside the source repo, if `TA_MEMORY_DB` points to a private mounted directory. Each request opens and closes its own connection, retaining data across requests and service restarts when hosted on persistent disk.
- `GET /v1/health` requires authentication and confirms local API process is up, **not backup or remote access**.

## Start on a trusted laptop/private server
Generate distinct high-entropy tokens locally (for example with `python -c "import secrets; print(secrets.token_urlsafe(32))"`). Store the full tokens in a private password/secret manager and set only their SHA256 digests in the service JSON config. Replace these examples with your own credentials; never commit or paste real secrets to GitHub.

```bash
export TA_MEMORY_IDENTITIES_JSON='[
 {"name":"founder","role":"founder","token_sha256":"<64-char-sha256-of-secret-founder-token>","projects":["SICARIO","BARD"]},
 {"name":"CUTLASS","role":"aide","token_sha256":"<64-char-sha256-of-cutlass-token>","projects":["SICARIO","BARD"]},
 {"name":"MAESTRO","role":"aide","token_sha256":"<64-char-sha256-of-maestro-token>","projects":["SICARIO","BARD"]}
]'
export TA_MEMORY_DB='/private/durable/path/tagurulabs_memory.sqlite3'
python -m continuity.memory_api
```

Example request from a private host with valid token:
```bash
curl -H "Authorization: Bearer $CUTLASS_TOKEN" 'http://127.0.0.1:8767/v1/context?project=SICARIO'
```

**Never open this HTTP port on the public internet.** For remote agent use, a reviewed HTTPS private reverse proxy or equivalent service-to-service private transport, access policy, rate limits and secret rotation are mandatory.

## What is still unbuilt
1. Persistent hosting + trusted secret management for actual AIDE workers.
2. Full logging/access controls and memory source review/supersession migrations; localhost API is an MVP, not a security-certified service.
3. Connected CUTLASS/MAESTRO runtime adapters and real model-backed jobs.
4. Authenticated Drive media bridge; independent FFprobe worker and media restore QA.
5. Encrypted backups with a verified cross-host restore, data-deletion/retention rules and privacy assessment for regulated workloads.
6. Human approval interface to replace direct founder API call.

The **test suite** verifies real HTTP credentials, approval, project isolation, draft visibility and cross-AIDE isolation with synthetic data. A test in an ephemeral GitHub runner does not establish a permanent production AIDE.
