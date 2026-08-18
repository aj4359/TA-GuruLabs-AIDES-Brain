// PAYE Forensics v22 - Guardian Case Bundle with Automatic Payslip Reconstruction

import { routeNewJobJourney } from './new-job-paye-guardian.js';
import { buildAllowanceCollisionCase } from './allowance-collision-engine.js';
import { reconstructPayPeriods } from './pay-period-tax-engine-v22.js';

const norm = v => String(v || '').toUpperCase().replace(/\s+/g, '');
const money = n => Math.round(Number(n || 0) * 100) / 100;

function routeComparison(input) {
  const declaration = norm(input.starterDeclaration);
  const p45 = Boolean(input.p45Provided);
  const otherJob = Boolean(input.anotherJobLive);
  const actual = norm(input.firstPayslipCode);
  const hmrc = norm(input.hmrcCurrentCode);
  const signals = [];

  let expectedFamily = 'UNKNOWN';
  let expectedText = 'Not enough confirmed starter information to model a likely route.';
  if (p45) { expectedFamily = 'P45_LED'; expectedText = 'The confirmed facts point to a P45-led starter route, subject to later HMRC coding.'; }
  else if (declaration === 'C' || otherJob) { expectedFamily = 'SECONDARY_JOB'; expectedText = 'The confirmed facts point toward an additional-job route rather than a fresh full Personal Allowance route.'; }
  else if (!declaration) { expectedFamily = 'NO_DECLARATION'; expectedText = 'No P45 and no declaration have been confirmed, so the first-pay route needs checking.'; }
  else { expectedFamily = 'PRIMARY_OR_RECENT_JOB'; expectedText = `Statement ${declaration} suggests a primary/recent-job starter route, subject to the exact checklist facts.`; }

  if (expectedFamily === 'SECONDARY_JOB' && /^1257[LMN]$/.test(actual.replace(/^(S|C)/,''))) {
    signals.push({severity:'HIGH',evidenceClass:'INFERRED',title:'Possible starter-route mismatch',detail:'Starter facts suggest an additional-job route, but the first payslip shows a full 1257-family allowance code.'});
  }
  if (actual && hmrc && actual !== hmrc) signals.push({severity:'HIGH',evidenceClass:'OBSERVED',title:'Payroll and HMRC codes differ',detail:`Payslip: ${actual}. HMRC current-year record: ${hmrc}.`});

  return { expectedFamily, expectedText, actualCode:actual || null, hmrcCode:hmrc || null, signals };
}

export function buildGuardianCaseBundleV22(input = {}) {
  const journey = routeNewJobJourney(input);
  const starterRoute = routeComparison(input);
  const allowanceCollision = buildAllowanceCollisionCase({ sources:Array.isArray(input.activeSources)?input.activeSources:[] });
  const automaticPayslipMovie = reconstructPayPeriods({ payslips:Array.isArray(input.payslips)?input.payslips:[], frequency:input.payFrequency || 'monthly' });
  const hmrcUnderpayment = money(input.hmrcUnderpayment || 0);
  const reconciliationDifference = money(Math.abs(hmrcUnderpayment - automaticPayslipMovie.possibleShortfall));
  const tolerance = hmrcUnderpayment ? Math.max(5, hmrcUnderpayment * 0.15) : 5;
  const reconciliationState = reconciliationDifference <= 5 ? 'LIKELY_MATCH' : reconciliationDifference <= tolerance ? 'POSSIBLE_MATCH' : 'UNRESOLVED_DIFFERENCE';

  const signals = [
    ...journey.signals,
    ...starterRoute.signals,
    ...allowanceCollision.findings.map(f=>({severity:f.severity,evidenceClass:f.evidenceClass,title:f.title,detail:f.explanation}))
  ];

  if (automaticPayslipMovie.frames.length) {
    signals.push({
      severity: reconciliationState === 'UNRESOLVED_DIFFERENCE' ? 'MEDIUM' : 'LOW',
      evidenceClass:'INFERRED',
      title: reconciliationState === 'UNRESOLVED_DIFFERENCE' ? 'Automatic payslip reconstruction leaves a missing piece' : 'Automatic payslip reconstruction broadly aligns with the stated underpayment',
      detail:`Possible reconstructed shortfall £${automaticPayslipMovie.possibleShortfall.toFixed(2)}; HMRC-stated underpayment £${hmrcUnderpayment.toFixed(2)}; difference £${reconciliationDifference.toFixed(2)}.`
    });
  }

  const missingPiecePrompts = reconciliationState === 'UNRESOLVED_DIFFERENCE' ? [
    'Check whether an earlier job or pension is missing from the case.',
    'Check whether the tax code changed during one of the pay periods.',
    'Check taxable benefits, State Pension or private pension income.',
    'Check whether HMRC used a different annual income estimate.',
    'Check prior in-year adjustments or tax already collected elsewhere.'
  ] : [];

  return {
    version:'22',
    journey,
    starterRoute,
    allowanceCollision,
    payslipMovie:automaticPayslipMovie,
    reconciliation:{hmrcUnderpayment,reconstructedPossibleShortfall:automaticPayslipMovie.possibleShortfall,difference:reconciliationDifference,state:reconciliationState},
    missingPiecePrompts,
    signals,
    chronology:[
      {stage:'STARTER',label:'Starter facts captured',evidenceClass:'OBSERVED'},
      ...(input.firstPayReceived?[{stage:'FIRST_PAY',label:'First payslip observed',evidenceClass:'OBSERVED'}]:[]),
      ...(starterRoute.signals.length?[{stage:'COMPARE',label:'Starter route compared with payroll',evidenceClass:'INFERRED'}]:[]),
      ...(allowanceCollision.findings.length?[{stage:'ALLOWANCE',label:'Allowance collision risk detected',evidenceClass:'INFERRED'}]:[]),
      ...(automaticPayslipMovie.frames.length?[{stage:'PAYSLIPS',label:'Pay-period tax expectation reconstructed automatically',evidenceClass:'INFERRED'}]:[]),
      ...(hmrcUnderpayment>0?[{stage:'RECONCILE',label:'Reconstructed shortfall compared with HMRC-stated amount',evidenceClass:'INFERRED'}]:[])
    ],
    guardrail:'Observed facts, inferred diagnostics and reconstructed expectations remain separate. This is not HMRC payroll software and does not establish fault or issue a tax code.'
  };
}
