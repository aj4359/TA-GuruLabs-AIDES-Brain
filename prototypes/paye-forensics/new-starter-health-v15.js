(function(){
  const SOURCES={
    starterChecklist:{id:'GOV-STARTER-CHECKLIST',url:'https://www.gov.uk/guidance/starter-checklist-for-paye'},
    newEmployee:{id:'GOV-NEW-EMPLOYEE-TAX-CODE',url:'https://www.gov.uk/new-employee-tax-code'},
    paye61030:{id:'HMRC-PAYE61030',url:'https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye61030'},
    multipleJobs:{id:'GOV-MULTIPLE-JOBS',url:'https://www.gov.uk/guidance/how-tax-works-if-you-have-more-than-one-job'},
    startJob:{id:'GOV-START-A-JOB',url:'https://www.gov.uk/start-a-job'},
    wrongCode:{id:'GOV-NEW-JOB-CODE-CHANGES',url:'https://www.gov.uk/guidance/changes-to-your-tax-code-when-you-start-a-new-job'}
  };

  function norm(v){return String(v||'').trim().toUpperCase().replace(/\s+/g,'');}
  function hasFullAllowance(code){return /^(S|C)?1257L(?:W1|M1|X|NONCUM)?$/.test(norm(code));}
  function isNoAllowanceRoute(code){return /^(S|C)?(BR|D0|D1|0T)/.test(norm(code));}
  function isEmergency(code){return /(W1|M1|X|NONCUM)$/.test(norm(code));}

  function expectedStarterRoute(input){
    const d=norm(input.declaration);
    if(input.p45Given) return {route:'P45-driven starter setup',evidence:'Observed',sourceIds:[SOURCES.newEmployee.id]};
    if(d==='A') return {route:'Statement A starter route',evidence:'Observed',sourceIds:[SOURCES.starterChecklist.id,SOURCES.paye61030.id]};
    if(d==='B') return {route:'Statement B starter route',evidence:'Observed',sourceIds:[SOURCES.starterChecklist.id,SOURCES.paye61030.id]};
    if(d==='C') return {route:'Statement C / additional-job route',evidence:'Observed',sourceIds:[SOURCES.starterChecklist.id,SOURCES.paye61030.id]};
    return {route:'No confirmed starter declaration',evidence:'Observed',sourceIds:[SOURCES.paye61030.id]};
  }

  function analyse(input){
    const code=norm(input.firstPayslipCode);
    const old=norm(input.previousJobCode);
    const d=norm(input.declaration);
    const risks=[];
    const add=(id,severity,title,why,sourceIds)=>risks.push({id,severity,title,why,evidenceType:'Inferred',sourceIds});

    if(input.anotherLiveJob && (d==='A'||d==='B')) add('DECLARATION-CONFLICT','high','Starter declaration may conflict with another live job','You told us another job is still active, but the selected declaration normally describes a different starter situation.',[SOURCES.starterChecklist.id,SOURCES.multipleJobs.id]);
    if(input.anotherLiveJob && hasFullAllowance(code)) add('DUPLICATE-ALLOWANCE-RISK','high','Possible duplicate Personal Allowance risk','A full 1257L-style allowance appears on this new job while another job is still active. That does not prove an error, but it deserves checking.',[SOURCES.multipleJobs.id,SOURCES.startJob.id]);
    if(!input.p45Given && !d) add('MISSING-STARTER-DECLARATION','high','No P45 and no confirmed starter declaration','Without a P45, the starter checklist information is normally used to work out the first-pay tax code.',[SOURCES.starterChecklist.id,SOURCES.newEmployee.id]);
    if(!input.p45Given && hasFullAllowance(code) && !input.hmrcCodeReceived) add('FULL-ALLOWANCE-WITHOUT-EVIDENCE','medium','1257L appears without a P45 or known HMRC-issued code','This may be correct in some cases, but the source of the code is unclear and should be checked.',[SOURCES.newEmployee.id,SOURCES.starterChecklist.id]);
    if(!input.p45Given && old && code===old && !input.hmrcCodeReceived) add('PRIOR-CODE-CARRYFORWARD','medium','New job code exactly matches the previous job code','A matching code can happen legitimately, but without P45 or HMRC-code evidence this is a useful payroll setup check.',[SOURCES.newEmployee.id]);
    if(d==='C' && hasFullAllowance(code)) add('C-ROUTE-MISMATCH','high','Statement C but full Personal Allowance appears on first payslip','Statement C is associated with the secondary-job route, so a full-allowance code merits checking.',[SOURCES.paye61030.id]);
    if(!d && !input.p45Given && !/^0T/.test(code)) add('NO-DECLARATION-ROUTE-MISMATCH','medium','First-pay code does not look like the no-declaration route','HMRC manual guidance associates no declaration with 0T Week 1/Month 1, unless another code has since been issued.',[SOURCES.paye61030.id]);
    if(isEmergency(code)) add('EMERGENCY-CODE','info','Emergency/non-cumulative basis detected','This may be temporary while HMRC receives the information needed to update the code.',[SOURCES.wrongCode.id]);
    if(isNoAllowanceRoute(code) && !input.anotherLiveJob && d!=='C') add('NO-ALLOWANCE-SINGLE-JOB-CHECK','medium','Single-job starter is being taxed without a normal allowance code','BR, D0, D1 or 0T can be valid, but for a sole job this may be worth checking against the starter information and HMRC record.',[SOURCES.wrongCode.id]);

    const score=risks.reduce((s,r)=>s+({high:3,medium:2,info:1}[r.severity]||0),0);
    const status=score>=6?'High check priority':score>=3?'Worth checking':'No obvious starter-code risk from supplied facts';
    return {status,score,expectedRoute:expectedStarterRoute(input),risks,code,sourceRegistry:SOURCES,disclaimer:'Risk indicators only. They do not prove an employer, payroll provider or HMRC made an error.'};
  }

  function firstPayslipWatch(input){
    const result=analyse(input);
    const actions=[];
    if(result.risks.length){
      actions.push('Compare the tax code on the first payslip with the code shown in HMRC’s current-year service.');
      actions.push('Check whether any previous employment is still showing as live when it has actually ended.');
      actions.push('If another job is still active, confirm the starter declaration reflected that fact.');
      actions.push('If the first pay has already happened, use the current-year service rather than completing a new starter checklist again.');
    } else actions.push('Keep the first payslip and re-check the code if HMRC issues a later change.');
    return {...result,actions};
  }

  window.PAYENewStarterHealthV15={SOURCES,analyse,firstPayslipWatch,hasFullAllowance,isNoAllowanceRoute,isEmergency};
})();