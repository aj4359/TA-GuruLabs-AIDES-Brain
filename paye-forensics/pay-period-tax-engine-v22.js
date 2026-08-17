// PAYE Forensics v22 - Automatic Pay-Period Tax Expectation Engine
// Reconstructs a plausible code-based PAYE deduction expectation from confirmed payslip facts.
// It is NOT HMRC payroll software and does not reproduce statutory table rounding or every coding edge case.

const RULES = {
  id: 'UK-2026-27-PERIOD-v1',
  taxYear: '2026/27',
  englandWalesNI: [
    { width: 37700, rate: 0.20, label: 'Basic rate' },
    { width: 87440, rate: 0.40, label: 'Higher rate' },
    { width: Infinity, rate: 0.45, label: 'Additional rate' }
  ],
  scotland: [
    { width: 3967, rate: 0.19, label: 'Starter rate' },
    { width: 12989, rate: 0.20, label: 'Basic rate' },
    { width: 14136, rate: 0.21, label: 'Intermediate rate' },
    { width: 31338, rate: 0.42, label: 'Higher rate' },
    { width: 62710, rate: 0.45, label: 'Advanced rate' },
    { width: Infinity, rate: 0.48, label: 'Top rate' }
  ]
};

const round2 = n => Math.round((Number(n || 0) + Number.EPSILON) * 100) / 100;
const norm = v => String(v || '').toUpperCase().replace(/\s+/g, '');

function periodsPerYear(frequency = 'monthly') {
  const f = String(frequency).toLowerCase();
  if (f === 'weekly') return 52;
  if (f === 'fortnightly') return 26;
  if (f === 'four-weekly' || f === '4-weekly') return 13;
  return 12;
}

function parseCode(rawCode = '') {
  const original = norm(rawCode);
  const nonCumulative = /(W1|M1|NONCUM|X)$/.test(original);
  const strippedMarkers = original.replace(/(W1|M1|NONCUM|X)$/,'');
  const jurisdiction = strippedMarkers.startsWith('S') ? 'Scotland' : strippedMarkers.startsWith('C') ? 'Wales' : 'England/NI';
  const body = strippedMarkers.replace(/^(S|C)/,'');

  if (body === 'BR') return { original, jurisdiction, family:'BR', nonCumulative, allowance:0 };
  if (body === 'D0') return { original, jurisdiction, family:'D0', nonCumulative, allowance:0 };
  if (body === 'D1') return { original, jurisdiction, family:'D1', nonCumulative, allowance:0 };
  if (body === 'NT') return { original, jurisdiction, family:'NT', nonCumulative, allowance:0 };
  if (body === '0T') return { original, jurisdiction, family:'0T', nonCumulative, allowance:0 };
  if (/^K\d+/.test(body)) return { original, jurisdiction, family:'K', nonCumulative, allowance:null, supported:false };

  const m = body.match(/^(\d{1,4})[LMN]?$/);
  if (m) return { original, jurisdiction, family:'NUMERIC', nonCumulative, allowance:Number(m[1]) * 10, supported:true };
  return { original, jurisdiction, family:'UNKNOWN', nonCumulative, allowance:null, supported:false };
}

function taxAcrossBands(taxable, bands, scale = 1) {
  let remaining = Math.max(0, taxable), tax = 0;
  const rows = [];
  for (const band of bands) {
    if (remaining <= 0) break;
    const width = band.width === Infinity ? Infinity : band.width * scale;
    const slice = width === Infinity ? remaining : Math.min(remaining, width);
    const bandTax = slice * band.rate;
    rows.push({ label: band.label, amount: round2(slice), rate: band.rate, tax: round2(bandTax) });
    tax += bandTax;
    remaining -= slice;
  }
  return { tax: round2(tax), rows };
}

function specialRateFor(parsed) {
  if (parsed.family === 'BR') return 0.20;
  if (parsed.family === 'D0') return parsed.jurisdiction === 'Scotland' ? 0.42 : 0.40;
  if (parsed.family === 'D1') return parsed.jurisdiction === 'Scotland' ? 0.45 : 0.45;
  return null;
}

