(function(){
  const money = v => `£${Math.round(Number(v||0)).toLocaleString('en-GB')}`;
  const n = v => Math.max(0, Number(v || 0));

  function decodeCode(code){
    const raw=String(code||'').trim().toUpperCase();
    const out={raw, observed:true, kind:'unknown', numericAllowance:null, basis:null, notes:[]};
    if(!raw){out.notes.push('No tax code supplied.');return out;}
    if(/W1|M1|X/.test(raw)){out.basis='non-cumulative';out.notes.push('The code contains a Week 1/Month 1/X marker. Treat as non-cumulative for explanation purposes.');}
    else out.basis='not-explicitly-non-cumulative';
    if(raw==='BR'){out.kind='BR';out.notes.push('All taxable pay at this source is generally taxed at the basic rate.');return out;}
    if(raw==='D0'){out.kind='D0';out.notes.push('All taxable pay at this source is generally taxed at the higher rate.');return out;}
    if(raw==='D1'){out.kind='D1';out.notes.push('All taxable pay at this source is generally taxed at the additional rate.');return out;}
    if(raw==='0T'){out.kind='0T';out.notes.push('No Personal Allowance is available through this code.');return out;}
    if(raw.startsWith('K')){
      const m=raw.match(/K(\d{1,4})/);out.kind='K';if(m)out.numericAllowance=-(Number(m[1])*10+9);out.notes.push('K code indicates additions exceed available allowances; the numeric value is only an explanatory approximation.');return out;
    }
    const m=raw.match(/(\d{1,4})/);
    if(m){out.numericAllowance=Number(m[1])*10+9;out.kind=raw.includes('S')?'Scottish numeric':raw.includes('C')?'Welsh numeric':'numeric';out.notes.push('Numeric code translated to an indicative tax-free amount using the standard code-number convention.');}
    if(raw.includes('L'))out.notes.push('L suffix commonly indicates entitlement to the standard Personal Allowance framework.');
    if(raw.includes('M'))out.notes.push('M suffix can indicate receipt of Marriage Allowance transfer.');
    if(raw.includes('N'))out.notes.push('N suffix can indicate transfer of part of Personal Allowance to a spouse/civil partner.');
    if(raw.includes('T'))out.notes.push('T suffix indicates other calculations are needed to work out the allowance.');
    return out;
  }

  function buildTimeMachine(input,result){
    const events=[];
    const oldIncome=n(input.previousNonSavingsEstimate), nowIncome=n(result.nonSavingsGross);
    const oldSavings=n(input.previousSavingsEstimate), nowSavings=n(result.savingsGross);
    if(oldIncome||nowIncome)events.push({id:'income',label:'Income estimate',before:oldIncome,after:nowIncome,delta:nowIncome-oldIncome,importance:Math.min(100,Math.abs(nowIncome-oldIncome)/100+40)});
    if(oldSavings||nowSavings)events.push({id:'savings',label:'Savings estimate',before:oldSavings,after:nowSavings,delta:nowSavings-oldSavings,importance:Math.min(100,Math.abs(nowSavings-oldSavings)/20+40)});
    const oldCode=decodeCode(input.oldTaxCode), newCode=decodeCode(input.newTaxCode);
    if(oldCode.raw||newCode.raw)events.push({id:'code',label:'Tax code',before:oldCode.raw||'—',after:newCode.raw||'—',delta:(oldCode.numericAllowance!=null&&newCode.numericAllowance!=null)?newCode.numericAllowance-oldCode.numericAllowance:null,importance:75});
    if(n(input.secondJobIncome)>0)events.push({id:'second-job',label:'Second job',before:0,after:n(input.secondJobIncome),delta:n(input.secondJobIncome),importance:72});
    if(n(input.privatePension)+n(input.statePension)>0)events.push({id:'pension',label:'Pension income',before:0,after:n(input.privatePension)+n(input.statePension),delta:n(input.privatePension)+n(input.statePension),importance:65});
    if(n(input.benefitsInKind)>0)events.push({id:'benefit',label:'Taxable benefit',before:0,after:n(input.benefitsInKind),delta:n(input.benefitsInKind),importance:68});
    return {events:events.sort((a,b)=>b.importance-a.importance),oldCode,newCode};
  }

  function missingPieces(input,result){
    if(result.confidence!=='Unable to reconcile')return [];
    const checks=[];
    const add=(id,title,why,priority)=>checks.push({id,title,why,priority});
    if(!n(input.secondJobIncome))add('second-job','Was there another employer?','A second PAYE source can materially alter the code and tax bands.',90);
    if(!n(input.statePension))add('state-pension','Was State Pension in payment?','State Pension is taxable but normally paid without PAYE deducted, so another code may collect the tax.',88);
    if(!n(input.privatePension))add('private-pension','Was there a private or workplace pension?','A pension payer may operate a separate PAYE code.',75);
    if(!n(input.benefitsInKind))add('benefits','Any company car, medical cover or other taxable benefit?','Benefits can reduce the tax-free amount available through PAYE.',72);
    if(!n(input.savingsInterest))add('savings','Did HMRC have a savings-interest estimate?','Untaxed savings can be coded out through PAYE.',68);
    if(!input.oldTaxCode||!input.newTaxCode)add('codes','Can you find both the old and new tax codes?','The direction and basis of the code change can reveal a likely collection mechanism.',85);
    if(!n(input.taxAlreadyDeducted))add('deducted','Check tax already deducted year to date','A wrong tax-deducted input can make an otherwise correct reconstruction look wrong.',95);
    add('prior-adjustment','Was an earlier-year underpayment or other adjustment being collected?','Historic underpayments can be included in a code and are not visible from current-year income alone.',80);
    add('basis','Was the revised code Week 1 / Month 1?','A non-cumulative basis changes how the revised code operates during the year.',82);
    return checks.sort((a,b)=>b.priority-a.priority).slice(0,6);
  }

  function evidenceLedger(input,result){
    const rows=[]; const obs=(label,value)=>rows.push({label,value,state:'Observed'}); const inf=(label,value)=>rows.push({label,value,state:'Inferred'}); const ill=(label,value)=>rows.push({label,value,state:'Illustrative'});
    obs('HMRC stated amount',money(result.hmrcStatedUnderpayment)); obs('Tax already deducted',money(result.taxAlreadyDeducted));
    if(input.oldTaxCode)obs('Old tax code',String(input.oldTaxCode)); if(input.newTaxCode)obs('New tax code',String(input.newTaxCode));
    inf('Reconstructed tax due',money(result.taxDue)); inf('Reconstructed underpayment',money(result.reconstructedUnderpayment)); inf('Difference',money(result.difference));
    if(result.iyaIllustration&&result.iyaIllustration.indicativeExtraPerPayday!=null)ill('Indicative extra per remaining payday',money(result.iyaIllustration.indicativeExtraPerPayday));
    return rows;
  }

  function enrich(input,result){
    const tm=buildTimeMachine(input,result);
    return Object.assign({},result,{v4:{timeMachine:tm,missingPieces:missingPieces(input,result),evidenceLedger:evidenceLedger(input,result),codeLens:{old:tm.oldCode,new:tm.newCode}}});
  }

  window.PAYEForensicsV4={decodeCode,buildTimeMachine,missingPieces,evidenceLedger,enrich};
})();