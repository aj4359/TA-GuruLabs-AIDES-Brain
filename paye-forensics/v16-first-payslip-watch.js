export function buildFirstPayslipWatch({ startDate, firstPayDate, currentDate, firstPayslipCode, hmrcCurrentCode, anotherLiveJob, starterDeclaration, p45Provided, hmrcCodeKnown }) {
  const day = Math.max(0, Math.floor((new Date(currentDate) - new Date(startDate)) / 86400000));
  const findings = [];
  const milestones = [1,14,28,35].map(d => ({ day:d, status: day >= d ? 'due' : 'upcoming' }));

  if (day >= 1 && !firstPayslipCode) findings.push({ severity:'medium', id:'NO_FIRST_PAYSLIP_CODE', text:'Add the tax code from the first payslip to continue the health check.' });
  if (anotherLiveJob && ['A','B'].includes((starterDeclaration||'').toUpperCase())) findings.push({ severity:'high', id:'DECLARATION_CONFLICT', text:'Your starter declaration may not match the fact that another job is still active.' });
  if (!p45Provided && !starterDeclaration) findings.push({ severity:'high', id:'NO_STARTER_ROUTE', text:'No P45 and no starter declaration are recorded in this case.' });
  if (anotherLiveJob && /^1257L(?:\s*(?:W1|M1|X|NONCUM))?$/i.test(firstPayslipCode||'')) findings.push({ severity:'high', id:'POSSIBLE_DUPLICATE_PA', text:'The new job appears to be using a full Personal Allowance while another job is still active. This is a check prompt, not proof the code is wrong.' });
  if (day >= 14 && hmrcCurrentCode && firstPayslipCode && hmrcCurrentCode.replace(/\s/g,'').toUpperCase() !== firstPayslipCode.replace(/\s/g,'').toUpperCase()) findings.push({ severity:'medium', id:'PAYROLL_HMRC_DELTA', text:'The code on the payslip does not match the current HMRC code entered for this employment.' });
  if (day >= 28 && !hmrcCurrentCode) findings.push({ severity:'medium', id:'HMRC_CODE_NOT_CHECKED', text:'Consider checking the current-year Income Tax service for the code HMRC currently holds for this employment.' });
  if (day >= 35 && (!hmrcCodeKnown || findings.some(f=>['PAYROLL_HMRC_DELTA','POSSIBLE_DUPLICATE_PA','DECLARATION_CONFLICT','NO_STARTER_ROUTE'].includes(f.id)))) findings.push({ severity:'high', id:'DAY35_ESCALATION', text:'This case still has unresolved tax-code risk indicators at day 35. Prepare a case summary and check the employment/code details with HMRC or payroll.' });

  return {
    day,
    phase: day < 14 ? 'EARLY' : day < 28 ? 'CHECK' : day < 35 ? 'RECONCILE' : 'ESCALATE_IF_UNRESOLVED',
    milestones,
    findings,
    nextAction: day < 14 ? 'Keep the first payslip and confirm the code shown.' : day < 28 ? 'Compare the payslip code with HMRC current-year information.' : day < 35 ? 'Resolve any payroll/HMRC mismatch and confirm employment status.' : 'If unresolved, generate the PAYE Forensics case pack.'
  };
}
