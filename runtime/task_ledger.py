"""TA GuruLabs AIDES OS: local, dependency-free durable work queue.

This is an intentionally safe orchestration substrate: it NEVER executes shell commands,
calls an LLM, publishes content, spends money, or connects to external services.
Only separately reviewed workers should consume approved tasks.
"""
import argparse
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

STATUSES = {"pending", "running", "blocked", "done", "failed"}
KINDS = {"research", "engineering", "quality_check", "release_review", "commercial_review"}
OWNERS = {"AUREUS", "HAVEN", "ARCHON", "CODEX", "SCOUT", "CONTINUITY_GUARD", "SALES_GENIUS"}
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
 id TEXT PRIMARY KEY,
 title TEXT NOT NULL,
 kind TEXT NOT NULL,
 owner TEXT NOT NULL,
 project TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'pending',
 approval TEXT NOT NULL DEFAULT 'not_required',
 acceptance TEXT NOT NULL,
 evidence TEXT,
 blocker TEXT,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit (
 seq INTEGER PRIMARY KEY AUTOINCREMENT,
 task_id TEXT NOT NULL,
 at TEXT NOT NULL,
 action TEXT NOT NULL,
 detail TEXT NOT NULL
);
"""
def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
def db(path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    return conn
def event(conn, task_id, action, detail):
    conn.execute("INSERT INTO audit (task_id,at,action,detail) VALUES (?,?,?,?)",
                 (task_id, now(), action, detail))
def add(conn, title, kind, owner, project, acceptance, approval="not_required"):
    if kind not in KINDS or owner not in OWNERS:
        raise ValueError("Unknown kind or owner")
    if approval not in {"not_required", "required"}:
        raise ValueError("Invalid approval policy")
    if not all(s and s.strip() for s in (title, project, acceptance)):
        raise ValueError("Title, project and acceptance criteria are mandatory")
    task_id = uuid.uuid4().hex[:12]
    stamp = now()
    with conn:
        conn.execute("""INSERT INTO tasks
        (id,title,kind,owner,project,status,approval,acceptance,created_at,updated_at)
        VALUES (?,?,?,?,?,'pending',?,?,?,?)""",
        (task_id,title,kind,owner,project,approval,acceptance,stamp,stamp))
        event(conn,task_id,"created",owner)
    return task_id
def change(conn, task_id, status, evidence=None, blocker=None):
    if status not in STATUSES: raise ValueError("Invalid status")
    with conn:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row is None: raise ValueError("Task not found")
        allowed = {
          "pending": {"running","blocked"},
          "running": {"done","failed","blocked"},
          "blocked": {"pending"},
          "failed": {"pending"},
          "done": set()
        }
        if status not in allowed[row["status"]]:
            raise ValueError("Invalid transition: %s to %s" % (row["status"],status))
        if status == "done" and not (evidence and evidence.strip()):
            raise ValueError("Completion requires an evidence reference")
        if status == "blocked" and not (blocker and blocker.strip()):
            raise ValueError("Blocked tasks require a reason")
        if row["approval"] == "required" and status == "running":
            raise ValueError("Requires explicit approval outside this queue; no approval API is implemented")
        conn.execute("""UPDATE tasks SET status=?, evidence=COALESCE(?,evidence),
        blocker=?,updated_at=? WHERE id=?""",(status,evidence,blocker,now(),task_id))
        event(conn,task_id,"status",status)
def list_tasks(conn):
    return [dict(row) for row in conn.execute("SELECT * FROM tasks ORDER BY created_at,id")]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db",default="runtime/data/tasks.sqlite3")
    sub = parser.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("add")
    for arg in ("title","kind","owner","project","acceptance"):p.add_argument("--"+arg,required=True)
    p.add_argument("--approval",choices=("not_required","required"),default="not_required")
    p=sub.add_parser("set")
    p.add_argument("id");p.add_argument("status",choices=sorted(STATUSES))
    p.add_argument("--evidence");p.add_argument("--blocker")
    sub.add_parser("list")
    args=parser.parse_args()
    conn=db(args.db)
    if args.cmd=="add":
        print(add(conn,args.title,args.kind,args.owner,args.project,args.acceptance,args.approval))
    elif args.cmd=="set":
        change(conn,args.id,args.status,args.evidence,args.blocker)
        print("updated",args.id)
    else:
        print(json.dumps(list_tasks(conn),indent=2))
if __name__=="__main__":
    main()
