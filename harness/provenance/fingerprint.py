#!/usr/bin/env python3
"""TA GuruLabs provenance evidence CLI, stdlib only.

This produces a file digest and an unsigned, self-asserted evidence record.
It DOES NOT provide a trusted timestamp, a verified signature, or proof of IP ownership.

Usage:
  python3 fingerprint.py create --file work.mp4 --project JWM-001 --asset-id JWM-001-v1 --out evidence/jwm.json
  python3 fingerprint.py verify --file work.mp4 --manifest evidence/jwm.json
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "ta-gurulabs.provenance.v1"
CHUNK = 1024 * 1024

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()

def canon(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")

def create(args):
    source = Path(args.file).resolve(strict=True)
    if not source.is_file():
        raise ValueError("Source must be a regular file")
    output = Path(args.out).resolve()
    if source == output:
        raise ValueError("Manifest cannot overwrite the source file")
    if output.exists() and not args.overwrite:
        raise FileExistsError("Manifest already exists; use a new version or --overwrite deliberately")
    parent = None
    if args.parent_manifest:
        parent_path = Path(args.parent_manifest).resolve(strict=True)
        parent = sha256_file(parent_path)
    record = {
        "schema": SCHEMA,
        "asset_id": args.asset_id,
        "project_id": args.project,
        "version": args.version,
        "publisher_brand": "TA GuruLabs",
        "created_record_at_utc": datetime.now(timezone.utc).isoformat(),
        "local_file_name": source.name,
        "file_size_bytes": source.stat().st_size,
        "sha256": sha256_file(source),
        "parent_manifest_sha256": parent,
        "claimed_contributors": args.contributor,
        "tools_or_aides": args.tool,
        "rights_status": args.rights_status,
        "licence_evidence_reference": args.licence_ref,
        "independent_timestamp": None,
        "signing_certificate": None,
        "c2pa_credential": None,
        "warning": (
            "Self-reported provenance record. Valid file hash is integrity evidence only: "
            "not proof of authorship, title, rights clearance, priority, or first publication."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(record, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    output.write_text(encoded, encoding="utf-8")
    proof = output.with_suffix(output.suffix + ".sha256")
    proof.write_text(sha256_file(output) + "  " + output.name + "\n", encoding="utf-8")
    print("CREATED:", output)
    print("SOURCE SHA256:", record["sha256"])
    print("MANIFEST SHA256:", sha256_file(output))
    print("NOTE: self-asserted unsigned record, not independent legal proof")
    return 0

def verify(args):
    source = Path(args.file).resolve(strict=True)
    manifest = Path(args.manifest).resolve(strict=True)
    record = json.loads(manifest.read_text(encoding="utf-8"))
    if record.get("schema") != SCHEMA:
        raise ValueError("Unsupported provenance schema")
    size = source.stat().st_size
    current = sha256_file(source)
    ok = size == record.get("file_size_bytes") and current == record.get("sha256")
    proof = manifest.with_suffix(manifest.suffix + ".sha256")
    receipt_ok = None
    if proof.exists():
        receipt_ok = proof.read_text(encoding="utf-8").split()[0] == sha256_file(manifest)
        ok = ok and receipt_ok
    print(json.dumps({
        "file_matches_manifest": size == record.get("file_size_bytes") and current == record.get("sha256"),
        "manifest_sidecar_matches": receipt_ok,
        "sha256_actual": current,
        "sha256_recorded": record.get("sha256"),
        "verified": ok,
        "warning": "Successful validation proves file matches this record; it does not prove authorship or prior rights."
    }, indent=2))
    return 0 if ok else 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    c = sub.add_parser("create")
    c.add_argument("--file", required=True)
    c.add_argument("--project", required=True)
    c.add_argument("--asset-id", required=True)
    c.add_argument("--out", required=True)
    c.add_argument("--version", default="1")
    c.add_argument("--parent-manifest")
    c.add_argument("--contributor", action="append", default=[])
    c.add_argument("--tool", action="append", default=[])
    c.add_argument("--rights-status", choices=["unverified", "partially-verified", "verified"],
                   default="unverified")
    c.add_argument("--licence-ref", action="append", default=[])
    c.add_argument("--overwrite", action="store_true")
    v = sub.add_parser("verify")
    v.add_argument("--file", required=True)
    v.add_argument("--manifest", required=True)
    args = parser.parse_args()
    try:
        return create(args) if args.action == "create" else verify(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
