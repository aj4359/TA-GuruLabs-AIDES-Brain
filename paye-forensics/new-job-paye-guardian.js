// PAYE Forensics v20 - New Job PAYE Guardian
// Unified journey router for prevention -> first pay -> watch -> collision -> forensics.

export function routeNewJobJourney(input = {}) {
  const firstPayReceived = Boolean(input.firstPayReceived);
  const daysSinceStart = Number(input.daysSinceStart || 0);
  const hasFirstPayslipCode = Boolean(input.firstPayslipCode);
  const anotherJobLive = Boolean(input.anotherJobLive);
  const activeSources = Array.isArray(input.activeSources) ? input.activeSources : [];
  const unresolvedUnderpayment = Number(input.hmrcUnderpayment || 0) > 0;

  const stages = [];
  let currentStage = 'STARTER_DECLARATION_COACH';

  if (!firstPayReceived) {
    stages.push({
      id: 'PRE_PAY',
      title: 'Before first pay',
      module: 'Starter Declaration Coach',
      purpose: 'Check P45 and starter-declaration facts before payroll runs.',
      status: 'ACTIVE'
    });
  } else {
    stages.push({
      id: 'PRE_PAY',
      title: 'Before first pay',
      module: 'Starter Declaration Coach',
      purpose: 'Historical context only. Do not redo the checklist after first pay.',
      status: 'COMPLETE_OR_PAST'
    });
    currentStage = 'FIRST_PAY_HEALTH_CHECK';
  }

  if (firstPayReceived) {
    stages.push({
      id: 'FIRST_PAY',
      title: 'First payslip',
      module: 'New Job Tax Code Health Check',
      purpose: 'Compare starter facts with the tax code that actually appeared.',
      status: hasFirstPayslipCode ? 'ACTIVE' : 'NEEDS_INPUT'
    });
  }

  if (firstPayReceived && daysSinceStart > 0) {
    currentStage = daysSinceStart >= 35 ? 'DAY_35_REVIEW' : 'FIRST_PAY_WATCH';
    stages.push({
      id: 'WATCH',
      title: '35-Day Watch',
      module: 'First Payslip Watch',
      purpose: 'Track payroll/HMRC code alignment while the new employment settles.',
      status: daysSinceStart >= 35 ? 'REVIEW_NOW' : 'WATCHING',
      day: daysSinceStart
    });
  }

  if (activeSources.length > 1 || anotherJobLive) {
    stages.push({
      id: 'ALLOWANCE',
      title: 'Allowance map',
      module: 'Personal Allowance Collision Check',
      purpose: 'Check whether full-allowance codes appear across more than one active PAYE source.',
      status: 'CHECK'
    });
  }

  if (unresolvedUnderpayment || daysSinceStart >= 35) {
    currentStage = unresolvedUnderpayment ? 'PAYE_FORENSICS' : currentStage;
    stages.push({
      id: 'FORENSICS',
      title: 'Forensic review',
      module: 'PAYE Forensics',
      purpose: 'Reconstruct a possible route to any underpayment or unresolved code position.',
      status: unresolvedUnderpayment ? 'ACTIVE' : 'AVAILABLE'
    });
  }

  const signals = [];
  if (!firstPayReceived && !input.p45Provided && !input.starterDeclaration) {
    signals.push({severity:'HIGH',title:'Starter information missing',evidenceClass:'OBSERVED'});
  }
  if (anotherJobLive && ['A','B'].includes(String(input.starterDeclaration || '').toUpperCase())) {
    signals.push({severity:'HIGH',title:'Possible starter-declaration conflict',evidenceClass:'INFERRED'});
  }
  if (firstPayReceived && !hasFirstPayslipCode) {
    signals.push({severity:'MEDIUM',title:'First-payslip tax code not yet captured',evidenceClass:'OBSERVED'});
  }
  if (daysSinceStart >= 35 && input.hmrcCurrentCode && input.firstPayslipCode && String(input.hmrcCurrentCode).toUpperCase() !== String(input.firstPayslipCode).toUpperCase()) {
    signals.push({severity:'HIGH',title:'Payroll and HMRC code still differ at Day 35',evidenceClass:'OBSERVED'});
  }

  return {
    currentStage,
    stages,
    signals,
    headline: currentStage === 'STARTER_DECLARATION_COACH' ? 'Prevent a PAYE problem before first pay.' :
      currentStage === 'FIRST_PAY_HEALTH_CHECK' ? 'Check what happened on your first payslip.' :
      currentStage === 'FIRST_PAY_WATCH' ? 'Watch your code while the new job settles.' :
      currentStage === 'DAY_35_REVIEW' ? 'Your new-job PAYE position needs a review.' :
      'Investigate why your PAYE position changed.',
    guardrail: 'This journey helps you check and understand PAYE information. It does not issue tax codes or prove that an employer, payroll provider or HMRC made an error.'
  };
}
