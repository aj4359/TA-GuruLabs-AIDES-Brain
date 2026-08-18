(function(){
  const SOURCES = {
    PAYE90025:{title:'PAYE90025 — PAYE underpayments',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye90025',claim:'When a code amendment produces extra tax due, HMRC may include an IYA/IYAR to collect it over the remaining weeks or months and operate the code on week 1/month 1.'},
    PAYE13130:{title:'PAYE13130 — In Year Adjustments',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye13130',claim:'On a P2, IYA/IYAR may appear as estimated tax you owe (this year) and an adjustment for estimated tax you owe (this year).'},
    PAYE61205:{title:'PAYE61205 — review code',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye61205',claim:'HMRC manual guidance says a revised lower code must be issued on a week 1/month 1 basis in the circumstances described.'},
    GOV_EMERGENCY:{title:'GOV.UK — Emergency tax codes',url:'https://www.gov.uk/tax-codes/emergency-tax-codes',claim:'W1, M1, X or NONCUM mean tax is calculated for the current pay period rather than cumulatively for the whole tax year.'},
    PAYE12070:{title:'PAYE12070 — underpayments',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye12070',claim:'IYAs are distinct from the normal £2,999.99 coding limit for earlier-year underpayments; coding and collection depend on case circumstances.'}
  };

  const money=v=>Math.max(0,Number(v||0));
  const round2=v=>Math.round((v+Number.EPSILON)*100)/100;
  function hasNonCumMarker(code){return /(?:\bW1\b|\bM1\b|\bX\b|NONCUM)/i.test(String(code||''));}
  function numericAllowance(code){
    const c=String(code||'').toUpperCase().replace(/\s+/g,'');
    if(/^K\d+/.test(c)) return null;
    const m=c.match(/(\d{1,4})/); return m?Number(m[1])*10+9:null;
  }

  function analyse(input,result){
    const oldCode=String(input.oldTaxCode||'').trim().toUpperCase();
    const newCode=String(input.newTaxCode||'').trim().toUpperCase();
    const stated=money(input.hmrcStatedUnderpayment || result?.hmrcStatedUnderpayment);
    const remaining=Math.max(0,Math.floor(money(input.remainingPayPeriods)));
    const observedNonCum=hasNonCumMarker(newCode);
    const oldAllowance=numericAllowance(oldCode), newAllowance=numericAllowance(newCode);
    const numericLowering=oldAllowance!=null&&newAllowance!=null&&newAllowance<oldAllowance;
    const evidence=[];
    if(newCode) evidence.push({type:'Observed',id:'new-code',label:'New tax code',value:newCode,source:'customer-confirmed/manual'});
    if(oldCode) evidence.push({type:'Observed',id:'old-code',label:'Old tax code',value:oldCode,source:'customer-confirmed/manual'});
    if(stated>0) evidence.push({type:'Observed',id:'stated-iya',label:'HMRC stated underpayment / IYA',value:round2(stated),source:'customer-confirmed/manual'});

    const conclusions=[];
    if(observedNonCum){
      conclusions.push({type:'Inferred',id:'noncum-observed',label:'Non-cumulative basis is visible in the code',value:true,confidence:'high',sourceIds:['GOV_EMERGENCY'],explanation:'The code itself contains a W1/M1/X/NONCUM marker, so non-cumulative operation is directly supported by the observed code.'});
    } else if(numericLowering){
      conclusions.push({type:'Illustrative',id:'lower-code-w1m1-possible',label:'A lower revised code may be operated on W1/M1',value:true,confidence:'medium',sourceIds:['PAYE61205'],explanation:'The simple numeric allowance appears lower. HMRC manual guidance describes W1/M1 operation for a revised lower code, but the customer code shown does not itself prove the basis of operation.'});
    }

    if(stated>0){
      conclusions.push({type:'Illustrative',id:'iya-collection-route',label:'Possible IYA collection route',value:stated,confidence:'medium',sourceIds:['PAYE90025','PAYE13130'],explanation:'An in-year code amendment can generate an IYA/IYAR intended to collect extra tax over the remaining weeks or months. This describes a possible HMRC pathway, not a reconstruction of the hidden IYAR formula.'});
    }
    if(stated>0&&remaining>0){
      conclusions.push({type:'Illustrative',id:'equal-spread-visual',label:'Equal-spread visual only',value:round2(stated/remaining),confidence:'low',sourceIds:['PAYE90025'],explanation:'This divides the stated amount by the remaining pay periods only to help the customer visualise scale. Actual PAYE deductions can differ because the restriction, pay, tax bands, payroll timing and code basis matter.'});
    }

    const timeline=[];
    timeline.push({step:1,title:'A fact changes',body:'Income, savings, pension, benefits, employment history or another coding item may change.'});
    timeline.push({step:2,title:'HMRC may amend the code',body:'The revised code reflects updated allowances, deductions or other income information.',sourceIds:['PAYE61205']});
    if(stated>0) timeline.push({step:3,title:'Extra tax may be identified',body:`The figure entered for estimated tax owed / underpayment is £${stated.toLocaleString('en-GB')}.`,sourceIds:['PAYE90025','PAYE13130']});
    timeline.push({step:4,title:'Possible IYA / IYAR route',body:'HMRC guidance describes using an In Year Adjustment and restriction to collect extra tax over the remainder of the tax year.',sourceIds:['PAYE90025','PAYE13130']});
    timeline.push({step:5,title:observedNonCum?'Non-cumulative marker observed':'Code basis must be checked',body:observedNonCum?`The new code ${newCode} contains a non-cumulative marker.`:'Do not assume W1/M1 unless the notice, tax code or payroll evidence supports it.',sourceIds:['GOV_EMERGENCY','PAYE61205']});

    return {modelVersion:'PAYE-IYA-v8',observedNonCum,numericLowering,oldAllowance,newAllowance,evidence,conclusions,timeline,sources:SOURCES,warning:'This module explains a possible collection pathway. It does not calculate or claim to know HMRC’s internal IYAR restriction formula.'};
  }

  window.PAYEIYAModelV8={analyse,SOURCES,hasNonCumMarker,numericAllowance};
})();