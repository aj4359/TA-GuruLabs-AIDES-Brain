// PAYE Forensics v25 - K Code / IYA / Underpayment explainer
// Customer education + forensic reconstruction only. Does not reproduce HMRC NPS or issue codes.

const n = v => Math.max(0, Number(v || 0));
const norm = v => String(v || '').toUpperCase().replace(/\s+/g, '');

export function decodeKCode(code = '') {
  const c = norm(code);
  const m = c.match(/^(S|C)?K(\d{1,4})(?:W1|M1|X|NONCUM)?$/);
  if (!m) return null;
  const number = Number(m[2]);
  // HMRC K-code construction is not simply a reverse allowance calculation in every live case.
  // Use this only as an explanatory signal for the scale of excess deductions represented by the code.
  const indicativeExcessDeductions = (number + 1) * 10;
  return {
    code: c,
    jurisdictionPrefix: m[1] || null,
    number,
    indicativeExcessDeductions,
    evidenceClass: 'INFERRED',
    explanation: 'A K code is used when coding deductions exceed coding allowances. Instead of giving tax-free pay, payroll adds an amount to taxable pay. The exact live code depends on HMRC coding inputs and should be checked against the P2/code breakdown.',
    fiftyPercentGuardrail: 'Tax deducted under a K code cannot exceed 50% of the pre-tax pay or pension for that pay period.'
  };
}

export function buildKCodeIYAStory(input = {}) {
  const taxCode = norm(input.taxCode);
  const previousCode = norm(input.previousCode);
  const k = decodeKCode(taxCode);
  const statedIYA = n(input.iyaAmount);
  const previousYearUnderpayment = n(input.previousYearUnderpayment);
  const statePension = n(input.statePension);
  const taxableBenefits = n(input.taxableBenefits);
  const taxableInterestEstimate = n(input.taxableInterestEstimate);
  const remainingPeriods = Math.max(0, Math.floor(n(input.remainingPayPeriods)));
  const basisMarker = /(W1|M1|X|NONCUM)$/.test(taxCode) ? taxCode.match(/(W1|M1|X|NONCUM)$/)[1] : null;

  const reasons = [];
  if (previousYearUnderpayment > 0) reasons.push({title:'Earlier-year underpayment',amount:previousYearUnderpayment,evidenceClass:'OBSERVED'});
  if (statePension > 0) reasons.push({title:'State Pension or other taxable state benefit',amount:statePension,evidenceClass:'OBSERVED'});
  if (taxableBenefits > 0) reasons.push({title:'Taxable benefits',amount:taxableBenefits,evidenceClass:'OBSERVED'});
  if (taxableInterestEstimate > 0) reasons.push({title:'Taxable savings interest estimate',amount:taxableInterestEstimate,evidenceClass:'OBSERVED'});

  const scenes = [
    {id:'START',title:'Why did my tax code change?',evidenceClass:'OBSERVED',detail:`Current code: ${taxCode || 'not supplied'}${previousCode ? `; previous code: ${previousCode}` : ''}.`},
    ...(k ? [{id:'KCODE',title:'What the K means',evidenceClass:'INFERRED',detail:k.explanation,guardrail:k.fiftyPercentGuardrail}] : []),
    ...(reasons.length ? [{id:'DEDUCTIONS',title:'What may be feeding the code',evidenceClass:'OBSERVED',items:reasons}] : []),
    ...(statedIYA > 0 ? [{id:'IYA',title:'What the IYA means',evidenceClass:'OBSERVED',detail:`HMRC has identified £${statedIYA.toFixed(2)} of extra tax to collect during the current tax year. The associated coding restriction is intended to collect that amount over the remaining pay periods.`}] : []),
    ...(basisMarker ? [{id:'BASIS',title:'Why W1/M1/X matters',evidenceClass:'OBSERVED',detail:`The ${basisMarker} marker means payroll is operating the code on a non-cumulative basis for the current pay period rather than recalculating the whole year to date.`}] : []),
    ...(statedIYA > 0 && remainingPeriods > 0 ? [{id:'SPREAD',title:'Payday road',evidenceClass:'ILLUSTRATIVE',detail:`An equal-spread picture would be about £${(statedIYA/remainingPeriods).toFixed(2)} across ${remainingPeriods} remaining pay periods. This is only a visual aid, not HMRC's actual IYAR formula.`}] : []),
    {id:'END',title:'Underpayment is the result, not the mystery',evidenceClass:'INFERRED',detail:'The underpayment is the difference between tax that should have been collected and tax actually collected. The forensic task is to identify which income, estimate, code, timing or payroll event created that difference.'}
  ];

  return {
    version:'25',
    taxCode,
    previousCode,
    kCode:k,
    iyaAmount:statedIYA,
    previousYearUnderpayment,
    basisMarker,
    reasons,
    scenes,
    customerSummary: k
      ? 'Your K code is not a penalty. It is a PAYE collection mechanism used when coding deductions are greater than coding allowances.'
      : 'Your tax code should be read together with any IYA or underpayment information, because the code is the collection mechanism and the underpayment is the amount being reconciled.',
    guardrail:'PAYE Forensics explains possible mechanics from confirmed facts. It does not reproduce HMRC NPS, determine fault, or issue a replacement tax code.'
  };
}
