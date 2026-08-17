// PAYE Forensics v23 - Cash Flow Story
// Separates deduction timing from annual liability and narrates code changes safely.

const n = v => Math.round(Number(v || 0) * 100) / 100;
const norm = v => String(v || '').toUpperCase().replace(/\s+/g, '');

export function buildCashFlowStory({ frames = [], hmrcUnderpayment = 0 } = {}) {
  let cumulativeActual = 0;
  let cumulativeReconstructed = 0;
  let previousCode = null;
  const scenes = [];

  for (const frame of frames) {
    const actual = n(frame.taxDeducted);
    const reconstructed = n(frame.reconstructedTax ?? frame.reconstructedExpectedTax);
    const code = norm(frame.taxCode);
    cumulativeActual = n(cumulativeActual + actual);
    cumulativeReconstructed = n(cumulativeReconstructed + reconstructed);
    const timingGap = n(cumulativeReconstructed - cumulativeActual);

    if (previousCode && code && code !== previousCode) {
      scenes.push({
        kind: 'CODE_CHANGE',
        evidenceClass: 'OBSERVED',
        period: frame.period,
        title: `Tax code changed from ${previousCode} to ${code}`,
        explanation: 'A code change can alter when tax is collected from later pay. It does not by itself prove that annual tax liability changed by the same amount.'
      });
    }

    scenes.push({
      kind: 'PAY_PERIOD',
      evidenceClass: 'MIXED',
      period: frame.period,
      gross: n(frame.gross),
      taxCode: code,
      actualTax: actual,
      reconstructedTax: reconstructed,
      periodDifference: n(reconstructed - actual),
      cumulativeActual,
      cumulativeReconstructed,
      cumulativeTimingGap: timingGap,
      title: timingGap > 0 ? 'Possible under-deduction building' : timingGap < 0 ? 'Possible over-deduction / catch-up' : 'Deductions broadly aligned in this reconstruction'
    });

    previousCode = code || previousCode;
  }

  const stated = n(hmrcUnderpayment);
  const reconstructedGap = scenes.filter(s=>s.kind==='PAY_PERIOD').length ? n(cumulativeReconstructed - cumulativeActual) : 0;
  const difference = n(Math.abs(stated - Math.max(0, reconstructedGap)));

  return {
    scenes,
    summary: {
      actualTaxCollected: cumulativeActual,
      reconstructedTaxCollected: cumulativeReconstructed,
      reconstructedTimingGap: reconstructedGap,
      hmrcStatedUnderpayment: stated,
      reconciliationDifference: difference
    },
    warnings: [
      'Deduction timing and annual tax liability are different concepts.',
      'A later code change can collect more or less tax without meaning that the same amount of annual liability was newly created.',
      'This story is a possible reconstruction from confirmed payslip facts, not a reproduction of HMRC or payroll software.'
    ]
  };
}
