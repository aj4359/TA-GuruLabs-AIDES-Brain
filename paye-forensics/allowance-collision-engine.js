// PAYE Forensics v18 - Personal Allowance Collision Engine
// Diagnostic/illustrative only. It does not determine or issue HMRC tax codes.

const FULL_ALLOWANCE_CODE_RE = /^(?:S|C)?1257[LMN]?$/i;

function normaliseCode(code = '') {
  return String(code).toUpperCase().replace(/\s+/g, '');
}

function numericAllowance(code = '') {
  const c = normaliseCode(code).replace(/^(S|C)/, '');
  const m = c.match(/^(\d{1,4})[LMN]?/);
  return m ? Number(m[1]) * 10 : 0;
}

function isFullAllowanceCode(code = '') {
  return FULL_ALLOWANCE_CODE_RE.test(normaliseCode(code));
}

export function buildAllowanceCollisionCase({ sources = [], personalAllowance = 12570 } = {}) {
  const active = sources.filter(s => s && s.active !== false);
  const mapped = active.map((s, index) => {
    const code = normaliseCode(s.taxCode);
    const codedAllowance = numericAllowance(code);
    return {
      id: s.id || `source-${index + 1}`,
      label: s.label || `PAYE source ${index + 1}`,
      type: s.type || 'employment',
      income: Number(s.income || 0),
      taxCode: code,
      codedAllowance,
      apparentAllowanceUsed: Math.min(Number(s.income || 0), codedAllowance),
      fullAllowanceSignal: isFullAllowanceCode(code),
      evidence: s.evidence || 'OBSERVED'
    };
  });

  const fullAllowanceSources = mapped.filter(s => s.fullAllowanceSignal);
  const totalNumericCodedAllowance = mapped.reduce((n, s) => n + s.codedAllowance, 0);
  const findings = [];

  if (fullAllowanceSources.length > 1) {
    findings.push({
      id: 'possible-duplicate-full-allowance',
      severity: 'HIGH',
      evidenceClass: 'INFERRED',
      title: 'Possible duplicate Personal Allowance signal',
      explanation: `${fullAllowanceSources.length} active PAYE sources show a 1257-family full-allowance code. That can create an under-deduction risk if the same annual allowance is effectively being used more than once.`,
      affectedSourceIds: fullAllowanceSources.map(s => s.id),
      nextAction: 'Check the current tax code HMRC holds for every active job or pension and compare it with each payslip.'
    });
  }

  if (totalNumericCodedAllowance > personalAllowance && mapped.length > 1) {
    findings.push({
      id: 'coded-allowance-total-above-standard-pa',
      severity: 'MEDIUM',
      evidenceClass: 'INFERRED',
      title: 'Coded allowances need checking across sources',
      explanation: `Numeric code values across active sources total about £${totalNumericCodedAllowance.toLocaleString('en-GB')}, above the standard £${personalAllowance.toLocaleString('en-GB')} Personal Allowance. Codes can include other adjustments, so this is a check prompt rather than proof of an error.`,
      affectedSourceIds: mapped.map(s => s.id),
      nextAction: 'Open each P2/code breakdown and check what allowances and deductions HMRC has allocated to each source.'
    });
  }

  const scenes = [
    { kind: 'ALLOWANCE_ORIGIN', title: 'Your standard Personal Allowance', amount: personalAllowance, evidenceClass: 'INFERRED' },
    ...mapped.map(s => ({
      kind: 'SOURCE_ALLOCATION',
      sourceId: s.id,
      title: s.label,
      taxCode: s.taxCode,
      income: s.income,
      codedAllowance: s.codedAllowance,
      fullAllowanceSignal: s.fullAllowanceSignal,
      evidenceClass: s.evidence
    }))
  ];

  if (fullAllowanceSources.length > 1) {
    scenes.push({
      kind: 'COLLISION',
      title: 'The same allowance may appear to be working in more than one place',
      sourceIds: fullAllowanceSources.map(s => s.id),
      amount: personalAllowance,
      evidenceClass: 'INFERRED',
      warning: 'This visual is diagnostic. It does not prove the codes are wrong and does not calculate an HMRC-issued replacement code.'
    });
  }

  return {
    personalAllowance,
    sources: mapped,
    totalNumericCodedAllowance,
    findings,
    scenes,
    status: findings.some(f => f.severity === 'HIGH') ? 'CHECK_NOW' : findings.length ? 'CHECK' : 'NO_DUPLICATE_SIGNAL',
    guardrail: 'PAYE Forensics interprets observed codes and models possible risk. HMRC determines and issues tax codes.'
  };
}
