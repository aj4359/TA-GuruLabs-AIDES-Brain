(function(){
  const SENSITIVE_KEYS=['name','address','postcode','nationalInsurance','niNumber','utr','email','phone','employerReference','payrollId'];
  function clone(v){return JSON.parse(JSON.stringify(v));}
  function redactObject(obj){
    if(Array.isArray(obj)) return obj.map(redactObject);
    if(!obj||typeof obj!=='object') return obj;
    const out={};
    for(const [k,v] of Object.entries(obj)){
      if(SENSITIVE_KEYS.some(x=>k.toLowerCase().includes(x.toLowerCase()))) out[k]='[REDACTED]';
      else out[k]=redactObject(v);
    }
    return out;
  }
  function buildShareBundle(full,opts={}){
    const includeAudit=!!opts.includeAudit;
    const includeCaptureConfidence=!!opts.includeCaptureConfidence;
    const safe={
      product:'TA GuruLabs PAYE Forensics',
      generatedAt:new Date().toISOString(),
      disclaimer:'Possible reconstruction based on confirmed and manually entered information. This does not confirm HMRC internal reasoning.',
      summary:{
        taxYear:full.result?.taxYear,
        jurisdiction:full.result?.jurisdiction,
        hmrcStatedUnderpayment:full.result?.hmrcStatedUnderpayment,
        reconstructedUnderpayment:full.result?.reconstructedUnderpayment,
        difference:full.result?.difference,
        confidence:full.result?.confidence,
        warnings:full.result?.warnings||[]
      },
      evidenceLedger:clone(full.evidenceLedger||{}),
      scenarios:clone(full.result?.scenarios||[]),
      iya:clone(full.iya||null),
      provenance:clone(full.provenance||{})
    };
    if(!includeCaptureConfidence&&safe.evidenceLedger?.observed){
      safe.evidenceLedger.observed=safe.evidenceLedger.observed.map(({extractionConfidence,...rest})=>rest);
    }
    if(includeAudit) safe.calculationAudit=clone(full.result||{});
    return redactObject(safe);
  }
  function toText(bundle){
    const s=bundle.summary||{};
    const lines=[
      'PAYE FORENSICS — CUSTOMER CASE SUMMARY',
      '',
      bundle.disclaimer,
      '',
      `Tax year: ${s.taxYear||'—'}`,
      `Jurisdiction: ${s.jurisdiction||'—'}`,
      `HMRC stated figure: £${Number(s.hmrcStatedUnderpayment||0).toFixed(2)}`,
      `Our reconstruction: £${Number(s.reconstructedUnderpayment||0).toFixed(2)}`,
      `Difference: £${Number(s.difference||0).toFixed(2)}`,
      `Reconciliation state: ${s.confidence||'—'}`,
      '',
      'Possible contributing factors:'
    ];
    (bundle.scenarios||[]).slice(0,5).forEach((x,i)=>lines.push(`${i+1}. ${x.title} — ${x.detail||x.evidence||''}`));
    lines.push('','Evidence labels: Observed = confirmed/supplied fact; Inferred = calculated from facts; Illustrative = explanatory scenario only.');
    return lines.join('\n');
  }
  window.PAYEPrivacyExportV8={buildShareBundle,toText,redactObject};
})();