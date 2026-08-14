(function(){
  const R = window.PAYE_RULES_2026_27;
  if (!R) throw new Error('PAYE rules not loaded');

  const n = v => Math.max(0, Number(v || 0));
  const round2 = v => Math.round((v + Number.EPSILON) * 100) / 100;

  function personalAllowance(adjustedNetIncome) {
    const ani = n(adjustedNetIncome);
    if (ani <= R.personalAllowanceTaperStart) return R.personalAllowance;
    const reduction = Math.floor((ani - R.personalAllowanceTaperStart) / 2);
    return Math.max(0, R.personalAllowance - reduction);
  }

  function taxAcrossBands(amount, bands) {
    let remaining = n(amount), tax = 0, rows = [];
    for (const band of bands) {
      if (remaining <= 0) break;
      const slice = Math.min(remaining, band.width);
      const bandTax = slice * band.rate;
      rows.push({ ruleId: band.id, label: band.label, amount: round2(slice), rate: band.rate, tax: round2(bandTax) });
      tax += bandTax;
      remaining -= slice;
    }
    return { tax: round2(tax), rows };
  }

  function ukRateSlices(amount, startingPosition, bands) {
    let remaining = n(amount), position = n(startingPosition), tax = 0, rows = [];
    for (const band of bands) {
      if (remaining <= 0) break;
      const upper = band.upper;
      if (position >= upper) continue;
      const room = upper === Infinity ? remaining : Math.max(0, upper - position);
      const slice = Math.min(remaining, room);
      if (slice <= 0) continue;
      const bandTax = slice * band.rate;
      rows.push({ ruleId: band.id, amount: round2(slice), rate: band.rate, tax: round2(bandTax) });
      tax += bandTax;
      position += slice;
      remaining -= slice;
    }
    return { tax: round2(tax), rows, endPosition: position };
  }

  function parseTaxCodeAllowance(code) {
    const m = String(code || '').toUpperCase().match(/(\d{1,4})/);
    if (!m) return null;
    return Number(m[1]) * 10 + 9;
  }

  function rankScenarios(input, result) {
    const candidates = [];
    const push = (id, title, evidence, score, detail) => candidates.push({ id, title, evidence, score, detail });

    const oldSavings = n(input.previousSavingsEstimate);
    const newSavings = n(input.savingsInterest);
    if (oldSavings !== newSavings && (oldSavings > 0 || newSavings > 0)) {
      push('SAVINGS_ESTIMATE_CHANGED','Savings interest estimate changed',`${oldSavings.toFixed(0)} → ${newSavings.toFixed(0)}`,Math.min(95,55 + Math.abs(newSavings-oldSavings)/25),'A changed savings estimate can alter the amount of tax HMRC attempts to collect through PAYE.');
    }

    const oldIncome = n(input.previousNonSavingsEstimate);
    const currentIncome = result.nonSavingsGross;
    if (oldIncome !== currentIncome && (oldIncome > 0 || currentIncome > 0)) {
      push('INCOME_ESTIMATE_CHANGED','Income estimate changed',`${oldIncome.toFixed(0)} → ${currentIncome.toFixed(0)}`,Math.min(95,50 + Math.abs(currentIncome-oldIncome)/100),'A revised employment or pension estimate can change the projected annual liability.');
    }

    if (n(input.secondJobIncome) > 0) push('SECOND_JOB','Second employment present',`£${n(input.secondJobIncome).toFixed(0)}`,72,'A second job can use a separate code and may change which income falls into higher tax bands.');
    if (n(input.privatePension) > 0 || n(input.statePension) > 0) push('PENSION','Pension income present',`£${(n(input.privatePension)+n(input.statePension)).toFixed(0)}`,58,'Pension income can affect PAYE coding, especially where State Pension is collected indirectly through another PAYE source.');
    if (n(input.benefitsInKind) > 0) push('BENEFIT','Taxable benefit entered',`£${n(input.benefitsInKind).toFixed(0)}`,68,'A taxable benefit can reduce tax-free allowances in a PAYE code.');
    if (n(input.isaIncome) > 0) push('ISA_CHECK','ISA income separated',`£${n(input.isaIncome).toFixed(0)}`,80,'ISA income has been kept outside ordinary taxable savings/dividend income in this reconstruction.');

    const oldAllow = parseTaxCodeAllowance(input.oldTaxCode);
    const newAllow = parseTaxCodeAllowance(input.newTaxCode);
    if (oldAllow !== null && newAllow !== null && oldAllow !== newAllow) {
      const delta = oldAllow - newAllow;
      push('CODE_ALLOWANCE_CHANGE','Tax-code allowance appears to have changed',`${oldAllow} → ${newAllow}`,75,`A simple numeric-code reading suggests roughly £${Math.abs(delta).toFixed(0)} ${delta>0?'less':'more'} tax-free allowance. This is only indicative because suffixes, prefixes and special codes can change interpretation.`);
    }

    if (result.taxDue > n(input.taxAlreadyDeducted) && n(input.taxAlreadyDeducted) > 0) {
      push('DEDUCTION_GAP','Tax deducted is below reconstructed liability',`£${result.taxDue.toFixed(2)} due vs £${n(input.taxAlreadyDeducted).toFixed(2)} deducted`,88,'On the figures entered, this gap directly contributes to the reconstructed underpayment.');
    }

    return candidates.sort((a,b)=>b.score-a.score).slice(0,5);
  }

  function calculate(input) {
    const employment = n(input.employmentIncome);
    const secondJob = n(input.secondJobIncome);
    const privatePension = n(input.privatePension);
    const statePension = n(input.statePension);
    const benefits = n(input.benefitsInKind);
    const otherNonSavings = n(input.otherNonSavings);
    const savingsGross = n(input.savingsInterest);
    const isaIncome = n(input.isaIncome);
    const dividendsGross = n(input.dividends);
    const nonSavingsGross = employment + secondJob + privatePension + statePension + benefits + otherNonSavings;
    const grossRelevantIncome = nonSavingsGross + savingsGross + dividendsGross;
    const ani = input.adjustedNetIncome === '' || input.adjustedNetIncome == null ? grossRelevantIncome : n(input.adjustedNetIncome);
    const pa = personalAllowance(ani);

    let allowanceLeft = pa;
    const paToNonSavings = Math.min(nonSavingsGross, allowanceLeft); allowanceLeft -= paToNonSavings;
    const taxableNonSavings = Math.max(0, nonSavingsGross - paToNonSavings);
    const paToSavings = Math.min(savingsGross, allowanceLeft); allowanceLeft -= paToSavings;
    const savingsAfterPA = Math.max(0, savingsGross - paToSavings);
    const paToDividends = Math.min(dividendsGross, allowanceLeft); allowanceLeft -= paToDividends;
    const dividendsAfterPA = Math.max(0, dividendsGross - paToDividends);

    const savingsStartAvailable = Math.max(0, R.startingRateSavingsLimit - taxableNonSavings);
    const savingsStartUsed = Math.min(savingsAfterPA, savingsStartAvailable);
    const savingsAfterStart = Math.max(0, savingsAfterPA - savingsStartUsed);

    // Savings/dividend band status follows UK savings/dividend bands, including for Scottish taxpayers.
    const ukPositionBeforeSavings = taxableNonSavings;
    const projectedTopPosition = ukPositionBeforeSavings + savingsAfterStart + dividendsAfterPA;
    const psaBand = projectedTopPosition > 125140 ? 'additional' : projectedTopPosition > 37700 ? 'higher' : 'basic';
    const psa = R.personalSavingsAllowance[psaBand];
    const psaUsed = Math.min(savingsAfterStart, psa);
    const taxableSavings = Math.max(0, savingsAfterStart - psaUsed);

    const dividendAllowanceUsed = Math.min(dividendsAfterPA, R.dividendAllowance);
    const taxableDividends = Math.max(0, dividendsAfterPA - dividendAllowanceUsed);

    const nsBands = input.jurisdiction === 'Scotland' ? R.scotlandNonSavingsBands : R.mainNonSavingsBands;
    const nsTax = taxAcrossBands(taxableNonSavings, nsBands);
    const savingsTax = ukRateSlices(taxableSavings, ukPositionBeforeSavings, R.ukSavingsBands);
    const dividendStartPosition = ukPositionBeforeSavings + taxableSavings;
    const dividendTax = ukRateSlices(taxableDividends, dividendStartPosition, R.ukDividendBands);
    const taxDue = round2(nsTax.tax + savingsTax.tax + dividendTax.tax);
    const deducted = n(input.taxAlreadyDeducted);
    const reconstructedUnderpayment = round2(Math.max(0, taxDue - deducted));
    const stated = n(input.hmrcStatedUnderpayment);
    const difference = round2(Math.abs(stated - reconstructedUnderpayment));

    const relativeTolerance = stated > 0 ? difference / stated : difference;
    let confidence = difference <= 5 ? 'Likely explanation' : (difference <= 50 || relativeTolerance <= 0.15) ? 'Possible explanation' : 'Unable to reconcile';

    const remainingPayPeriods = Math.max(0, Math.floor(n(input.remainingPayPeriods)));
    const indicativePerPayday = remainingPayPeriods ? round2(stated / remainingPayPeriods) : null;

    const result = {
      engineVersion: 'PAYE-FORensics-v2.0', ruleSetId: R.id, taxYear: R.taxYear,
      jurisdiction: input.jurisdiction || 'England & Northern Ireland',
      nonSavingsGross: round2(nonSavingsGross), savingsGross: round2(savingsGross), isaIncomeExcluded: round2(isaIncome), dividendsGross: round2(dividendsGross),
      adjustedNetIncomeUsed: round2(ani), personalAllowance: round2(pa), paAllocation: { nonSavings: round2(paToNonSavings), savings: round2(paToSavings), dividends: round2(paToDividends) },
      taxableNonSavings: round2(taxableNonSavings), savingsStartAvailable: round2(savingsStartAvailable), savingsStartUsed: round2(savingsStartUsed),
      personalSavingsAllowanceBand: psaBand, personalSavingsAllowance: psa, personalSavingsAllowanceUsed: round2(psaUsed), taxableSavings: round2(taxableSavings),
      dividendAllowance: R.dividendAllowance, dividendAllowanceUsed: round2(dividendAllowanceUsed), taxableDividends: round2(taxableDividends),
      nonSavingsTax: nsTax, savingsTax, dividendTax, taxDue,
      taxAlreadyDeducted: round2(deducted), hmrcStatedUnderpayment: round2(stated), reconstructedUnderpayment, difference, confidence,
      iyaIllustration: { remainingPayPeriods, indicativeExtraPerPayday: indicativePerPayday, warning: 'Illustrative only. Actual PAYE collection depends on code basis, payroll timing and HMRC coding instructions.' },
      warnings: [], audit: { assumptions: [], sources: R.sources }
    };

    if (input.adjustedNetIncome === '' || input.adjustedNetIncome == null) result.audit.assumptions.push('Adjusted net income was approximated using entered taxable income. Pension contributions, Gift Aid and other ANI adjustments were not supplied.');
    if (isaIncome > 0) result.warnings.push(`£${isaIncome.toFixed(2)} ISA income was excluded from ordinary taxable savings/dividend income.`);
    if (ani > R.personalAllowanceTaperStart) result.warnings.push(`Personal Allowance tapered because adjusted net income used was above £${R.personalAllowanceTaperStart.toLocaleString('en-GB')}.`);
    if (difference > Math.max(50, stated * 0.15)) result.warnings.push('The reconstructed figure does not closely match the HMRC-stated amount. Check for missing estimates, benefits, pensions, prior-period adjustments, code basis or tax-deducted figures.');

    result.scenarios = rankScenarios(input, result);
    return result;
  }

  window.PAYEForensicsV2 = { calculate, parseTaxCodeAllowance };
})();
