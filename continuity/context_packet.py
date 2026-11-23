#!/usr/bin/env python3
"""Produce a bounded, approval-only context packet for a trusted local AIDE worker.
Development helper: the caller identity must be authenticated by the host;
never expose this CLI/database directly to untrusted users.
"""
import argparse, json, sqlite3, sys
from pathlib import Path
try:
    from aide_memory_store import connect, recall
except ImportError:
    from continuity.aide_memory_store import connect, recall

def context_packet(c, *, aide, project, max_memories=30):
    if not aide or not project: raise ValueError("aide and project required")
    if not 1 <= max_memories <= 100: raise ValueError("Invalid limit")
    memories=recall(c,aide=aide,project=project)[:max_memories]
    # Do NOT put confidential URLs, unpublished assets or raw source media in
    # the agent packet. This is an inventory reference, not asset authorization.
    rows=c.execute("""SELECT id,title,kind,version,rights,status,sha256,bytes
        FROM assets WHERE project=? AND confidentiality IN ('internal','public')
        ORDER BY created_at DESC LIMIT 100""",(project,)).fetchall()
    return {"contract":"tagurulabs-context-v1","aide":aide,"project":project,
       "status":"SCOPED_LOCAL_DATA_NOT_RUNTIME_AUTHENTICATED",
       "approved_memories":memories,"nonconfidential_asset_index":[dict(x) for x in rows],
       "note":"Requires caller authorization, actual source retrieval and rights/restore evidence before execution."}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",default=".private/jingwu_memory.sqlite3")
    p.add_argument("--aide",required=True)
    p.add_argument("--project",required=True)
    p.add_argument("--limit",type=int,default=30)
    args=p.parse_args()
    c=connect(args.db)
    print(json.dumps(context_packet(c,aide=args.aide,project=args.project,max_memories=args.limit),indent=2))
if __name__=="__main__":main()
