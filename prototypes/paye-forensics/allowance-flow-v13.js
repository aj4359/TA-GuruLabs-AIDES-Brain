(function(){
  function n(v){ const x=Number(v); return Number.isFinite(x)?Math.max(0,x):0; }
  function codeAllowance(code){
    const c=String(code||'').toUpperCase().trim();
    const stripped=c.replace(/^(S|C)/,'').replace(/\s+/g,'');
    if(/^K\d+/.test(stripped)) return {type:'negative',amount:0,negative:(parseInt(stripped.match(/^K(\d+)/)[1],10)+1)*10};
    if(/^(BR|D0|D1|0T|NT)/.test(stripped)) return {type:'none',amount:0,negative:0};
    const m=stripped.match(/^(\d+)[A-Z]/);
    return m?{type:'positive',amount:(parseInt(m[1],10)*10)+9,negative:0}:{type:'unknown',amount:null,negative:0};
  }
  function analyseSource(s){
    const income=n(s.income), parsed=codeAllowance(s.taxCode);
    const coded=parsed.amount==null?0:parsed.amount;
    const effective=Math.min(income,coded);
    const unused=Math.max(0,coded-effective);
    return {...s,income,parsed,codedAllowance:coded,effectiveAllowanceUsed:effective,apparentlyUnusedAllowance:unused,taxedWithoutAllowance:Math.max(0,income-effective)};
  }
  function analyse(sources, personalAllowance=12570){
    const rows=(sources||[]).map(analyseSource);
    const apparentUsed=rows.reduce((a,r)=>a+r.effectiveAllowanceUsed,0);
    const apparentCoded=rows.reduce((a,r)=>a+r.codedAllowance,0);
    const apparentUnusedAtSources=rows.reduce((a,r)=>a+r.apparentlyUnusedAllowance,0);
    const apparentHeadroom=Math.max(0,n(personalAllowance)-apparentUsed);
    const fullRateSources=rows.filter(r=>['BR','D0','D1','0T'].some(k=>String(r.taxCode||'').toUpperCase().includes(k)) && r.income>0);
    const opportunities=[];
    if(apparentHeadroom>0 && fullRateSources.length){
      opportunities.push({type:'allocation-check',amount:Math.min(apparentHeadroom,fullRateSources.reduce((a,r)=>a+r.income,0)),targets:fullRateSources.map(r=>r.label||r.type||'PAYE source'),evidenceType:'Inferred',message:'Some Personal Allowance appears not to be effectively used while another PAYE source is taxed without allowance. Ask HMRC whether the allocation and estimated incomes are correct.'});
    }
    if(apparentCoded>personalAllowance*1.15){
      opportunities.push({type:'double-count-check',amount:apparentCoded-personalAllowance,evidenceType:'Inferred',message:'The combined numeric coded allowances appear materially above one standard Personal Allowance. This may be valid because codes can include other adjustments, so check the P2 breakdown rather than assuming an error.'});
    }
    return {personalAllowance:n(personalAllowance),sources:rows,apparentUsed,apparentCoded,apparentUnusedAtSources,apparentHeadroom,opportunities};
  }
  function simulateShift(model,targetIndex,amount){
    const shift=Math.min(n(amount),model.apparentHeadroom,n(model.sources[targetIndex]?.income));
    return {shift,targetIndex,target:model.sources[targetIndex],warning:'Illustrative only. HMRC must issue any revised code. Moving allowance between PAYE sources can change when and where tax is deducted without changing total annual tax.'};
  }
  window.PAYEAllowanceFlowV13={codeAllowance,analyseSource,analyse,simulateShift};
})();