// PAYE Forensics v19 - Starter Declaration Coach
// Plain-English prevention aid. It does not replace the official HMRC starter checklist.

export function coachStarterDeclaration(input = {}) {
  const {
    hasP45 = false,
    anotherJobLive = false,
    previousJobEnded = false,
    receivedBenefitsOrPensionThisTaxYear = false,
    hasBeenPaidByNewEmployer = false
  } = input;

  const findings = [];
  let suggestedStatement = null;

  if (hasBeenPaidByNewEmployer) {
    findings.push({
      level: 'INFO',
      title: 'You have already been paid',
      explanation: 'Once the first pay has happened, PAYE Forensics should switch from declaration coaching to checking the actual payslip code and the HMRC current-year record.',
      action: 'Use the New Job Tax Code Health Check instead of trying to recreate the original starter declaration.'
    });
  }

  if (anotherJobLive) {
    suggestedStatement = 'C';
    findings.push({
      level: 'HIGH',
      title: 'Another job is still live',
      explanation: 'This is the key fact for avoiding accidental use of a full Personal Allowance at the new job.',
      action: 'Review the official starter checklist carefully and make sure the declaration reflects that another job still exists.'
    });
  } else if (previousJobEnded && !hasP45) {
    suggestedStatement = receivedBenefitsOrPensionThisTaxYear ? 'B' : 'A';
    findings.push({
      level: 'MEDIUM',
      title: 'Previous job ended but no P45 is available',
      explanation: 'The declaration route depends on what other taxable income or benefits you have had in the tax year.',
      action: 'Check the official wording before confirming the declaration.'
    });
  } else if (!hasP45 && !previousJobEnded && !anotherJobLive) {
    findings.push({
      level: 'MEDIUM',
      title: 'No P45 and job history is unclear',
      explanation: 'This is a higher-risk setup because payroll has less information to work from.',
      action: 'Confirm whether any previous employment ended and whether any other job remains live before completing the declaration.'
    });
  }

  return {
    suggestedStatement,
    findings,
    summary: {
      hasP45,
      anotherJobLive,
      previousJobEnded,
      receivedBenefitsOrPensionThisTaxYear,
      hasBeenPaidByNewEmployer
    },
    guardrail: 'This coach explains risk patterns in plain English. It does not complete the official HMRC declaration for the customer and does not guarantee a payroll tax code.'
  };
}
