// PAYE Forensics v24 - Pensioner Allowance Split Explainer
// Explains how one Personal Allowance may be allocated across multiple small pensions
// while untaxed savings interest can reduce the net allowance available for PAYE coding.

const round2 = n => Math.round((Number(n || 0) + Number.EPSILON) * 100) / 100;
const norm = v => String(v || '').toUpperCase().replace(/\s+/g, '');

export function buildPensionerAllowanceSplit(input = {}) {
  const pa = Number(input.personalAllowance || 12570);
  const pensions = (Array.isArray(input.pensions) ? input.pensions : []).map((p, i) => ({
    id: p.id || `pension-${i+1}`,
    label: p.label || `Pension ${i+1}`,
    annualIncome: Math.max(0, Number(p.annualIncome || 0)),
    taxCode: norm(p.taxCode || ''),
    observed: p.observed !== false
  }));
  const statePension = Math.max(0, Number(input.statePension || 0));
  const untaxedInterest = Math.max(0, Number(input.untaxedInterest || 0));
  const savingsZeroRateCoverage = Math.max(0, Number(input.savingsZeroRateCoverage || 0)); // SSR + PSA amount actually covering interest
  const interestPotentiallyTaxable = Math.max(0, untaxedInterest - savingsZeroRateCoverage);

  // Coding illustration only: show how untaxed income may consume/reduce allowance available in codes.
  // We do not assert HMRC will code the full taxable interest amount pound-for-pound in every case.
  const illustrativeNetAllowancePool = Math.max(0, pa - statePension - interestPotentiallyTaxable);

  let remaining = illustrativeNetAllowancePool;
  const allocations = pensions.map((p, i) => {
    const allocated = Math.min(p.annualIncome, remaining);
    remaining -= allocated;
    return {
      ...p,
      illustrativeAllowanceAllocated: round2(allocated),
      illustrativeTaxableRemainder: round2(Math.max(0, p.annualIncome - allocated)),
      allocationRole: i === 0 ? 'PRIMARY-LIKE' : 'SECONDARY-LIKE'
    };
  });

  const totalPensionIncome = pensions.reduce((n,p)=>n+p.annualIncome,0);
  const totalAllocated = allocations.reduce((n,p)=>n+p.illustrativeAllowanceAllocated,0);

  const findings = [];
  if (pensions.length >= 3) findings.push({
    evidenceClass:'OBSERVED',
    title:'Multiple pension sources',
    detail:`${pensions.length} occupational/private pension sources are being considered separately.`
  });
  if (statePension > 0) findings.push({
    evidenceClass:'INFERRED',
    title:'State Pension may absorb part of the available allowance',
    detail:'State Pension is taxable but normally paid without PAYE deduction, so PAYE coding may use allowance at another pension source to collect the tax due.'
  });
  if (untaxedInterest > 0) findings.push({
    evidenceClass:'INFERRED',
    title:'Untaxed savings interest may reduce the allowance left for pension codes',
    detail:`Untaxed interest entered: £${round2(untaxedInterest).toFixed(2)}. Zero-rate savings coverage entered: £${round2(savingsZeroRateCoverage).toFixed(2)}.`
  });
  if (remaining > 0) findings.push({
    evidenceClass:'ILLUSTRATIVE',
    title:'Possible surplus allowance remains after these pension allocations',
    detail:`About £${round2(remaining).toFixed(2)} remains in this illustration. HMRC may allocate surplus allowance differently across pension sources.`
  });
  if (totalPensionIncome > illustrativeNetAllowancePool) findings.push({
    evidenceClass:'ILLUSTRATIVE',
    title:'Some pension income remains taxable after the illustrated allowance split',
    detail:`Illustrated pension income £${round2(totalPensionIncome).toFixed(2)} versus illustrated allowance pool £${round2(illustrativeNetAllowancePool).toFixed(2)}.`
  });

  return {
    version:'24',
    personalAllowance: round2(pa),
    statePension: round2(statePension),
    untaxedInterest: round2(untaxedInterest),
    savingsZeroRateCoverage: round2(savingsZeroRateCoverage),
    interestPotentiallyTaxable: round2(interestPotentiallyTaxable),
    illustrativeNetAllowancePool: round2(illustrativeNetAllowancePool),
    allocations,
    totalPensionIncome: round2(totalPensionIncome),
    totalAllocated: round2(totalAllocated),
    surplusIllustrativeAllowance: round2(remaining),
    findings,
    scenes:[
      {kind:'PA_ORIGIN',title:'Start with one Personal Allowance',amount:round2(pa),evidenceClass:'INFERRED'},
      ...(statePension>0?[{kind:'STATE_PENSION',title:'State Pension uses part of the tax-free capacity',amount:round2(statePension),evidenceClass:'INFERRED'}]:[]),
      ...(untaxedInterest>0?[{kind:'INTEREST',title:'Untaxed interest can also affect coding',amount:round2(untaxedInterest),zeroRateCoverage:round2(savingsZeroRateCoverage),evidenceClass:'INFERRED'}]:[]),
      ...allocations.map(a=>({kind:'PENSION_ALLOCATION',title:a.label,income:a.annualIncome,allowance:a.illustrativeAllowanceAllocated,taxableRemainder:a.illustrativeTaxableRemainder,evidenceClass:a.observed?'OBSERVED':'ILLUSTRATIVE'})),
      {kind:'SUMMARY',title:'One allowance, several pension sources',remaining:round2(remaining),evidenceClass:'ILLUSTRATIVE'}
    ],
    guardrail:'This is an explanatory allocation model, not a reproduction of HMRC NPS coding or a replacement tax code. HMRC may allocate allowances and deductions differently between primary and secondary pension sources.'
  };
}
