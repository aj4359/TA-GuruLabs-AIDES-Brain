(function(){
  const CODE_SOURCE='GOVUK-TAX-CODES-2026';
  const MULTI_SOURCE='GOVUK-MULTIPLE-JOBS-2026';

  function parse(code){
    const raw=String(code||'').trim().toUpperCase().replace(/\s+/g,'');
    const result={raw,observed:true,sourceIds:[CODE_SOURCE],prefix:null,suffix:null,number:null,basis:'cumulative-or-unknown',meaning:[],flags:[]};
    if(!raw){result.flags.push('missing-code'); return result;}
    if(/^S/.test(raw)) result.prefix='S';
    else if(/^C/.test(raw)) result.prefix='C';
    const m=raw.match(/(\d+)/); if(m) result.number=Number(m[1]);
    if(/K\d+/.test(raw)) result.suffix='K';
    else {
      const letter=raw.match(/[A-Z]+$/); if(letter) result.suffix=letter[0];
    }
    if(/W1|M1|NONCUM|X/.test(raw)){result.basis='non-cumulative-observed';result.flags.push('emergency-or-noncumulative-marker');}
    if(/BR/.test(raw)) result.meaning.push('All income at this source is generally taxed at the basic rate.');
    if(/D0/.test(raw)) result.meaning.push('All income at this source is generally taxed at the higher rate.');
    if(/D1/.test(raw)) result.meaning.push('All income at this source is generally taxed at the additional rate.');
    if(/0T/.test(raw)) result.meaning.push('No Personal Allowance is being given at this source.');
    if(/NT/.test(raw)) result.meaning.push('No tax is deducted from this source in the circumstances represented by the code.');
    if(/K\d+/.test(raw)) result.meaning.push('A K code indicates deductions or untaxed income exceed the tax-free allowances represented in the code.');
    if(/L/.test(raw) && result.number!=null) result.meaning.push('L normally indicates entitlement to the standard Personal Allowance framework.');
    if(/M(?!1)/.test(raw)) result.meaning.push('M can indicate receipt of Marriage Allowance transferred from a spouse or civil partner.');
    if(/N/.test(raw) && !/NONCUM/.test(raw)) result.meaning.push('N can indicate transfer of part of the Personal Allowance to a spouse or civil partner.');
    if(result.prefix==='S') result.meaning.push('Scottish Income Tax rates apply to non-savings, non-dividend income at this PAYE source.');
    if(result.prefix==='C') result.meaning.push('Welsh tax-code prefix applies to this PAYE source.');
    if(result.number!=null && !/K\d+|BR|D0|D1|0T|NT/.test(raw)){
      result.indicativeTaxFreeAmount=result.number*10+9;
      result.meaning.push('The numeric element broadly represents the tax-free amount allocated to this PAYE source, subject to HMRC coding rules and rounding.');
    }
    return result;
  }

  function allowancePlanner({personalAllowance=12570,sources=[]}={}){
    const clean=(sources||[]).map((s,i)=>({id:s.id||`source-${i+1}`,name:s.name||`Source ${i+1}`,income:Math.max(0,Number(s.income||0)),code:parse(s.code),kind:s.kind||'employment'}));
    const totalIncome=clean.reduce((a,s)=>a+s.income,0);
    const usedBySource=clean.map(s=>{
      let codedAllowance=0;
      if(s.code.indicativeTaxFreeAmount!=null) codedAllowance=Math.min(s.income,s.code.indicativeTaxFreeAmount);
      return {...s,codedAllowance};
    });
    const codedTotal=usedBySource.reduce((a,s)=>a+s.codedAllowance,0);
    const available=Math.max(0,Number(personalAllowance||0));
    const apparentlyUnused=Math.max(0,Math.min(available,totalIncome)-codedTotal);
    const brIncome=usedBySource.filter(s=>/BR/.test(s.code.raw)).reduce((a,s)=>a+s.income,0);
    const opportunities=[];
    if(apparentlyUnused>0 && brIncome>0){
      opportunities.push({type:'possible-split-opportunity',evidenceType:'Inferred',sourceIds:[MULTI_SOURCE],amount:Math.min(apparentlyUnused,brIncome),title:'Some Personal Allowance may be unused while another source is fully taxed',explanation:'HMRC says unused Personal Allowance from a lower-paying main job may sometimes be allocated to another job, depending on the circumstances. This is a check-and-contact opportunity, not an automatic entitlement or instruction to change a code yourself.'});
    }
    if(clean.length>1){
      opportunities.push({type:'multi-source-check',evidenceType:'Observed',sourceIds:[MULTI_SOURCE],title:'Check which source is using your Personal Allowance',explanation:'With more than one job or pension, each source usually has its own tax code and HMRC recommends checking which source is using the Personal Allowance and whether estimated incomes are correct.'});
    }
    return {personalAllowance:available,totalIncome,codedAllowanceEstimate:codedTotal,apparentlyUnusedAllowance:apparentlyUnused,sources:usedBySource,opportunities,warning:'This is an allocation diagnostic, not a recommendation to alter a tax code. HMRC controls PAYE codes. Irregular income can make allowance splitting produce the wrong in-year deductions.'};
  }

  window.PAYETaxCodeInterpreterV11={parse,allowancePlanner,SOURCES:{CODE_SOURCE,MULTI_SOURCE}};
})();