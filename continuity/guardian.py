#!/usr/bin/env python3
"""TA GuruLabs deterministic continuity guard; stdlib only."""
import argparse
import hashlib
import json
import pathlib
import sys

def validate(root, manifest):
    findings = []
    def add(level, code, message):
        findings.append({"severity": level, "code": code, "message": message})
    for key in ("id", "project", "canon", "protected_assets"):
        if key not in manifest:
            add("error", "SCHEMA", "Missing required key: " + key)
    if any(f["severity"] == "error" for f in findings):
        return findings
    if not isinstance(manifest["protected_assets"], list):
        add("error", "SCHEMA", "protected_assets must be a list")
        return findings
    for asset in manifest["protected_assets"]:
        path = asset.get("path", "")
        sha = asset.get("sha256")
        pp = pathlib.PurePosixPath(path)
        if not path or not isinstance(path, str) or pp.is_absolute() or ".." in pp.parts:
            add("error", "INVALID_PATH", "Invalid asset path: " + repr(path))
            continue
        p = root / path
        if not p.is_file():
            add("error" if asset.get("required", True) else "warning", "MISSING_ASSET", path)
            continue
        if sha and hashlib.sha256(p.read_bytes()).hexdigest().lower() != sha.lower():
            add("error", "HASH_DRIFT", path)
        elif not sha:
            add("warning", "UNPINNED_ASSET", path)
    for item in manifest.get("required_phrases", []):
        path, phrases = item.get("path", ""), item.get("phrases", [])
        p = root / path
        if not p.is_file():
            add("error", "MISSING_CANON_DOCUMENT", path)
            continue
        data = p.read_text(encoding="utf-8", errors="replace").casefold()
        for phrase in phrases:
            if phrase.casefold() not in data:
                add("error", "CANON_DRIFT", path + ": missing " + repr(phrase))
    for item in manifest.get("forbidden_phrases", []):
        path, phrases = item.get("path", ""), item.get("phrases", [])
        p = root / path
        if not p.is_file():
            continue
        data = p.read_text(encoding="utf-8", errors="replace").casefold()
        for phrase in phrases:
            if phrase.casefold() in data:
                add("error", "FORBIDDEN_CLAIM", path + ": " + repr(phrase))
    return findings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest", default="continuity/manifest.json")
    parser.add_argument("--out", default="continuity_report.json")
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    file = root / args.manifest
    if not file.is_file():
        report = {"status": "FAIL", "findings": [{"severity": "error", "code": "NO_MANIFEST", "message": str(file)}]}
    else:
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            findings = validate(root, data)
            report = {"status": "FAIL" if any(f["severity"] == "error" for f in findings) else "PASS", "project": data.get("project"), "findings": findings}
        except (ValueError, TypeError, KeyError) as exc:
            report = {"status": "FAIL", "findings": [{"severity": "error", "code": "INVALID_MANIFEST", "message": str(exc)}]}
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if report["status"] == "FAIL" else 0

if __name__ == "__main__":
    sys.exit(main())
