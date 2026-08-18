(function(){
  function money(v){return '£'+Math.round(Number(v||0)).toLocaleString('en-GB')}
  function sentence(text,evidenceType,sourceIds=[],ruleIds=[],meta={}){
    return {text,evidenceType,sourceIds,ruleIds,meta};
  }
  function build(bundle){
    const r=bundle.result||{};
    const observed=(bundle.evidenceLedger&&bundle.evidenceLedger.observed)||[];
    const find=t=>observed.find(x=>x.target===t);
    const lines=[];
    const emp=find('employmentIncome');
    const sav=find('savingsInterest');
    const code=find('newTaxCode');
    const hmrc=find('hmrcStatedUnderpayment');
    if(emp) lines.push(sentence(`Your confirmed notice shows estimated employment income of ${money(emp.value)}.`,'Observed',[],[],{field:'employmentIncome',sourceLabel:emp.sourceLabel}));
    if(sav) lines.push(sentence(`Your confirmed notice shows savings interest of ${money(sav.value)}.`,'Observed',[],[],{field:'savingsInterest',sourceLabel:sav.sourceLabel}));
    if(code) lines.push(sentence(`Your confirmed tax code is ${code.value}.`,'Observed',['GOV-TAX-CODES'],[],{field:'newTaxCode',sourceLabel:code.sourceLabel}));
    if(hmrc) lines.push(sentence(`The underpayment or adjustment amount you confirmed is ${money(hmrc.value)}.`,'Observed',[],[],{field:'hmrcStatedUnderpayment',sourceLabel:hmrc.sourceLabel}));
    lines.push(sentence(`Our deterministic reconstruction produces a possible underpayment of ${money(r.reconstructedUnderpayment)}.`,'Inferred',['GOV-INCOME-TAX-RATES'],['RECON-UNDERPAYMENT'],{value:r.reconstructedUnderpayment}));
    lines.push(sentence(`That is ${money(r.difference)} away from the HMRC figure you entered.`,'Inferred',[],['RECON-DIFFERENCE'],{value:r.difference,confidence:r.confidence}));
    if(r.scenarios&&r.scenarios[0]) lines.push(sentence(`${r.scenarios[0].title} is one of the strongest possible contributing factors found from the information available.`,'Illustrative',r.scenarios[0].sourceIds||[],r.scenarios[0].ruleIds||[],{scenarioScore:r.scenarios[0].score}));
    if(r.iyaIllustration&&r.iyaIllustration.indicativeExtraPerPayday!=null){
      lines.push(sentence(`An equal-spread illustration would be about ${money(r.iyaIllustration.indicativeExtraPerPayday)} per remaining payday, but this is not HMRC's IYAR formula.`,'Illustrative',['PAYE90025','PAYE13130'],['IYA-EQUAL-SPREAD-VISUAL'],{warning:r.iyaIllustration.warning}));
    }
    return lines;
  }
  function audit(lines){return lines.map((x,i)=>({sentenceId:`S${String(i+1).padStart(3,'0')}`,...x}))}
  window.PAYENarrativeProvenanceV10={build,audit};
})();