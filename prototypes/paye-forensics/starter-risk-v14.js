(function(){
  const SOURCES={
    starterChecklist:{id:'GOV-STARTER-CHECKLIST',title:'Starter checklist if you’re starting a new job',url:'https://www.gov.uk/guidance/starter-checklist-for-paye'},
    newEmployee:{id:'GOV-NEW-EMPLOYEE-CODE',title:'Work out your new employee tax code',url:'https://www.gov.uk/new-employee-tax-code'},
    multipleJobs:{id:'GOV-MULTIPLE-JOBS',title:'How tax works if you have more than one job',url:'https://www.gov.uk/guidance/how-tax-works-if-you-have-more-than-one-job'},
    startJobChanges:{id:'GOV-START-JOB-CODE-CHANGES',title:'Changes to your tax code when you start a new job',url:'https://www.gov.uk/guidance/changes-to-your-tax-code-when-you-start-a-new-job'},
    paye61030:{id:'HMRC-PAYE61030',title:'PAYE61030 starter declaration statement types',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye61030'},
    paye61025:{id:'HMRC-PAYE61025',title:'PAYE61025 employer responsibilities',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye61025'},
    checkCurrentYear:{id:'GOV-CHECK-CURRENT-YEAR',title:'Check your Income Tax for the current year',url:'https://www.gov.uk/check-income-tax-current-year'}
  };

  function normCode(v){return String(v||'').trim().toUpperCase().replace(/\s+/g,'');}
  function hasEmergencyMarker(code){return /(W1|M1|NONCUM|X)$/.test(normCode(code));}
  function isFullAllowanceLike(code){return /^([SC])?1257L(?:W1|M1|X|NONCUM)?$/.test(normCode(code));}

  function expectedStarterRoute(declaration){
    const d=String(declaration||'').trim().toUpperCase();
    if(d==='A') return {kind:'primary',message:'Statement A indicates this is the first job since 6 April and no relevant taxable benefit/pension listed in the statement.',sourceIds:[SOURCES.paye61030.id]};
    if(d==='B') return {kind:'primary-existing-year-history',message:'Statement B indicates this is now the only job, but there has been another job or relevant taxable benefit earlier in the tax year.',sourceIds:[SOURCES.paye61030.id]};
    if(d==='C') return {kind:'secondary',message:'Statement C is the multiple/current-job route and is associated with BR in HMRC starter rules.',sourceIds:[SOURCES.paye61030.id]};
    return {kind:'unsigned-or-unknown',message:'If no starter declaration is completed, HMRC guidance says 0T on a Week 1/Month 1 basis is used as the override starter code.',sourceIds:[SOURCES.paye61030.id]};
  }

  function analyseStarter(input){
    const x={
      hasP45:Boolean(input&&input.hasP45),
      stillHasAnotherJob:Boolean(input&&input.stillHasAnotherJob),
      declaration:String(input&&input.declaration||'').trim().toUpperCase(),
      priorJobEnded:Boolean(input&&input.priorJobEnded),
      priorCode:normCode(input&&input.priorCode),
      firstPayslipCode:normCode(input&&input.firstPayslipCode),
      employerCopiedPriorCode:Boolean(input&&input.employerCopiedPriorCode),
      firstJobSince6April:Boolean(input&&input.firstJobSince6April),
      hadEarlierJobThisTaxYear:Boolean(input&&input.hadEarlierJobThisTaxYear),
      receivingStateOrOccupationalPension:Boolean(input&&input.receivingStateOrOccupationalPension)
    };
    const findings=[];
    const push=(severity,title,detail,sourceIds,check)=>findings.push({severity,title,detail,sourceIds,check});

    if(x.stillHasAnotherJob && x.declaration && x.declaration!=='C'){
      push('high','Starter declaration may conflict with having another live job',`You said another job is still active, but starter declaration ${x.declaration} was used. HMRC says people starting an additional job should declare that they already have another job; an incorrect checklist can lead to the wrong tax being deducted.`,[SOURCES.multipleJobs.id,SOURCES.starterChecklist.id],'Check the starter declaration submitted to payroll and whether HMRC shows both employments as live.');
    }

    if(!x.stillHasAnotherJob && x.priorJobEnded && x.declaration==='C'){
      push('medium','Statement C may have been selected when the earlier job had ended','HMRC guidance notes that selecting Statement C in error can lead to BR/0T outcomes until the record is corrected.',[SOURCES.startJobChanges.id,SOURCES.paye61030.id],'Check whether your former employer has reported the leaving details and whether HMRC still shows that employment as live.');
    }

    if(x.employerCopiedPriorCode){
      push('high','Possible payroll code carry-forward','A previous employer tax code should not simply be reused as a new-starter code without following the P45/starter rules. HMRC says employers normally work out a new starter code from the P45 or starter declaration and report starter information on the FPS.',[SOURCES.newEmployee.id,SOURCES.paye61025.id],'Ask payroll what source they used for the opening tax code: P45, starter declaration or an HMRC coding notice.');
    }

    if(!x.hasP45 && !x.declaration){
      push('high','Missing starter declaration','No P45 and no declaration is a material risk. HMRC guidance says an unsigned/missing starter declaration leads to 0T Week 1/Month 1 as the override starter route.',[SOURCES.paye61030.id,SOURCES.starterChecklist.id],'Check the onboarding record and first FPS starter declaration.');
    }

    if(x.stillHasAnotherJob && isFullAllowanceLike(x.firstPayslipCode)){
      push('high','Full Personal Allowance may have been used at an additional job',`Your first payslip shows ${x.firstPayslipCode}. A 1257L-type code can be valid, but where another job is still live it deserves checking because HMRC normally allocates one Personal Allowance across the person’s PAYE sources rather than giving a fresh full allowance automatically to every job.`,[SOURCES.multipleJobs.id,SOURCES.checkCurrentYear.id],'Check which job HMRC currently treats as the main employment and where the Personal Allowance is allocated.');
    }

    if(!x.hasP45 && isFullAllowanceLike(x.firstPayslipCode) && !hasEmergencyMarker(x.firstPayslipCode)){
      push('medium','Full cumulative-looking code used without a P45','A full 1257L-type code without W1/M1/X may be correct after HMRC has issued it, but if payroll used it immediately without a P45 or HMRC notice, verify the starter route used.',[SOURCES.newEmployee.id,SOURCES.starterChecklist.id],'Ask whether HMRC issued the code or payroll selected it locally.');
    }

    if(x.priorCode && x.firstPayslipCode && x.priorCode===x.firstPayslipCode && !x.hasP45){
      push('medium','New job code exactly matches prior-job code without P45 evidence','An exact carry-over can happen legitimately after HMRC coding, but without a P45 it is worth checking whether payroll simply copied the previous code instead of applying new-starter rules.',[SOURCES.newEmployee.id,SOURCES.paye61025.id],'Check payroll onboarding notes and HMRC current-year employment records.');
    }

    if(!findings.length){
      push('low','No obvious starter-code conflict found','The facts entered do not show an obvious starter declaration or payroll setup conflict. That does not prove the code is correct.',[SOURCES.checkCurrentYear.id],'Compare the first payslip code with HMRC’s current-year service and confirm all jobs/pensions and estimated incomes are present.');
    }

    const high=findings.filter(f=>f.severity==='high').length;
    const medium=findings.filter(f=>f.severity==='medium').length;
    const risk=high?'High':medium?'Review':'Low';
    return {risk,findings,starterRoute:expectedStarterRoute(x.declaration),sourceRegistry:SOURCES,input:x,epistemicNote:'These are risk indicators and possible explanations, not proof of an employer or HMRC error.'};
  }

  window.PAYEStarterRiskV14={analyseStarter,expectedStarterRoute,SOURCES};
})();