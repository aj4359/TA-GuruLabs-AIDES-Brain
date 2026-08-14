(function(){
  const FIELD_DEFS = [
    {id:'taxCode', label:'Tax code', hint:'Look near the employment or pension heading for a code such as 1257L, 0T, BR, D0, D1 or a K code.', target:'newTaxCode', type:'text'},
    {id:'employmentEstimate', label:'Estimated pay from this job', hint:'Look for the estimated annual pay or employment income figure shown for the PAYE source.', target:'employmentIncome', type:'money'},
    {id:'pensionEstimate', label:'Pension income', hint:'If the notice lists private or occupational pension income, copy the annual figure shown.', target:'privatePension', type:'money'},
    {id:'statePension', label:'State Pension', hint:'If State Pension is listed as an item affecting the code, copy the annual figure shown.', target:'statePension', type:'money'},
    {id:'benefits', label:'Benefits or expenses', hint:'Look for company car, medical benefit or another taxable benefit included in the code.', target:'benefitsInKind', type:'money'},
    {id:'savings', label:'Untaxed savings interest', hint:'Look for bank or building society interest, untaxed interest or savings income.', target:'savingsInterest', type:'money'},
    {id:'underpayment', label:'Earlier-year or in-year underpayment amount', hint:'If an amount is shown as tax owed, underpayment or adjustment, copy the actual tax amount, not just a code deduction.', target:'hmrcStatedUnderpayment', type:'money'}
  ];

  function normaliseMoney(v){
    const cleaned = String(v ?? '').replace(/[^0-9.-]/g,'');
    const n = Number(cleaned);
    return Number.isFinite(n) ? Math.max(0,n) : null;
  }

  function candidate(fieldId, rawValue, confidence, sourceLabel){
    const def = FIELD_DEFS.find(x=>x.id===fieldId);
    if(!def) throw new Error('Unknown capture field: '+fieldId);
    const value = def.type==='money' ? normaliseMoney(rawValue) : String(rawValue||'').trim().toUpperCase();
    return {
      fieldId, target:def.target, label:def.label, hint:def.hint,
      extractedValue:value,
      extractionConfidence: Math.max(0,Math.min(1,Number(confidence||0))),
      sourceLabel: sourceLabel || 'Uploaded coding notice',
      status:'needs-confirmation',
      evidenceType:'Observed once customer confirms',
      confirmedValue:null
    };
  }

  function confirm(item, confirmedValue){
    const def = FIELD_DEFS.find(x=>x.id===item.fieldId);
    const value = def.type==='money' ? normaliseMoney(confirmedValue) : String(confirmedValue||'').trim().toUpperCase();
    return {...item,status:'confirmed',confirmedValue:value,confirmedAt:new Date().toISOString(),evidenceType:'Observed'};
  }

  function reject(item){ return {...item,status:'rejected',confirmedValue:null,evidenceType:'Untrusted extraction'}; }

  function applyConfirmed(items, input){
    const next = {...input};
    items.filter(x=>x.status==='confirmed').forEach(x=>{ next[x.target]=x.confirmedValue; });
    return next;
  }

  function completeness(items){
    const total = items.length || 1;
    const confirmed = items.filter(x=>x.status==='confirmed').length;
    const rejected = items.filter(x=>x.status==='rejected').length;
    return {confirmed,rejected,total,ratio:confirmed/total};
  }

  // Demo candidates only. Production image extraction must be performed by an approved document/image pipeline,
  // with every extracted value explicitly confirmed by the customer before it can affect a calculation.
  function demoCandidates(){
    return [
      candidate('taxCode','1129L',0.96,'P2 coding notice'),
      candidate('employmentEstimate','£32,000',0.93,'P2 coding notice'),
      candidate('savings','£1,800',0.78,'P2 coding notice'),
      candidate('underpayment','£640',0.88,'P2 coding notice')
    ];
  }

  window.PAYECaptureAssistV6 = {FIELD_DEFS,candidate,confirm,reject,applyConfirmed,completeness,demoCandidates};
})();