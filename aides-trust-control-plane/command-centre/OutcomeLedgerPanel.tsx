type OutcomeStatus =
  | "unknown"
  | "observed"
  | "partial"
  | "achieved"
  | "not_achieved"
  | "reversed";

type OutcomeLedgerEntry = {
  transactionId: string;
  commissionedBy: string;
  deployedBy: string;
  action: string;
  intendedResult: string;
  observedResult?: string | null;
  status: OutcomeStatus;
  evidenceCount: number;
  confidence?: number | null;
  causationClaimed: boolean;
  learningRef?: string | null;
  stoppable: boolean;
};

const label: Record<OutcomeStatus, string> = {
  unknown: "INSUFFICIENT EVIDENCE",
  observed: "OBSERVED",
  partial: "PARTIAL",
  achieved: "ACHIEVED",
  not_achieved: "NOT ACHIEVED",
  reversed: "REVERSED",
};

export function OutcomeLedgerPanel({ entry }: { entry: OutcomeLedgerEntry }) {
  const confidence = entry.confidence == null ? "NOT CLAIMED" : `${Math.round(entry.confidence * 100)}%`;

  return (
    <section aria-label="Governed work outcome ledger" className="rounded-2xl border border-amber-300/20 bg-black/80 p-5 text-zinc-100">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs tracking-[0.28em] text-amber-200/70">TA GURULABS // OUTCOME LEDGER</p>
          <h2 className="mt-2 text-xl font-semibold">Governed Work Proof</h2>
          <p className="mt-1 font-mono text-xs text-zinc-500">{entry.transactionId}</p>
        </div>
        <span className="rounded-full border border-amber-200/30 px-3 py-1 text-xs tracking-wider">{label[entry.status]}</span>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-3">
        <ProofCell title="COMMISSIONED BY" value={entry.commissionedBy} />
        <ProofCell title="DEPLOYED BY" value={entry.deployedBy} />
        <ProofCell title="STOPPABLE" value={entry.stoppable ? "YES" : "NO"} />
      </div>

      <div className="mt-5 border-l border-amber-200/30 pl-4">
        <p className="text-xs tracking-wider text-zinc-500">AUTHORISED ACTION</p>
        <p className="mt-1 text-sm">{entry.action}</p>
        <p className="mt-4 text-xs tracking-wider text-zinc-500">INTENDED RESULT</p>
        <p className="mt-1 text-sm">{entry.intendedResult}</p>
        <p className="mt-4 text-xs tracking-wider text-zinc-500">OBSERVED RESULT</p>
        <p className="mt-1 text-sm">{entry.observedResult || "No verified outcome recorded yet."}</p>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-4">
        <ProofCell title="EVIDENCE" value={`${entry.evidenceCount} REF${entry.evidenceCount === 1 ? "" : "S"}`} />
        <ProofCell title="CONFIDENCE" value={confidence} />
        <ProofCell title="CAUSATION" value={entry.causationClaimed ? "CLAIMED" : "NOT CLAIMED"} />
        <ProofCell title="LEARNING" value={entry.learningRef ? "REFERENCED" : "NONE"} />
      </div>

      <p className="mt-5 text-xs leading-5 text-zinc-500">
        Observed outcomes do not automatically prove causation. Unknown outcomes remain visible rather than being converted into success claims.
      </p>
    </section>
  );
}

function ProofCell({ title, value }: { title: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.02] p-3">
      <p className="text-[10px] tracking-[0.2em] text-zinc-500">{title}</p>
      <p className="mt-2 text-sm font-medium">{value}</p>
    </div>
  );
}
