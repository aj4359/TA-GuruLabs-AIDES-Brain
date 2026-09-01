create extension if not exists pgcrypto;

create table if not exists public.aides_audit_events (
  id uuid primary key default gen_random_uuid(),
  transaction_id uuid not null,
  sequence_no bigint not null,
  actor_id text not null,
  actor_role text not null,
  event_type text not null check (event_type in (
    'signal_observed','authority_checked','approval_requested','approval_granted','approval_denied',
    'authority_revoked','execution_started','execution_killed','execution_completed','outcome_recorded'
  )),
  action text,
  resource text,
  policy_decision text check (policy_decision in ('allow','deny','require_human_approval') or policy_decision is null),
  approver_id text,
  evidence jsonb not null default '{}'::jsonb,
  outcome jsonb not null default '{}'::jsonb,
  previous_hash text,
  event_hash text not null,
  created_at timestamptz not null default now(),
  unique(transaction_id, sequence_no),
  unique(event_hash)
);

create index if not exists aides_audit_events_tx_idx
  on public.aides_audit_events(transaction_id, sequence_no);

create index if not exists aides_audit_events_created_idx
  on public.aides_audit_events(created_at desc);

alter table public.aides_audit_events enable row level security;

revoke insert, update, delete on public.aides_audit_events from anon, authenticated;
grant select on public.aides_audit_events to authenticated;

-- Deliberately no UPDATE or DELETE policy.
-- Writes should be performed only by a privileged server-side service that:
-- 1. reads the previous event hash for the transaction,
-- 2. canonicalises the new event payload,
-- 3. computes SHA-256(previous_hash || canonical_payload),
-- 4. inserts exactly once.
--
-- Production hardening: use a protected service role, separate signing key/KMS,
-- immutable or WORM-capable backup/retention, and independent timestamp/anchor
-- where procurement/security requirements justify it.

create or replace view public.aides_audit_transaction_summary as
select
  transaction_id,
  min(created_at) as started_at,
  max(created_at) as last_event_at,
  count(*) as event_count,
  bool_or(event_type = 'approval_granted') as human_approved,
  bool_or(event_type = 'execution_killed') as was_killed,
  bool_or(event_type = 'authority_revoked') as authority_revoked,
  bool_or(event_type = 'execution_completed') as completed,
  bool_or(event_type = 'outcome_recorded') as outcome_recorded
from public.aides_audit_events
group by transaction_id;
