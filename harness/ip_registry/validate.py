#!/usr/bin/env python3
"""Validate portfolio preservation register without mistaking metadata for backups."""
import json, pathlib, sys
ALLOWED={"PUBLIC","INTERNAL","CONFIDENTIAL_IP","RESTRICTED_DATA"}
STATES={"PENDING","PARTIAL","COPIED","RESTORE_VERIFIED"}
def check(data):
 errors=[];warnings=[];seen=set()
 if data.get("schema_version")!=1:errors.append("Unsupported registry schema")
 for p in data.get("projects",[]):
  ident=p.get("id")
  if not ident or ident in seen:errors.append("Missing or duplicate project ID")
  seen.add(ident)
  if p.get("classification") not in ALLOWED:errors.append(str(ident)+": bad classification")
  state=p.get("status")
  if state not in STATES:errors.append(str(ident)+": invalid state")
  if state in {"COPIED","RESTORE_VERIFIED"} and not p.get("backup_proof"):errors.append(str(ident)+": claimed backup lacks receipt")
  if state=="RESTORE_VERIFIED" and not p.get("restore_proof"):errors.append(str(ident)+": claimed restore lacks proof")
  if state in {"PENDING","PARTIAL"}:warnings.append(str(ident)+": preservation incomplete")
  if p.get("classification")=="RESTRICTED_DATA" and state in {"COPIED","RESTORE_VERIFIED"} and not p.get("restricted_storage_attestation"):errors.append(str(ident)+": restricted data requires protected storage attestation")
 if not data.get("projects"):errors.append("Missing project inventory")
 return errors,warnings
if __name__=="__main__":
 path=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "harness/ip_registry/projects.json")
 e,w=check(json.loads(path.read_text()))
 print(json.dumps({"status":"FAIL" if e else "PASS_WITH_GAPS" if w else "PASS","errors":e,"warnings":w},indent=2))
 sys.exit(1 if e else 0)
