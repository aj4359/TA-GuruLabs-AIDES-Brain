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

-- Atomic append RPC.
-- The transaction-scoped advisory lock serialises writers for a single
-- transaction_id, preventing two concurrent events from claiming the same
-- sequence number / predecessor hash. Hashing occurs in Postgres over a
-- canonical jsonb representation of the event payload.
create or replace function public.append_aides_audit_event(
  p_transaction_id uuid,
  p_actor_id text,
  p_actor_role text,
  p_event_type text,
  p_action text default null,
  p_resource text default null,
  p_policy_decision text default null,
  p_approver_id text default null,
  p_evidence jsonb default '{}'::jsonb,
  p_outcome jsonb default '{}'::jsonb
)
returns public.aides_audit_events
language plpgsql
security definer
set search_path = public, pg_catalog
as $$
declare
  v_previous_hash text;
  v_sequence_no bigint;
  v_payload jsonb;
  v_event_hash text;
  v_row public.aides_audit_events;
begin
  if p_event_type not in (
    'signal_observed','authority_checked','approval_requested','approval_granted','approval_denied',
    'authority_revoked','execution_started','execution_killed','execution_completed','outcome_recorded'
  ) then
    raise exception 'Unsupported event_type: %', p_event_type;
  end if;

  if p_policy_decision is not null and p_policy_decision not in ('allow','deny','require_human_approval') then
    raise exception 'Unsupported policy_decision: %', p_policy_decision;
  end if;

  if p_event_type = 'approval_granted' and nullif(btrim(p_approver_id), '') is null then
    raise exception 'approval_granted requires approver_id';
  end if;

  -- One writer at a time per governed transaction.
  perform pg_advisory_xact_lock(hashtextextended(p_transaction_id::text, 0));

  select event_hash, sequence_no
    into v_previous_hash, v_sequence_no
  from public.aides_audit_events
  where transaction_id = p_transaction_id
  order by sequence_no desc
  limit 1;

  v_sequence_no := coalesce(v_sequence_no, 0) + 1;

  v_payload := jsonb_build_object(
    'transaction_id', p_transaction_id,
    'sequence_no', v_sequence_no,
    'actor_id', p_actor_id,
    'actor_role', p_actor_role,
    'event_type', p_event_type,
    'action', p_action,
    'resource', p_resource,
    'policy_decision', p_policy_decision,
    'approver_id', p_approver_id,
    'evidence', coalesce(p_evidence, '{}'::jsonb),
    'outcome', coalesce(p_outcome, '{}'::jsonb)
  );

  v_event_hash := encode(
    digest(coalesce(v_previous_hash, '') || v_payload::text, 'sha256'),
    'hex'
  );

  insert into public.aides_audit_events (
    transaction_id, sequence_no, actor_id, actor_role, event_type,
    action, resource, policy_decision, approver_id, evidence, outcome,
    previous_hash, event_hash
  ) values (
    p_transaction_id, v_sequence_no, p_actor_id, p_actor_role, p_event_type,
    p_action, p_resource, p_policy_decision, p_approver_id,
    coalesce(p_evidence, '{}'::jsonb), coalesce(p_outcome, '{}'::jsonb),
    v_previous_hash, v_event_hash
  )
  returning * into v_row;

  return v_row;
end;
$$;

-- Keep the append path privileged. In Supabase the service_role key bypasses
-- RLS and may execute this function from trusted server code. Browser/client
-- roles are explicitly denied.
revoke all on function public.append_aides_audit_event(uuid,text,text,text,text,text,text,text,jsonb,jsonb) from public;
revoke all on function public.append_aides_audit_event(uuid,text,text,text,text,text,text,text,jsonb,jsonb) from anon, authenticated;
grant execute on function public.append_aides_audit_event(uuid,text,text,text,text,text,text,text,jsonb,jsonb) to service_role;

-- Deliberately no UPDATE or DELETE policy. A stored event is never rewritten.
-- Production hardening should also use protected service credentials,
-- signing/key management, immutable or WORM-capable backup/retention, and an
-- independent timestamp/anchor where procurement/security requirements justify it.

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

-- Verification view: each event must point to the immediately preceding hash.
create or replace view public.aides_audit_chain_verification as
with ordered as (
  select
    transaction_id,
    sequence_no,
    previous_hash,
    event_hash,
    lag(event_hash) over (partition by transaction_id order by sequence_no) as expected_previous_hash
  from public.aides_audit_events
)
select
  transaction_id,
  bool_and(
    case
      when sequence_no = 1 then previous_hash is null
      else previous_hash = expected_previous_hash
    end
  ) as linkage_valid,
  count(*) as event_count
from ordered
group by transaction_id;