export function reconstructPayPeriods({ payslips = [], frequency = 'monthly' } = {}) {
  const ppy = periodsPerYear(frequency);
  const frames = [];
  let ytdGross = 0;
  let reconstructedTaxYTD = 0;
  let actualTaxYTD = 0;

  payslips.forEach((p, idx) => {
    const gross = Math.max(0, Number(p.gross || 0));
    const actualTax = Math.max(0, Number(p.taxDeducted || 0));
    const parsed = parseCode(p.taxCode);
    ytdGross += gross;
    actualTaxYTD += actualTax;

    let expectedThisPeriod = actualTax;
    let expectedYTD = reconstructedTaxYTD + actualTax;
    let evidenceClass = 'OBSERVED_ONLY';
    let method = 'No supported code reconstruction available; actual deducted tax retained as neutral benchmark.';
    let auditRows = [];
    let warning = null;

    if (parsed.family === 'NT') {
      expectedThisPeriod = 0; expectedYTD = reconstructedTaxYTD;
      evidenceClass = 'INFERRED'; method = 'NT code treated as no income tax deducted for this PAYE source.';
    } else if (specialRateFor(parsed) != null) {
      const rate = specialRateFor(parsed);
      expectedThisPeriod = round2(gross * rate);
      expectedYTD = round2(reconstructedTaxYTD + expectedThisPeriod);
      evidenceClass = 'INFERRED'; method = `${parsed.family} treated as a fixed-rate code for this period.`;
      auditRows = [{ label: parsed.family, amount: round2(gross), rate, tax: expectedThisPeriod }];
    } else if (parsed.family === 'NUMERIC' || parsed.family === '0T') {
      const bands = parsed.jurisdiction === 'Scotland' ? RULES.scotland : RULES.englandWalesNI;
      const allowanceAnnual = parsed.family === 'NUMERIC' ? parsed.allowance : 0;
      if (parsed.nonCumulative) {
        const allowancePeriod = allowanceAnnual / ppy;
        const taxable = Math.max(0, gross - allowancePeriod);
        const calc = taxAcrossBands(taxable, bands, 1 / ppy);
        expectedThisPeriod = calc.tax;
        expectedYTD = round2(reconstructedTaxYTD + expectedThisPeriod);
        auditRows = calc.rows;
        evidenceClass = 'INFERRED';
        method = 'Non-cumulative marker observed: allowance and tax bands applied to this pay period only.';
      } else {
        const periodNumber = Math.max(1, Number(p.taxPeriod || idx + 1));
        const fraction = Math.min(1, periodNumber / ppy);
        const allowanceYTD = allowanceAnnual * fraction;
        const taxableYTD = Math.max(0, ytdGross - allowanceYTD);
        const calc = taxAcrossBands(taxableYTD, bands, fraction);
        expectedYTD = calc.tax;
        expectedThisPeriod = round2(Math.max(0, expectedYTD - reconstructedTaxYTD));
        auditRows = calc.rows;
        evidenceClass = 'INFERRED';
        method = 'Cumulative approximation: current code allowance and rate bands applied to confirmed year-to-date pay.';
      }
    } else if (parsed.family === 'K') {
      warning = 'K-code exact pay-period reconstruction is deferred because K codes require additional coding-restriction and regulatory-limit handling.';
    } else {
      warning = 'Tax code family is not yet supported for automatic period reconstruction.';
    }

    reconstructedTaxYTD = round2(expectedYTD);
    const periodGap = round2(expectedThisPeriod - actualTax);
    const possibleShortfall = round2(Math.max(0, reconstructedTaxYTD - actualTaxYTD));
    const possibleOverdeduction = round2(Math.max(0, actualTaxYTD - reconstructedTaxYTD));

    frames.push({
      period: p.period || idx + 1,
      taxPeriod: p.taxPeriod || idx + 1,
      gross: round2(gross),
      taxCode: parsed.original || null,
      actualTax: round2(actualTax),
      reconstructedExpectedTax: round2(expectedThisPeriod),
      actualTaxYTD: round2(actualTaxYTD),
      reconstructedTaxYTD: round2(reconstructedTaxYTD),
      periodGap,
      possibleShortfall,
      possibleOverdeduction,
      code: parsed,
      method,
      auditRows,
      evidenceClass,
      warning
    });
  });

  return {
    engineVersion: '22.0',
    ruleSetId: RULES.id,
    taxYear: RULES.taxYear,
    frequency,
    periodsPerYear: ppy,
    frames,
    reconstructedTaxYTD: round2(reconstructedTaxYTD),
    actualTaxYTD: round2(actualTaxYTD),
    possibleShortfall: round2(Math.max(0, reconstructedTaxYTD - actualTaxYTD)),
    possibleOverdeduction: round2(Math.max(0, actualTaxYTD - reconstructedTaxYTD)),
    disclaimer: 'Automatic code-based reconstruction only. It is not HMRC payroll software, does not reproduce every statutory rounding/table rule, and does not prove a payroll error.'
  };
}

export { parseCode, periodsPerYear };
