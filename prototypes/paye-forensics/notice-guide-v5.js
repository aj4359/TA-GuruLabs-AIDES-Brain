(function(){
  const steps = [
    {id:'tax-code',title:'Find your tax code',hint:'Look for the code shown against the job or pension you are checking.',field:'newTaxCode',evidence:'Observed',sourceIds:['GOV-TAX-CODES-MEANING','HMRC-PAYE11030']},
    {id:'source',title:'Which job or pension is this for?',hint:'A P2 can show more than one live employment or pension. Pick the source that matches this code.',field:'sourceLabel',evidence:'Observed',sourceIds:['HMRC-PAYE11030']},
    {id:'allowances',title:'Find the allowances section',hint:'Enter any Personal Allowance, reliefs or expenses shown as additions to the code calculation.',field:'noticeAllowances',evidence:'Observed',sourceIds:['HMRC-PAYE11040']},
    {id:'deductions',title:'Find the deductions section',hint:'Enter deductions such as untaxed income, company benefits, State Pension or other items shown as reducing the tax-free amount.',field:'noticeDeductions',evidence:'Observed',sourceIds:['HMRC-PAYE11040','HMRC-PAYE12040']},
    {id:'state-pension',title:'Does the notice mention State Pension or taxable state benefits?',hint:'If yes, enter the annual amount shown or your best known figure. We will label it as customer-supplied, not HMRC-confirmed.',field:'statePension',evidence:'Observed',sourceIds:['HMRC-PAYE12040','HMRC-TAX-CODE-CHECKER']},
    {id:'benefits',title:'Does it mention a company benefit?',hint:'Examples can include medical insurance or a company car. Enter the amount shown on your notice if available.',field:'benefitsInKind',evidence:'Observed',sourceIds:['GOV-TAX-CODES-MEANING','HMRC-TAX-CODE-CHECKER']},
    {id:'other-income',title:'Does it mention untaxed income or interest?',hint:'Enter any untaxed income or savings figure shown. This can be one reason a code is reduced.',field:'savingsInterest',evidence:'Observed',sourceIds:['GOV-TAX-CODES-MEANING','HMRC-PAYE12040']},
    {id:'basis',title:'Do you see W1, M1, X or NONCUM?',hint:'These markers indicate an emergency/non-cumulative basis. Capture the marker exactly as shown.',field:'basisMarker',evidence:'Observed',sourceIds:['GOV-TAX-CODES-MEANING']},
    {id:'previous',title:'If you have an older coding notice, compare it',hint:'Enter the previous tax code and any previous income or savings estimates you can find. This powers the Tax Time Machine.',field:'oldTaxCode',evidence:'Observed',sourceIds:['HMRC-PAYE13001']},
    {id:'hmrc-figure',title:'Enter the HMRC underpayment or in-year adjustment figure',hint:'Use the figure HMRC has actually shown you. Our reconstruction will be compared against it rather than replacing it.',field:'hmrcStatedUnderpayment',evidence:'Observed',sourceIds:['HMRC-PAYE13001']}
  ];

  function buildChecklist(values={}) {
    return steps.map((s,index)=>({
      ...s,
      index:index+1,
      complete: values[s.field] !== undefined && values[s.field] !== null && String(values[s.field]).trim() !== ''
    }));
  }

  function buildEvidenceLedger(values={}, result=null) {
    const observed = steps.filter(s=>values[s.field] !== undefined && values[s.field] !== null && String(values[s.field]).trim()!=='').map(s=>({type:'Observed',label:s.title,value:values[s.field],sourceIds:s.sourceIds}));
    const inferred = result ? [
      {type:'Inferred',label:'Reconstructed underpayment',value:result.reconstructedUnderpayment},
      {type:'Inferred',label:'Difference from HMRC figure',value:result.difference},
      {type:'Inferred',label:'Reconciliation state',value:result.confidence}
    ] : [];
    const illustrative = result && result.iyaIllustration && result.iyaIllustration.indicativeExtraPerPayday != null ? [
      {type:'Illustrative',label:'Indicative extra amount per remaining payday',value:result.iyaIllustration.indicativeExtraPerPayday,note:'Illustration only; actual payroll collection depends on HMRC coding instructions and payroll timing.'}
    ] : [];
    return {observed,inferred,illustrative};
  }

  window.PAYENoticeGuideV5 = {steps,buildChecklist,buildEvidenceLedger};
})();
