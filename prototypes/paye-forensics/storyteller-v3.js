(function(){
  const money = v => `£${Math.round(Number(v || 0)).toLocaleString('en-GB')}`;
  const pct = v => `${Math.round(Number(v || 0))}%`;

  function confidenceNarrative(result){
    if(result.confidence === 'Likely explanation') return {
      label:'Strong match',
      tone:'positive',
      copy:`Our reconstruction is very close to the HMRC figure. That makes this a plausible route to the amount shown, but it is not proof of HMRC's internal calculation.`
    };
    if(result.confidence === 'Possible explanation') return {
      label:'Plausible match',
      tone:'caution',
      copy:`Some of the figures line up, but there is still a meaningful gap. One or more estimates, coding adjustments or payroll details may be missing.`
    };
    return {
      label:'We found a mismatch',
      tone:'warning',
      copy:`The figures entered do not reproduce the HMRC amount closely enough. That is useful: it tells us what to check next instead of pretending the numbers agree.`
    };
  }

  function hero(result){
    const c = confidenceNarrative(result);
    return {
      eyebrow:'Your Tax Story',
      title:`HMRC says ${money(result.hmrcStatedUnderpayment)}`,
      subtitle:'Let’s reconstruct one possible route to that number.',
      confidence:c
    };
  }

  function sourceCards(input){
    const rows = [
      ['Employment', input.employmentIncome],
      ['Second job', input.secondJobIncome],
      ['Private pension', input.privatePension],
      ['State Pension', input.statePension],
      ['Benefits', input.benefitsInKind],
      ['Other income', input.otherNonSavings],
      ['Savings interest', input.savingsInterest],
      ['Dividends', input.dividends]
    ].filter(([,v]) => Number(v||0) > 0);
    return rows.map(([label,value],i)=>({
      id:`income-${i+1}`,
      type:'income-source',
      label,
      value:Number(value||0),
      display:money(value),
      narration:`${label} adds ${money(value)} to the picture.`
    }));
  }

  function allowanceScenes(result){
    const scenes=[];
    scenes.push({
      id:'personal-allowance', type:'allowance', label:'Personal Allowance', display:money(result.personalAllowance),
      narration:`We first apply a Personal Allowance of ${money(result.personalAllowance)} to the income entered.`
    });
    if(result.savingsStartUsed>0){
      scenes.push({
        id:'savings-starting-rate', type:'allowance', label:'Savings starting rate used', display:money(result.savingsStartUsed),
        narration:`Part of the savings interest may sit inside the starting-rate-for-savings band in this reconstruction.`
      });
    }
    if(result.personalSavingsAllowanceUsed>0){
      scenes.push({
        id:'psa', type:'allowance', label:'Personal Savings Allowance used', display:money(result.personalSavingsAllowanceUsed),
        narration:`We then apply ${money(result.personalSavingsAllowanceUsed)} of Personal Savings Allowance.`
      });
    }
    if(result.dividendAllowanceUsed>0){
      scenes.push({
        id:'dividend-allowance', type:'allowance', label:'Dividend Allowance used', display:money(result.dividendAllowanceUsed),
        narration:`${money(result.dividendAllowanceUsed)} of dividends is covered by the dividend allowance in this calculation.`
      });
    }
    if(result.isaIncomeExcluded>0){
      scenes.push({
        id:'isa-shield', type:'safeguard', label:'ISA income kept out', display:money(result.isaIncomeExcluded),
        narration:`We kept ${money(result.isaIncomeExcluded)} of ISA income outside ordinary taxable savings and dividend income.`
      });
    }
    return scenes;
  }

  function taxScenes(result){
    return [
      {
        id:'taxable-stack', type:'tax-stack', label:'Income left to tax',
        display:`${money(result.taxableNonSavings)} + ${money(result.taxableSavings)} + ${money(result.taxableDividends)}`,
        narration:'After allowances, this is the remaining taxable stack in our reconstruction.'
      },
      {
        id:'tax-due', type:'tax', label:'Reconstructed tax due', display:money(result.taxDue),
        narration:`The rules engine calculates approximately ${money(result.taxDue)} of tax from the information entered.`
      },
      {
        id:'already-paid', type:'tax-paid', label:'Tax already deducted', display:money(result.taxAlreadyDeducted),
        narration:`You told us ${money(result.taxAlreadyDeducted)} has already been collected.`
      },
      {
        id:'underpayment', type:'result', label:'Possible underpayment', display:money(result.reconstructedUnderpayment),
        narration:`That leaves a reconstructed shortfall of ${money(result.reconstructedUnderpayment)}.`
      }
    ];
  }

  function iyaScene(result){
    if(!result.iyaIllustration || !result.iyaIllustration.remainingPayPeriods || result.hmrcStatedUnderpayment<=0) return [];
    return [{
      id:'iya-spread', type:'timeline', label:'Possible in-year collection',
      display:`≈ ${money(result.iyaIllustration.indicativeExtraPerPayday)} × ${result.iyaIllustration.remainingPayPeriods}`,
      narration:`If HMRC were trying to collect the stated amount evenly over the remaining ${result.iyaIllustration.remainingPayPeriods} paydays, that would be roughly ${money(result.iyaIllustration.indicativeExtraPerPayday)} per payday. This is only an illustration.`
    }];
  }

  function reconciliation(result){
    const c=confidenceNarrative(result);
    return {
      id:'reconcile', type:'reconciliation',
      hmrc:result.hmrcStatedUnderpayment,
      reconstructed:result.reconstructedUnderpayment,
      difference:result.difference,
      label:c.label,
      narration:`HMRC says ${money(result.hmrcStatedUnderpayment)}. Our reconstruction gives ${money(result.reconstructedUnderpayment)}. The difference is ${money(result.difference)}.`
    };
  }

  function nextChecks(result){
    const checks=[];
    for(const s of (result.scenarios||[]).slice(0,4)){
      checks.push({title:s.title, evidence:s.evidence, score:s.score, strength:pct(s.score), detail:s.detail});
    }
    if(result.confidence==='Unable to reconcile'){
      checks.push({title:'Check the missing-data list',evidence:'Mismatch remains',score:99,strength:'Priority',detail:'Compare the figures entered with the latest coding notice, payslip, pension figures, taxable benefits and any HMRC income or savings estimates.'});
    }
    return checks;
  }

  function buildStory(input,result){
    return {
      storyVersion:'PAYE-STORY-v3',
      hero:hero(result),
      scenes:[
        ...sourceCards(input),
        ...allowanceScenes(result),
        ...taxScenes(result),
        ...iyaScene(result),
        reconciliation(result)
      ],
      nextChecks:nextChecks(result),
      disclaimer:'This is an illustrative reconstruction based on the information entered. It does not confirm HMRC’s internal calculation or replace HMRC records or professional tax advice.'
    };
  }

  window.PAYEStorytellerV3={buildStory};
})();
