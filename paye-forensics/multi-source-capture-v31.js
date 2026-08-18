// TA GuruLabs PAYE Forensics v31 - confirmed multi-source PAYE capture
// Copyright © TA GuruLabs. Confidential implementation concept.

const norm = v => String(v || '').toUpperCase().replace(/\s+/g,'');
const n = v => Math.max(0, Number(v || 0));

export function normaliseSource(source = {}, index = 0) {
  return {
    id: source.id || `source-${index+1}`,
    label: source.label || `PAYE source ${index+1}`,
    type: source.type || 'employment',
    annualIncome: n(source.annualIncome),
    taxCode: norm(source.taxCode),
    taxDeducted: n(source.taxDeducted),
    active: source.active !== false,
    confirmed: source.confirmed === true,
    evidenceType: source.evidenceType || 'manual',
    evidenceLabel: source.evidenceLabel || 'Customer confirmed',
    sourceDate: source.sourceDate || null
  };
}

export function buildConfirmedSourceSet(input = {}) {
  const sources = (Array.isArray(input.sources) ? input.sources : []).map(normaliseSource);
  const confirmed = sources.filter(s => s.active && s.confirmed);
  const unconfirmed = sources.filter(s => s.active && !s.confirmed);

  const totals = confirmed.reduce((acc, s) => {
    if (s.type === 'employment') acc.employmentIncome += s.annualIncome;
    else if (s.type === 'private-pension') acc.privatePension += s.annualIncome;
    else acc.otherNonSavings += s.annualIncome;
    acc.taxAlreadyDeducted += s.taxDeducted;
    return acc;
  }, { employmentIncome:0, privatePension:0, otherNonSavings:0, taxAlreadyDeducted:0 });

  return {
    version:'31',
    sources,
    confirmed,
    unconfirmed,
    gatePassed: unconfirmed.length === 0 && confirmed.length > 0,
    totals,
    activeSources: confirmed.map(s => ({
      id:s.id,label:s.label,type:s.type,income:s.annualIncome,taxCode:s.taxCode,active:true,evidence:'OBSERVED'
    })),
    warnings: unconfirmed.length ? [`${unconfirmed.length} active PAYE source(s) are not confirmed and are excluded from calculation.`] : [],
    guardrail:'Only customer-confirmed active PAYE source facts are promoted into the deterministic calculation.'
  };
}
