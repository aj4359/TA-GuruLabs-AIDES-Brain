(function(){
  function redactText(s=''){
    return String(s)
      .replace(/\b[A-Z]{2}\d{6}[A-D]\b/gi,'[NI REDACTED]')
      .replace(/\b\d{10}\b/g,'[UTR/ID REDACTED]')
      .replace(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi,'[EMAIL REDACTED]')
      .replace(/\b(?:\+44\s?7\d{3}|07\d{3})\s?\d{3}\s?\d{3}\b/g,'[PHONE REDACTED]');
  }
  function build(bundle, narrative, opts={}){
    const r=bundle.result||{};
    const observed=(bundle.evidenceLedger&&bundle.evidenceLedger.observed)||[];
    const inferred=(bundle.evidenceLedger&&bundle.evidenceLedger.inferred)||[];
    const illustrative=(bundle.evidenceLedger&&bundle.evidenceLedger.illustrative)||[];
    const scenarios=(r.scenarios||[]).slice(0,3).map(x=>({title:x.title,detail:x.detail,score:x.score,evidence:x.evidence}));
    const questions=[];
    if(r.difference>25) questions.push('Which income, pension, savings, benefit or earlier adjustment figures did HMRC use to produce this amount?');
    if(bundle.caseInput&&bundle.caseInput.newTaxCode) questions.push(`Why was tax code ${bundle.caseInput.newTaxCode} issued, and from what date was it operated?`);
    if(bundle.caseInput&&bundle.caseInput.previousSavingsEstimate!=null&&bundle.caseInput.savingsInterest!=null&&Number(bundle.caseInput.savingsInterest)!==Number(bundle.caseInput.previousSavingsEstimate)) questions.push('What savings-interest estimate is currently held, and what source supplied or triggered the change?');
    questions.push('Was the revised code operated cumulatively or on a Week 1/Month 1/non-cumulative basis?');
    const pack={
      title:'PAYE Forensics Customer Case Pack',
      generatedAt:new Date().toISOString(),
      disclaimer:'Possible reconstruction based on confirmed and manually entered information. This does not confirm HMRC internal reasoning or replace professional tax advice.',
      reconciliation:{hmrcStated:r.hmrcStatedUnderpayment,reconstructed:r.reconstructedUnderpayment,difference:r.difference,status:r.confidence},
      strongestPossibleCauses:scenarios,
      narrative:(narrative||[]).map(x=>({text:redactText(x.text),evidenceType:x.evidenceType,sourceIds:x.sourceIds||[],ruleIds:x.ruleIds||[]})),
      evidence:{observed:observed.map(x=>({fieldId:x.fieldId,target:x.target,value:x.value,sourceLabel:x.sourceLabel,evidenceType:'Observed'})),inferred,illustrative},
      questionsForHMRC:questions,
      unresolved:r.difference>25?['The supplied information does not closely reconcile with the HMRC figure. Check for missing or stale inputs.']:[],
      privacy:{redacted:true,includesCaptureConfidence:false,includesRawDocument:false}
    };
    if(opts.includeAudit) pack.adviserAudit={ruleSetId:r.ruleSetId,result:r,provenance:bundle.provenance||{}};
    return pack;
  }
  function toText(pack){
    const p=pack; const gbp=v=>'£'+Math.round(Number(v||0)).toLocaleString('en-GB');
    const lines=[p.title,'','Possible reconstruction — not confirmation of HMRC internal reasoning.','',`HMRC figure: ${gbp(p.reconciliation.hmrcStated)}`,`Our reconstruction: ${gbp(p.reconciliation.reconstructed)}`,`Difference: ${gbp(p.reconciliation.difference)}`,`Reconciliation: ${p.reconciliation.status}`,'','What the evidence says:'];
    p.narrative.forEach(x=>lines.push(`- [${x.evidenceType}] ${x.text}`));
    if(p.strongestPossibleCauses.length){lines.push('','Possible contributing factors:');p.strongestPossibleCauses.forEach(x=>lines.push(`- ${x.title}: ${x.detail}`));}
    if(p.questionsForHMRC.length){lines.push('','Questions to ask HMRC:');p.questionsForHMRC.forEach(x=>lines.push(`- ${x}`));}
    lines.push('','Privacy note: common personal identifiers are redacted by default; raw extraction confidence and uploaded-document content are excluded.');
    return lines.join('\n');
  }
  window.PAYECasePackV10={build,toText,redactText};
})();