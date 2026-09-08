import React from "react";

type StageStatus = "complete" | "pending" | "blocked" | "unknown";

type MissionStage = {
  label: string;
  detail: string;
  status: StageStatus;
  evidenceRef?: string;
};

type MissionControlProof = {
  missionId: string;
  mission: string;
  commissionedBy: string;
  worker: string;
  budgetGbp: string;
  measuredCostGbp: string;
  outcome: string;
  verifiedValueGbp?: string;
  learningStatus: string;
  stages: MissionStage[];
};

const badge: Record<StageStatus, string> = {
  complete: "✓ COMPLETE",
  pending: "◌ PENDING",
  blocked: "■ BLOCKED",
  unknown: "? INSUFFICIENT EVIDENCE",
};

export default function MissionControlPanel({ proof }: { proof: MissionControlProof }) {
  return (
    <section style={{ background: "#070707", color: "#f4ead0", padding: 24, border: "1px solid #6d5720", fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace" }}>
      <header style={{ marginBottom: 22 }}>
        <div style={{ color: "#b99a43", letterSpacing: 3, fontSize: 12 }}>TA GURULABS · AIDES MISSION CONTROL</div>
        <h2 style={{ margin: "8px 0 4px", fontSize: 25 }}>{proof.mission}</h2>
        <div style={{ opacity: 0.65, fontSize: 12 }}>MISSION {proof.missionId} · COMMISSIONED BY {proof.commissionedBy}</div>
      </header>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(150px,1fr))", gap: 10, marginBottom: 22 }}>
        <Metric label="WORKER" value={proof.worker} />
        <Metric label="BUDGET" value={`£${proof.budgetGbp}`} />
        <Metric label="MEASURED COST" value={`£${proof.measuredCostGbp}`} />
        <Metric label="OUTCOME" value={proof.outcome} />
        <Metric label="VERIFIED VALUE" value={proof.verifiedValueGbp ? `£${proof.verifiedValueGbp}` : "UNKNOWN"} />
        <Metric label="LEARNING" value={proof.learningStatus} />
      </div>

      <div style={{ display: "grid", gap: 8 }}>
        {proof.stages.map((stage, index) => (
          <div key={`${index}-${stage.label}`} style={{ display: "grid", gridTemplateColumns: "34px minmax(150px,0.8fr) minmax(200px,1.4fr) minmax(150px,1fr)", gap: 12, alignItems: "center", padding: "12px 10px", borderTop: "1px solid #28220f" }}>
            <span style={{ color: "#b99a43" }}>{String(index + 1).padStart(2, "0")}</span>
            <strong>{stage.label}</strong>
            <span style={{ opacity: 0.78 }}>{stage.detail}</span>
            <span style={{ fontSize: 11 }}>{badge[stage.status]}{stage.evidenceRef ? ` · ${stage.evidenceRef}` : ""}</span>
          </div>
        ))}
      </div>

      <footer style={{ marginTop: 22, paddingTop: 14, borderTop: "1px solid #6d5720", fontSize: 11, opacity: 0.65 }}>
        Evidence view only. A completed stage does not prove causation. Unknown value remains unknown. Consequential work remains subject to authority and human gates.
      </footer>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ border: "1px solid #28220f", padding: 12, minHeight: 62 }}>
      <div style={{ color: "#b99a43", fontSize: 10, letterSpacing: 1.5 }}>{label}</div>
      <div style={{ marginTop: 8, fontSize: 14 }}>{value}</div>
    </div>
  );
}

export type { MissionControlProof, MissionStage, StageStatus };
