export type AuditEvent = {
  sequenceNo: number;
  createdAt: string;
  actorId: string;
  eventType: string;
  policyDecision?: 'allow' | 'deny' | 'require_human_approval' | null;
  approverId?: string | null;
  eventHash: string;
  previousHash?: string | null;
  evidence?: Record<string, unknown>;
  outcome?: Record<string, unknown>;
};

export type GovernedTransaction = {
  transactionId: string;
  actorId: string;
  authorityLabel: string;
  confidence?: number;
  materiality?: number;
  canRevoke: boolean;
  canKill: boolean;
  chainVerified: boolean;
  checkpointVerified?: boolean;
  events: AuditEvent[];
};

const labels: Record<string, string> = {
  signal_observed: 'Signal observed',
  authority_checked: 'Authority checked',
  approval_requested: 'Approval requested',
  approval_granted: 'Approval granted',
  approval_denied: 'Approval denied',
  authority_revoked: 'Authority revoked',
  execution_started: 'Execution started',
  execution_killed: 'Execution killed',
  execution_completed: 'Execution completed',
  outcome_recorded: 'Outcome recorded',
};

export function GovernedTransactionPanel({ transaction }: { transaction: GovernedTransaction }) {
  const approval = [...transaction.events].reverse().find((event) => event.eventType === 'approval_granted');
  const outcome = [...transaction.events].reverse().find((event) => event.eventType === 'outcome_recorded');

  return (
    <section aria-labelledby={`tx-${transaction.transactionId}`} style={{ border: '1px solid #2b2923', background: '#0b0c0b', color: '#ece9df', padding: 20 }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', gap: 16, borderBottom: '1px solid #24251f', paddingBottom: 14 }}>
        <div>
          <div style={{ fontSize: 11, letterSpacing: '.16em', color: '#9a8a65' }}>AIDES TRUST CONTROL PLANE</div>
          <h2 id={`tx-${transaction.transactionId}`} style={{ margin: '8px 0 0' }}>Governed transaction</h2>
          <code style={{ fontSize: 11, color: '#aaa' }}>{transaction.transactionId}</code>
        </div>
        <div style={{ textAlign: 'right', fontSize: 12 }}>
          <div>{transaction.chainVerified ? 'CHAIN VERIFIED ✓' : 'CHAIN FAILED ✕'}</div>
          <div>{transaction.checkpointVerified ? 'CHECKPOINT VERIFIED ✓' : 'CHECKPOINT UNVERIFIED'}</div>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0,1.2fr) minmax(260px,.8fr)', gap: 18, marginTop: 18 }}>
        <div>
          {transaction.events.map((event) => (
            <article key={`${event.sequenceNo}-${event.eventHash}`} style={{ borderLeft: '2px solid #b8964f', background: '#0e100f', padding: '12px 14px', marginBottom: 10 }}>
              <small style={{ color: '#8c8d85' }}>#{event.sequenceNo} · {event.createdAt} · {event.actorId}</small>
              <strong style={{ display: 'block', margin: '6px 0' }}>{labels[event.eventType] ?? event.eventType}</strong>
              {event.policyDecision && <div>Policy: {event.policyDecision}</div>}
              {event.approverId && <div>Approver: {event.approverId}</div>}
              <code style={{ display: 'block', marginTop: 8, fontSize: 10, wordBreak: 'break-all', color: '#9c9b91' }}>{event.eventHash}</code>
            </article>
          ))}
        </div>

        <aside>
          <Fact label="WHO ACTED" value={transaction.actorId} />
          <Fact label="AUTHORITY" value={transaction.authorityLabel} />
          <Fact label="EVIDENCE" value={`Confidence ${transaction.confidence ?? '—'} · Materiality ${transaction.materiality ?? '—'}`} />
          <Fact label="APPROVER" value={approval?.approverId ?? 'Not approved'} />
          <Fact label="STOPPABLE" value={`${transaction.canRevoke ? 'REVOKE' : 'NO REVOKE'} / ${transaction.canKill ? 'KILL' : 'NO KILL'}`} />
          <Fact label="OUTCOME" value={outcome ? 'Recorded' : 'Pending'} />
          <div style={{ border: '1px solid #8a6b31', background: '#141109', padding: 12, marginTop: 12 }}>CONSEQUENTIAL ACTIONS: HUMAN GATE ENFORCED</div>
        </aside>
      </div>
    </section>
  );
}

function Fact({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ borderTop: '1px solid #24251f', padding: '11px 0' }}>
      <div style={{ color: '#8f907f', fontSize: 10, letterSpacing: '.1em' }}>{label}</div>
      <strong>{value}</strong>
    </div>
  );
}
