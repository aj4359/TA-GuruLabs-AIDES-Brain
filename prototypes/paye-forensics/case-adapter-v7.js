(function(){
  const DEFAULTS = {
    jurisdiction:'England & Northern Ireland',
    employmentIncome:0, secondJobIncome:0, privatePension:0, statePension:0,
    benefitsInKind:0, otherNonSavings:0, savingsInterest:0, isaIncome:0, dividends:0,
    taxAlreadyDeducted:0, hmrcStatedUnderpayment:0, previousNonSavingsEstimate:0,
    previousSavingsEstimate:0, oldTaxCode:'', newTaxCode:'', remainingPayPeriods:0,
    adjustedNetIncome:''
  };

  function ensureConfirmedKeyEvidence(items){
    const required = ['taxCode','employmentEstimate','underpayment'];
    const missing = required.filter(id => !items.some(x=>x.fieldId===id && x.status==='confirmed'));
    return { ok: missing.length===0, missing };
  }

  function buildCase(items, manualInput){
    const gate = ensureConfirmedKeyEvidence(items || []);
    if(!gate.ok) return { ok:false, reason:'evidence-gate-failed', missing:gate.missing };
    const seeded = {...DEFAULTS, ...(manualInput||{})};
    const observedInputs = window.PAYECaptureAssistV6.applyConfirmed(items, seeded);
    const observed = items.filter(x=>x.status==='confirmed').map(x=>({
      fieldId:x.fieldId, target:x.target, value:x.confirmedValue, sourceLabel:x.sourceLabel,
      extractionConfidence:x.extractionConfidence, confirmedAt:x.confirmedAt, evidenceType:'Observed'
    }));
    return {
      ok:true,
      caseInput: observedInputs,
      evidenceLedger:{ observed, inferred:[], illustrative:[] },
      captureAudit: items,
      provenance:{ adapter:'PAYE-CaseAdapter-v7', captureModel:'PAYE-CaptureAssist-v6' }
    };
  }

  function calculateCase(bundle){
    if(!bundle || !bundle.ok) throw new Error('Cannot calculate: evidence gate has not passed');
    const result = window.PAYEForensicsV2.calculate(bundle.caseInput);
    const inferred = [
      {id:'reconstructed-underpayment',label:'Reconstructed underpayment',value:result.reconstructedUnderpayment,evidenceType:'Inferred',ruleSetId:result.ruleSetId},
      {id:'reconciliation-difference',label:'Difference from HMRC stated amount',value:result.difference,evidenceType:'Inferred',ruleSetId:result.ruleSetId},
      {id:'confidence',label:'Reconciliation state',value:result.confidence,evidenceType:'Inferred',ruleSetId:result.ruleSetId}
    ];
    const illustrative = [];
    if(result.iyaIllustration && result.iyaIllustration.indicativeExtraPerPayday != null){
      illustrative.push({id:'indicative-extra-per-payday',label:'Illustrative extra per remaining payday',value:result.iyaIllustration.indicativeExtraPerPayday,evidenceType:'Illustrative',warning:result.iyaIllustration.warning});
    }
    return {...bundle, result, evidenceLedger:{...bundle.evidenceLedger,inferred,illustrative}};
  }

  function buildNarrative(bundle){
    const r=bundle.result;
    const savingsObs=bundle.evidenceLedger.observed.find(x=>x.target==='savingsInterest');
    const employmentObs=bundle.evidenceLedger.observed.find(x=>x.target==='employmentIncome');
    const underpaymentObs=bundle.evidenceLedger.observed.find(x=>x.target==='hmrcStatedUnderpayment');
    const facts=[];
    if(employmentObs) facts.push(`Your notice shows estimated pay of £${Number(employmentObs.value||0).toLocaleString('en-GB')}.`);
    if(savingsObs) facts.push(`Your notice shows £${Number(savingsObs.value||0).toLocaleString('en-GB')} savings interest.`);
    if(underpaymentObs) facts.push(`The amount you confirmed from the notice is £${Number(underpaymentObs.value||0).toLocaleString('en-GB')}.`);
    if(r.scenarios && r.scenarios[0]) facts.push(`${r.scenarios[0].title} is one of the strongest possible contributing factors from the information entered.`);
    facts.push(`Our reconstruction produces £${Number(r.reconstructedUnderpayment||0).toLocaleString('en-GB')}, a difference of £${Number(r.difference||0).toLocaleString('en-GB')} from the HMRC figure.`);
    return facts;
  }

  window.PAYECaseAdapterV7={DEFAULTS,ensureConfirmedKeyEvidence,buildCase,calculateCase,buildNarrative};
})();