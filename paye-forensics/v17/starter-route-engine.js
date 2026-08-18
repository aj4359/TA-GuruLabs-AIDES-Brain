export const STARTER_ROUTE = Object.freeze({
  P45: 'P45_ROUTE',
  A: 'STATEMENT_A',
  B: 'STATEMENT_B',
  C: 'STATEMENT_C',
  NONE: 'NO_DECLARATION',
});

const normaliseCode = (value = '') => String(value).toUpperCase().replace(/\s+/g, '');
const hasNonCumulativeMarker = (code) => /(W1|M1|X|NONCUM)/.test(normaliseCode(code));
const isFullAllowanceNumeric = (code) => /^(S|C)?1257L(?:W1|M1|X|NONCUM)?$/.test(normaliseCode(code));
const isBRFamily = (code) => /^(S|C)?BR(?:W1|M1|X|NONCUM)?$/.test(normaliseCode(code));
const is0T = (code) => /^(S|C)?0T(?:W1|M1|X|NONCUM)?$/.test(normaliseCode(code));

export function expectedStarterRoute(input = {}) {
  const declaration = String(input.declaration || '').toUpperCase();
  const hasP45 = Boolean(input.hasP45);
  const anotherJobLive = Boolean(input.anotherJobLive);
  const previousJobEnded = Boolean(input.previousJobEnded);

  if (hasP45) {
    return {
      route: STARTER_ROUTE.P45,
      expectedCodeFamily: 'P45-derived or later HMRC-issued code',
      confidence: 'SUPPORTED',
      rationale: 'A valid P45 normally supplies previous pay, tax and code information for the new payroll record.',
    };
  }

  if (!declaration) {
    return {
      route: STARTER_ROUTE.NONE,
      expectedCodeFamily: '0T Week 1/Month 1 starter route',
      confidence: 'SUPPORTED',
      rationale: 'No P45 and no starter declaration points to the no-declaration starter route.',
    };
  }

  if (declaration === 'C') {
    return {
      route: STARTER_ROUTE.C,
      expectedCodeFamily: 'BR-family secondary-job starter route',
      confidence: anotherJobLive ? 'SUPPORTED' : 'POSSIBLE_CONFLICT',
      rationale: anotherJobLive
        ? 'Statement C is consistent with another live job or pension using the main allowance.'
        : 'Statement C can be inconsistent where no other employment or pension is actually continuing.',
    };
  }

  if (declaration === 'A') {
    return {
      route: STARTER_ROUTE.A,
      expectedCodeFamily: 'Standard-allowance starter route, subject to payroll/HMRC rules',
      confidence: anotherJobLive ? 'POSSIBLE_CONFLICT' : 'SUPPORTED',
      rationale: anotherJobLive
        ? 'Statement A appears inconsistent with a continuing job and may expose duplicate allowance risk.'
        : 'Statement A may be consistent where there has been no other job/pension in the tax year and other conditions are met.',
    };
  }

  if (declaration === 'B') {
    return {
      route: STARTER_ROUTE.B,
      expectedCodeFamily: 'Standard-allowance non-cumulative starter route, subject to payroll/HMRC rules',
      confidence: anotherJobLive ? 'POSSIBLE_CONFLICT' : 'SUPPORTED',
      rationale: anotherJobLive
        ? 'Statement B appears inconsistent with another continuing job and may expose duplicate allowance risk.'
        : previousJobEnded
          ? 'Statement B may be consistent where there was an earlier job in the tax year that has ended.'
          : 'Statement B may be consistent, but previous-employment facts should be checked.',
    };
  }

  return {
    route: 'UNKNOWN',
    expectedCodeFamily: 'Unknown',
    confidence: 'CHECK_INPUT',
    rationale: 'Starter declaration could not be interpreted.',
  };
}

export function compareExpectedToActual(input = {}) {
  const expected = expectedStarterRoute(input);
  const actualCode = normaliseCode(input.actualFirstPayslipCode);
  const hmrcCode = normaliseCode(input.hmrcCurrentYearCode);
  const previousCode = normaliseCode(input.previousJobCode);
  const anotherJobLive = Boolean(input.anotherJobLive);
  const knownHmrcIssuedCode = Boolean(input.knownHmrcIssuedCode);
  const findings = [];

  if (!actualCode) {
    findings.push({
      id: 'MISSING_FIRST_PAYSLIP_CODE',
      severity: 'CHECK',
      evidence: 'OBSERVED_GAP',
      text: 'First-payslip tax code has not been confirmed yet.',
    });
  }

  if (expected.route === STARTER_ROUTE.C && actualCode && !isBRFamily(actualCode) && !knownHmrcIssuedCode) {
    findings.push({
      id: 'STATEMENT_C_ROUTE_MISMATCH',
      severity: 'HIGH',
      evidence: 'INFERRED',
      text: `Statement C points toward a secondary-job starter route, but the first payslip shows ${actualCode}. Check whether HMRC issued a different code.`
    });
  }

  if (expected.route === STARTER_ROUTE.NONE && actualCode && !(is0T(actualCode) && hasNonCumulativeMarker(actualCode)) && !knownHmrcIssuedCode) {
    findings.push({
      id: 'NO_DECLARATION_ROUTE_MISMATCH',
      severity: 'HIGH',
      evidence: 'INFERRED',
      text: 'No declaration was recorded, but the first-payslip code does not resemble the expected no-declaration 0T non-cumulative starter route.'
    });
  }

  if (anotherJobLive && isFullAllowanceNumeric(actualCode) && !knownHmrcIssuedCode) {
    findings.push({
      id: 'POSSIBLE_DUPLICATE_ALLOWANCE',
      severity: 'HIGH',
      evidence: 'INFERRED',
      text: 'Another job is still live and this new job appears to be using the full standard Personal Allowance. This is a duplicate-allocation risk indicator, not proof of an error.'
    });
  }

  if (!input.hasP45 && previousCode && actualCode === previousCode && !knownHmrcIssuedCode) {
    findings.push({
      id: 'POSSIBLE_PRIOR_CODE_CARRY_FORWARD',
      severity: 'CHECK',
      evidence: 'INFERRED',
      text: `The first-payslip code matches the previous job code (${actualCode}) despite no P45 being recorded. Check how payroll obtained the code.`
    });
  }

  if (hmrcCode && actualCode && hmrcCode !== actualCode) {
    findings.push({
      id: 'PAYROLL_HMRC_DELTA',
      severity: 'CHECK',
      evidence: 'OBSERVED',
      text: `Payroll shows ${actualCode}, while the confirmed HMRC current-year code is ${hmrcCode}. Timing and issue dates need checking before concluding there is an error.`
    });
  }

  return {
    expected,
    actual: {
      firstPayslipCode: actualCode || null,
      hmrcCurrentYearCode: hmrcCode || null,
      previousJobCode: previousCode || null,
      knownHmrcIssuedCode,
    },
    routeMatchState: findings.some(f => f.severity === 'HIGH') ? 'POSSIBLE_MISMATCH' : findings.length ? 'CHECK' : 'NO_OBVIOUS_CONFLICT',
    findings,
    guardrail: 'This comparison models a possible starter route from confirmed information. It does not prove that payroll, the employer or HMRC made an error and it does not issue tax codes.'
  };
}
