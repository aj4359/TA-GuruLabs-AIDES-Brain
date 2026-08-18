// PAYE Forensics v21 - Unified Guardian Case Bundle
// Combines journey routing, observed-code comparison, allowance-collision diagnostics
// and an illustrative payslip-by-payslip shortfall story.

import { routeNewJobJourney } from './new-job-paye-guardian.js';
import { buildAllowanceCollisionCase } from './allowance-collision-engine.js';

const norm = v => String(v || '').toUpperCase().replace(/\s+/g, '');
const money = n => Math.round(Number(n || 0) * 100) / 100;

function classifyRoute(input) {
  const declaration = norm(input.starterDeclaration);
  const p45 = Boolean(input.p45Provided);
  const otherJob = Boolean(input.anotherJobLive);
  const actual = norm(input.firstPayslipCode);
  const hmrc = norm(input.hmrcCurrentCode);
  const signals = [];

  let expectedFamily = 'UNKNOWN';
  let expectedText = 'Not enough confirmed starter information to model a likely route.';

  if (p45) {
    expectedFamily = 'P45_LED';
    expectedText = 'A P45-led starter route would normally use the starter information supplied from the previous employment, subject to later HMRC coding.';
  } else if (declaration === 'C' || otherJob) {
    expectedFamily = 'SECONDARY_JOB';
    expectedText = 'The confirmed facts suggest a secondary-job starter route rather than a fresh full Personal Allowance route.';
  } else if (!declaration) {
    expectedFamily = 'NO_DECLARATION';
    expectedText = 'With no P45 and no completed declaration, the starter route should be checked carefully against the first payslip.';
  } else if (['A','B'].includes(declaration)) {
    expectedFamily = 'PRIMARY_OR_RECENT_JOB';
    expectedText = `Statement ${declaration} suggests a primary/recent-employment starter route, subject to the exact official checklist facts.`;
  }

  if (expectedFamily === 'SECONDARY_JOB' && /^1257[LMN]$/.test(actual.replace(/^(S|C)/,''))) {
    signals.push({severity:'HIGH', evidenceClass:'INFERRED', title:'Possible expected-route vs payroll mismatch', detail:'The starter facts suggest an additional-job route, but the first payslip shows a full 1257-family allowance code.'});
  }
  if (hmrc && actual && hmrc !== actual) {
    signals.push({severity:'HIGH', evidenceClass:'OBSERVED', title:'Payroll and HMRC codes differ', detail:`First payslip shows ${actual}; the confirmed HMRC current-year code is ${hmrc}.`});
  }
  if (!p45 && input.previousTaxCode && actual && norm(input.previousTaxCode) === actual) {
    signals.push({severity:'MEDIUM', evidenceClass:'INFERRED', title:'Previous code appears to have carried forward', detail:'The first-payslip code matches the previous employment code, but no P45 has been confirmed. This is a check prompt, not proof of payroll error.'});
  }

  return { expectedFamily, expectedText, actualCode: actual || null, hmrcCode: hmrc || null, signals };
}

function buildPayslipMovie(input) {
  const payslips = Array.isArray(input.payslips) ? input.payslips : [];
  const statedUnderpayment = Number(input.hmrcUnderpayment || 0);
  const frames = [];
  let cumulativeIllustrativeShortfall = 0;

  payslips.forEach((p, i) => {
    const gross = Number(p.gross || 0);
    const taxDeducted = Number(p.taxDeducted || 0);
    const benchmarkTax = Number.isFinite(Number(p.reconstructedExpectedTax)) ? Number(p.reconstructedExpectedTax) : taxDeducted;
    const periodDifference = Math.max(0, benchmarkTax - taxDeducted);
    cumulativeIllustrativeShortfall += periodDifference;
    frames.push({
      period: p.period || i + 1,
      gross: money(gross),
      taxDeducted: money(taxDeducted),
      reconstructedExpectedTax: money(benchmarkTax),
      periodDifference: money(periodDifference),
      cumulativeIllustrativeShortfall: money(cumulativeIllustrativeShortfall),
      taxCode: norm(p.taxCode || input.firstPayslipCode),
      evidenceClass: Number.isFinite(Number(p.reconstructedExpectedTax)) ? 'INFERRED' : 'OBSERVED_ONLY'
    });
  });

  return {
    frames,
    statedUnderpayment: money(statedUnderpayment),
    illustrativeCumulativeShortfall: money(cumulativeIllustrativeShortfall),
    reconciliationDifference: money(Math.abs(statedUnderpayment - cumulativeIllustrativeShortfall)),
    disclaimer: 'This movie is an illustrative reconstruction of deduction timing. It is not HMRC payroll software and does not by itself determine annual tax liability.'
  };
}

export function buildGuardianCaseBundle(input = {}) {
  const journey = routeNewJobJourney(input);
  const routeComparison = classifyRoute(input);
  const sources = Array.isArray(input.activeSources) ? input.activeSources : [];
  const allowanceCollision = buildAllowanceCollisionCase({ sources });
  const payslipMovie = buildPayslipMovie(input);

  const signals = [
    ...journey.signals,
    ...routeComparison.signals,
    ...allowanceCollision.findings.map(f => ({severity:f.severity,evidenceClass:f.evidenceClass,title:f.title,detail:f.explanation}))
  ];

  if (payslipMovie.frames.length && Number(input.hmrcUnderpayment || 0) > 0) {
    signals.push({
      severity: payslipMovie.reconciliationDifference <= 5 ? 'LOW' : 'MEDIUM',
      evidenceClass: 'ILLUSTRATIVE',
      title: payslipMovie.reconciliationDifference <= 5 ? 'Payslip story broadly reconciles with stated underpayment' : 'Payslip story does not fully reconcile',
      detail: `Illustrative cumulative shortfall £${payslipMovie.illustrativeCumulativeShortfall.toFixed(2)} versus stated underpayment £${payslipMovie.statedUnderpayment.toFixed(2)}.`
    });
  }

  return {
    version: '21',
    journey,
    routeComparison,
    allowanceCollision,
    payslipMovie,
    signals,
    chronology: [
      {stage:'STARTER', label:'Starter facts captured', evidenceClass:'OBSERVED'},
      ...(input.firstPayReceived ? [{stage:'FIRST_PAY', label:'First payslip observed', evidenceClass:'OBSERVED'}] : []),
      ...(routeComparison.signals.length ? [{stage:'COMPARE', label:'Starter route compared with payroll', evidenceClass:'INFERRED'}] : []),
      ...(allowanceCollision.findings.length ? [{stage:'ALLOWANCE', label:'Personal Allowance collision risk detected', evidenceClass:'INFERRED'}] : []),
      ...(payslipMovie.frames.length ? [{stage:'MOVIE', label:'Payslip deduction story reconstructed', evidenceClass:'ILLUSTRATIVE'}] : []),
      ...(Number(input.hmrcUnderpayment || 0) > 0 ? [{stage:'FORENSICS', label:'Underpayment ready for forensic reconciliation', evidenceClass:'OBSERVED'}] : [])
    ],
    guardrail: 'Observed facts, inferred diagnostics and illustrative reconstructions remain separate. The bundle does not issue a tax code or establish fault.'
  };
}
