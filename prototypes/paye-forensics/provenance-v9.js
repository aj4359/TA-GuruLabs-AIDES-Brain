(function(){
  const SOURCES={
    PAYE11030:{title:'P2 notice of coding',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye11030'},
    PAYE11040:{title:'P2 notes',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye11040'},
    PAYE11020:{title:'P2 automatic notes for in-year changes',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye11020'},
    PAYE12040:{title:'Other coding deductions / coded-out income',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye12040'},
    PAYE12035:{title:'Benefits in kind in coding',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye12035'},
    PAYE13001:{title:'General coding principles',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye13001'},
    PAYE13002:{title:'P2/P6/P6T and S/C prefixes',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye13002'},
    TAXCODES:{title:'GOV.UK tax code meanings',url:'https://www.gov.uk/tax-codes/what-your-tax-code-means'},
    EMERGENCY:{title:'GOV.UK emergency tax codes',url:'https://www.gov.uk/tax-codes/emergency-tax-codes'},
    RATES:{title:'Income Tax rates and allowances',url:'https://www.gov.uk/income-tax-rates/current-rates-and-allowances'},
    SAVINGS:{title:'Tax on savings interest',url:'https://www.gov.uk/apply-tax-free-interest-on-savings'},
    DIVIDENDS:{title:'Tax on dividends',url:'https://www.gov.uk/tax-on-dividends'},
    SCOTLAND:{title:'Scottish Income Tax',url:'https://www.gov.uk/scottish-income-tax'}
  };

  const RULES={
    personalAllowance:{label:'Personal Allowance',sources:['RATES'],explain:'The reconstruction applies the tax-year Personal Allowance, subject to tapering where relevant.'},
    personalAllowanceTaper:{label:'Personal Allowance taper',sources:['RATES'],explain:'Above the statutory adjusted-net-income threshold the Personal Allowance is reduced according to the tax-year rule.'},
    startingRateSavings:{label:'Starting rate for savings',sources:['SAVINGS'],explain:'The available starting-rate band for savings is reduced by taxable non-savings income.'},
    personalSavingsAllowance:{label:'Personal Savings Allowance',sources:['SAVINGS'],explain:'The allowance depends on the customer’s tax-band position for savings.'},
    dividendAllowance:{label:'Dividend Allowance',sources:['DIVIDENDS'],explain:'The tax-year Dividend Allowance is applied before dividend rates.'},
    scottishNonSavings:{label:'Scottish non-savings rates',sources:['SCOTLAND'],explain:'Scottish taxpayers use Scottish bands for non-savings, non-dividend income.'},
    codedOutIncome:{label:'Coded-out income',sources:['PAYE12040','PAYE13001'],explain:'PAYE codes can collect tax on some untaxed income by reducing coding allowances.'},
    benefitsInKind:{label:'Benefits in kind',sources:['PAYE12035'],explain:'Taxable benefits can be included in the code and affect the customer’s PAYE position.'},
    p2Meaning:{label:'P2 coding notice',sources:['PAYE11030','PAYE11040'],explain:'A P2 explains how the customer’s code is made up and the items included in it.'},
    codePrefixes:{label:'S/C code prefixes',sources:['PAYE13002'],explain:'S and C prefixes indicate Scottish and Welsh PAYE treatment respectively.'},
    inYearNotes:{label:'In-year code-change notes',sources:['PAYE11020'],explain:'P2 automatic notes can reflect recognised in-year coding changes including IYA-related scenarios.'},
    emergencyBasis:{label:'Week 1 / Month 1 / X / NONCUM',sources:['EMERGENCY'],explain:'These markers indicate current-pay-period-only operation rather than cumulative treatment.'}
  };

  function attachRuleProvenance(result){
    const rows=[];
    const add=(area,ruleKey,detail,value)=>rows.push({area,ruleKey,label:RULES[ruleKey]?.label||ruleKey,detail,value,sources:RULES[ruleKey]?.sources||[]});
    add('allowance','personalAllowance','Personal Allowance used in reconstruction',result.personalAllowance);
    if(result.adjustedNetIncomeUsed>100000) add('allowance','personalAllowanceTaper','Allowance taper applied because adjusted net income exceeded threshold',result.adjustedNetIncomeUsed);
    add('savings','startingRateSavings','Starting-rate band available/used for savings',result.savingsStartUsed);
    add('savings','personalSavingsAllowance','Personal Savings Allowance used',result.personalSavingsAllowanceUsed);
    add('dividends','dividendAllowance','Dividend Allowance used',result.dividendAllowanceUsed);
    if(result.jurisdiction==='Scotland') add('jurisdiction','scottishNonSavings','Scottish non-savings rates applied',result.taxableNonSavings);
    (result.nonSavingsTax?.rows||[]).forEach(r=>rows.push({area:'non-savings-tax',ruleKey:r.ruleId,label:r.label||r.ruleId,detail:'Tax-band slice',value:r.amount,rate:r.rate,tax:r.tax,sources:[result.jurisdiction==='Scotland'?'SCOTLAND':'RATES']}));
    (result.savingsTax?.rows||[]).forEach(r=>rows.push({area:'savings-tax',ruleKey:r.ruleId,label:r.ruleId,detail:'Savings tax-band slice',value:r.amount,rate:r.rate,tax:r.tax,sources:['SAVINGS','RATES']}));
    (result.dividendTax?.rows||[]).forEach(r=>rows.push({area:'dividend-tax',ruleKey:r.ruleId,label:r.ruleId,detail:'Dividend tax-band slice',value:r.amount,rate:r.rate,tax:r.tax,sources:['DIVIDENDS']}));
    return {...result, provenanceRows:rows};
  }

  function explainRule(ruleKey){
    const r=RULES[ruleKey]; if(!r) return null;
    return {...r,sourceDetails:r.sources.map(id=>({id,...SOURCES[id]}))};
  }

  function sourceDetails(ids){return (ids||[]).map(id=>({id,...SOURCES[id]})).filter(x=>x.title)}

  window.PAYEProvenanceV9={SOURCES,RULES,attachRuleProvenance,explainRule,sourceDetails};
})();