-- Runtime enforcement persistence for the AIDES Trust Control Plane.
-- Kept separate from the validated v1 audit event enum so intervention
-- vocabulary can evolve without weakening the baseline audit contract.

create table if not exists public.aides_runtime_interventions (
  id uuid primary key default gen_random_uuid(),
  transaction_id uuid not null,
  actor_id text not null,
  intervention text not null check (intervention in (
    'deny','pause','revoke_credentials','quarantine','terminate'
  )),
  target_action text,
  reason text not null,
  state_before text,
  state_after text not null,
  credentials_active_after boolean not null,
  requested_by text not null,
  created_at timestamptz not null default now()
);

create index if not exists aides_runtime_interventions_tx_idx
  on public.aides_runtime_interventions(transaction_id, created_at);

alter table public.aides_runtime_interventions enable row level security;
revoke insert, update, delete on public.aides_runtime_interventions from anon, authenticated;
grant select on public.aides_runtime_interventions to authenticated;

create or replace function public.record_aides_runtime_intervention(
  p_transaction_id uuid,
  p_actor_id text,
  p_intervention text,
  p_target_action text,
  p_reason text,
  p_state_before text,
  p_state_after text,
  p_credentials_active_after boolean,
  p_requested_by text
)
returns public.aides_runtime_interventions
language plpgsql
security definer
set search_path = public, pg_catalog
as $$
declare
  v_row public.aides_runtime_interventions;
begin
  if p_intervention not in ('deny','pause','revoke_credentials','quarantine','terminate') then
    raise exception 'Unsupported intervention: %', p_intervention;
  end if;

  if nullif(btrim(p_reason), '') is null then
    raise exception 'Runtime intervention requires a reason';
  end if;

  insert into public.aides_runtime_interventions (
    transaction_id, actor_id, intervention, target_action, reason,
    state_before, state_after, credentials_active_after, requested_by
  ) values (
    p_transaction_id, p_actor_id, p_intervention, p_target_action, p_reason,
    p_state_before, p_state_after, p_credentials_active_after, p_requested_by
  ) returning * into v_row;

  return v_row;
end;
$$;

revoke all on function public.record_aides_runtime_intervention(uuid,text,text,text,text,text,text,boolean,text) from public;
revoke all on function public.record_aides_runtime_intervention(uuid,text,text,text,text,text,text,boolean,text) from anon, authenticated;
grant execute on function public.record_aides_runtime_intervention(uuid,text,text,text,text,text,text,boolean,text) to service_role;

create or replace view public.aides_runtime_intervention_summary as
select
  transaction_id,
  count(*) as intervention_count,
  bool_or(intervention = 'deny') as had_deny,
  bool_or(intervention = 'pause') as was_paused,
  bool_or(intervention = 'revoke_credentials') as credentials_revoked,
  bool_or(intervention = 'quarantine') as was_quarantined,
  bool_or(intervention = 'terminate') as was_terminated,
  max(created_at) as last_intervention_at
from public.aides_runtime_interventions
group by transaction_id;
