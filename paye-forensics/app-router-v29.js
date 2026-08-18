// TA GuruLabs PAYE Forensics v29 - Unified journey router
// Copyright © TA GuruLabs. Confidential product architecture.

export function choosePayeJourney(facts = {}) {
  const hasUnderpayment = Number(facts.hmrcUnderpayment || facts.underpayment || 0) > 0;
  const hasNewJob = Boolean(facts.startedNewJob || facts.newJobStartDate);
  const hasFirstPay = Boolean(facts.firstPayslip || facts.hasBeenPaid);
  const hasMultipleSources = Number(facts.activePayeSources || (facts.sources||[]).filter(s=>s?.active!==false).length || 0) > 1;
  const hasPensions = (facts.pensions||[]).length > 0 || Number(facts.statePension||0) > 0;
  const hasThreePensions = (facts.pensions||[]).length >= 3;
  const hasSavings = Number(facts.untaxedInterest || facts.savingsInterest || 0) > 0;
  const taxCode = String(facts.taxCode || '').toUpperCase().replace(/\s+/g,'');
  const hasK = /^(S|C)?K\d+/.test(taxCode);
  const hasIya = Number(facts.iyaAmount||0) > 0;

  const modules = [];
  if (hasNewJob && !hasFirstPay) modules.push('STARTER_DECLARATION_COACH');
  if (hasNewJob && hasFirstPay) modules.push('NEW_JOB_HEALTH_CHECK','FIRST_PAYSLIP_WATCH');
  if (hasMultipleSources) modules.push('PERSONAL_ALLOWANCE_MAP','ALLOWANCE_COLLISION_CHECK');
  if (hasPensions) modules.push('PENSION_INCOME_MAP');
  if (hasThreePensions || (hasPensions && hasSavings)) modules.push('PENSIONER_ALLOWANCE_SPLIT');
  if (hasK) modules.push('K_CODE_EXPLAINER');
  if (hasIya) modules.push('IYA_EXPLAINER');
  if (hasUnderpayment) modules.push('UNDERPAYMENT_DETECTIVE','RECONCILIATION_BRIDGE','MISSING_PIECE_MODE');

  const primary = hasUnderpayment ? 'UNDERPAYMENT_FORENSICS'
    : hasNewJob ? 'NEW_JOB_GUARDIAN'
    : hasPensions ? 'PENSIONER_PAYE'
    : hasMultipleSources ? 'MULTI_SOURCE_PAYE'
    : 'TAX_CODE_CHECK';

  return {
    version:'29',
    primaryJourney:primary,
    modules:[...new Set(modules)],
    presentationLevels:['SIMPLE','NORMAL','ADVISER'],
    customerPrompt: primary==='UNDERPAYMENT_FORENSICS'
      ? 'HMRC says I owe tax. Show me how that may have happened.'
      : primary==='NEW_JOB_GUARDIAN'
      ? 'I started a new job. Is my tax looking right?'
      : primary==='PENSIONER_PAYE'
      ? 'I have pensions and other income. Show me where my allowance is going.'
      : primary==='MULTI_SOURCE_PAYE'
      ? 'I have more than one PAYE income. Show me where my allowance is working.'
      : 'Explain my tax code and what it is doing.',
    guardrail:'Routing chooses explanation modules only. It does not decide that HMRC, payroll, an employer or a pension provider has made an error.'
  };
}
