import React from "react";

type InterventionStep = {
  stage: "DETECT" | "DENY" | "REVOKE" | "VERIFY_STOP";
  status: "COMPLETE" | "PENDING" | "BLOCKED" | "INSUFFICIENT_EVIDENCE";
  evidenceRef?: string | null;
  detail: string;
};

export type InterventionReplayProof = {
  proofId: string;
  feedMode: "SANITISED_DEMO" | "RECORDED_PROOF";
  worker: string;
  attemptedAction: string;
  enforcementStatus: "REQUESTED" | "EFFECTIVE" | "FAILED" | "UNKNOWN";
  mttiSeconds?: number | null;
  productionMttiClaimed: false;
  timeline: InterventionStep[];
};

export function InterventionReplayPanel({ proof }: { proof: InterventionReplayProof }) {
  const measured = proof.enforcementStatus === "EFFECTIVE" && proof.mttiSeconds != null;
  return (
    <section aria-label="Intervention proof" style={{background:"#090909",color:"#f4e7b2",border:"1px solid #725d25",borderRadius:18,padding:24,fontFamily:"Inter,system-ui,sans-serif"}}>
      <div style={{display:"flex",justifyContent:"space-between",gap:16,alignItems:"baseline",flexWrap:"wrap"}}>
        <div>
          <div style={{fontSize:12,letterSpacing:2,opacity:.7}}>AIDES OS · INTERVENTION PROOF</div>
          <h2 style={{margin:"8px 0 4px",fontSize:28}}>{proof.proofId}</h2>
          <div style={{opacity:.72}}>{proof.feedMode} · Worker {proof.worker}</div>
        </div>
        <div style={{textAlign:"right"}}>
          <div style={{fontSize:12,opacity:.7}}>EFFECTIVE INTERVENTION</div>
          <strong style={{fontSize:26}}>{proof.enforcementStatus}</strong>
        </div>
      </div>

      <div style={{marginTop:22,padding:16,border:"1px solid #302814",borderRadius:12}}>
        <div style={{fontSize:12,opacity:.65}}>ATTEMPTED ACTION</div>
        <div style={{marginTop:6,fontSize:18}}>{proof.attemptedAction}</div>
      </div>

      <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(170px,1fr))",gap:10,marginTop:18}}>
        {proof.timeline.map((step, index) => (
          <article key={step.stage} style={{padding:14,border:"1px solid #3d3219",borderRadius:12}}>
            <div style={{fontSize:11,opacity:.55}}>0{index + 1}</div>
            <strong>{step.stage.replace("_"," ")}</strong>
            <p style={{fontSize:13,lineHeight:1.45,opacity:.78,minHeight:56}}>{step.detail}</p>
            <div style={{fontSize:11}}>{step.status}</div>
            {step.evidenceRef && <code style={{display:"block",marginTop:7,fontSize:10,opacity:.55,overflowWrap:"anywhere"}}>{step.evidenceRef}</code>}
          </article>
        ))}
      </div>

      <div style={{display:"flex",gap:12,marginTop:18,flexWrap:"wrap"}}>
        <div style={{padding:"12px 16px",border:"1px solid #725d25",borderRadius:12}}>
          <div style={{fontSize:11,opacity:.65}}>MEASURED MTTI</div>
          <strong>{measured ? `${proof.mttiSeconds}s` : "INSUFFICIENT EVIDENCE"}</strong>
        </div>
        <div style={{padding:"12px 16px",border:"1px solid #302814",borderRadius:12}}>
          <div style={{fontSize:11,opacity:.65}}>PRODUCTION CLAIM</div>
          <strong>NO</strong>
        </div>
      </div>

      <p style={{margin:"18px 0 0",fontSize:12,lineHeight:1.5,opacity:.58}}>
        Controlled evidence replay only. The measured MTTI belongs to this recorded proof and is not a production latency or reliability claim.
      </p>
    </section>
  );
}
