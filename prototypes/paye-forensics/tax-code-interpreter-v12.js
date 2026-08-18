(function(){
  const SOURCE_IDS={
    TAX_CODES:'GOVUK-TAX-CODES',
    MULTI_JOBS:'GOVUK-MULTIPLE-JOBS-2026',
    CURRENT_YEAR:'GOVUK-CHECK-INCOME-TAX-CURRENT-YEAR'
  };

  function clean(code){return String(code||'').trim().toUpperCase().replace(/\s+/g,'');}
  function numericAllowance(code){
    const m=clean(code).match(/^(?:S|C)?(\d+)([A-Z].*)?$/);
    if(!m) return null;
    return Number(m[1])*10;
  }
  function interpret(code){
    const c=clean(code);
    const out={code:c,jurisdiction:'UK',basis:'cumulative-or-unknown',allowance:null,signals:[],sourceIds:[SOURCE_IDS.TAX_CODES]};
    if(/^S/.test(c)){out.jurisdiction='Scotland';out.signals.push('Scottish PAYE prefix observed');}
    if(/^C/.test(c)){out.jurisdiction='Wales';out.signals.push('Welsh PAYE prefix observed');}
    if(/W1|M1|X|NONCUM/.test(c)){out.basis='non-cumulative-observed';out.signals.push('Non-cumulative marker observed');}
    if(/BR/.test(c)) out.signals.push('All taxable income at this source is generally taxed at basic rate');
    if(/D0/.test(c)) out.signals.push('All taxable income at this source is generally taxed at higher rate');
    if(/D1/.test(c)) out.signals.push('All taxable income at this source is generally taxed at additional rate');
    if(/0T/.test(c)) out.signals.push('No Personal Allowance is being given at this source');
    if(/NT/.test(c)) out.signals.push('No tax is deducted at this source under the code');
    if(/K\d+/.test(c)){out.signals.push('K code: deductions/untaxed income appear to exceed allowances');out.allowance=0;}
    else out.allowance=numericAllowance(c);
    if(/M(?!1)/.test(c)) out.signals.push('Marriage Allowance recipient marker may be present');
    if(/N/.test(c)) out.signals.push('Marriage Allowance transferor marker may be present');
    return out;
  }

  function mapAllowance(sources, personalAllowance){
    const pa=Number(personalAllowance||12570);
    const rows=(sources||[]).map((s,i)=>{
      const code=interpret(s.code);
      const income=Math.max(0,Number(s.income||0));
      const codedAllowance=code.allowance==null?0:Math.max(0,code.allowance);
      const effectiveUse=Math.min(income,codedAllowance);
      return {id:s.id||('source-'+(i+1)),name:s.name||('PAYE source '+(i+1)),income,code:s.code||'',interpreted:code,codedAllowance,effectiveUse};
    });
    const totalEffectiveUse=rows.reduce((a,b)=>a+b.effectiveUse,0);
    const apparentlyUnused=Math.max(0,pa-totalEffectiveUse);
    const fullyTaxedSources=rows.filter(r=>/BR|D0|D1|0T/.test(clean(r.code)) && r.income>0);
    const opportunity=apparentlyUnused>0 && fullyTaxedSources.length>0;
    const checks=[];
    if(opportunity){
      checks.push('Some Personal Allowance appears unused while another PAYE source is taxed without allowance. Check HMRC’s estimated income for each source and ask whether allocating unused allowance elsewhere is appropriate.');
    }
    if(rows.some(r=>r.income<r.codedAllowance && r.codedAllowance>0)) checks.push('At least one source has more coded allowance than its entered income, which may indicate spare allowance or simply an estimate mismatch.');
    if(rows.length>1) checks.push('With multiple jobs/pensions, review which source HMRC treats as the main source and whether any old source is still active.');
    return {personalAllowance:pa,rows,totalEffectiveUse,apparentlyUnused,opportunity,checks,sourceIds:[SOURCE_IDS.MULTI_JOBS,SOURCE_IDS.CURRENT_YEAR]};
  }

  function simulateShift(model,targetSourceId){
    const target=model.rows.find(r=>r.id===targetSourceId);
    if(!target) return {ok:false,reason:'target-not-found'};
    const movable=Math.min(model.apparentlyUnused,target.income);
    return {ok:true,targetSourceId,movableAllowance:movable,warning:'Illustrative allocation scenario only. HMRC must issue any revised code, and total annual tax may be unchanged even if deductions move between sources.'};
  }

  window.PAYETaxCodeV12={interpret,mapAllowance,simulateShift,SOURCE_IDS};
})();