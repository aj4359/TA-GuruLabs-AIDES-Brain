/* PAYE Forensics v2 regression suite.
   Run in browser after rules-2026-27.js and engine-v2.js.
   These are guardrails for deterministic behaviour, not a substitute for HMRC validation. */
(function(){
  const E = window.PAYEForensicsV2;
  if (!E) throw new Error('PAYEForensicsV2 not loaded');

  const base = {
    jurisdiction: 'England & Northern Ireland',
    employmentIncome: 0, secondJobIncome: 0, privatePension: 0, statePension: 0,
    benefitsInKind: 0, otherNonSavings: 0, savingsInterest: 0, isaIncome: 0,
    dividends: 0, adjustedNetIncome: '', taxAlreadyDeducted: 0,
    hmrcStatedUnderpayment: 0, previousSavingsEstimate: 0,
    previousNonSavingsEstimate: 0, oldTaxCode: '1257L', newTaxCode: '1257L',
    remainingPayPeriods: 0
  };
  const run = x => E.calculate({...base, ...x});
  const eq = (name, actual, expected, tolerance=0.01) => {
    if (Math.abs(actual-expected) > tolerance) throw new Error(`${name}: expected ${expected}, got ${actual}`);
  };
  const ok = (name, condition) => { if (!condition) throw new Error(name); };
  const results=[];
  const t=(name,fn)=>{try{fn();results.push({name,status:'PASS'});}catch(e){results.push({name,status:'FAIL',error:e.message});}};

  t('Personal Allowance shelters low employment income',()=>{
    const r=run({employmentIncome:12570});
    eq('tax due',r.taxDue,0);
    eq('taxable non-savings',r.taxableNonSavings,0);
  });

  t('Starting rate for savings available at low non-savings income',()=>{
    const r=run({employmentIncome:16000,savingsInterest:200});
    eq('starting rate available',r.savingsStartAvailable,1570);
    eq('starting rate used',r.savingsStartUsed,200);
    eq('taxable savings',r.taxableSavings,0);
  });

  t('No starting rate once taxable non-savings reaches 5000',()=>{
    const r=run({employmentIncome:17570,savingsInterest:100});
    eq('starting rate available',r.savingsStartAvailable,0);
  });

  t('ISA income is excluded',()=>{
    const a=run({employmentIncome:32000,savingsInterest:800,isaIncome:5000});
    const b=run({employmentIncome:32000,savingsInterest:800,isaIncome:0});
    eq('tax due unchanged by ISA',a.taxDue,b.taxDue);
    eq('ISA audit value',a.isaIncomeExcluded,5000);
  });

  t('Personal Allowance taper begins over 100000 ANI',()=>{
    const r=run({employmentIncome:110000,adjustedNetIncome:110000});
    eq('tapered PA',r.personalAllowance,7570);
  });

  t('Personal Allowance reaches zero at 125140 ANI',()=>{
    const r=run({employmentIncome:125140,adjustedNetIncome:125140});
    eq('PA zero',r.personalAllowance,0);
  });

  t('Scottish non-savings calculation differs from England/NI',()=>{
    const e=run({employmentIncome:60000,jurisdiction:'England & Northern Ireland'});
    const s=run({employmentIncome:60000,jurisdiction:'Scotland'});
    ok('Scottish tax should differ',Math.abs(e.nonSavingsTax.tax-s.nonSavingsTax.tax)>1);
  });

  t('Savings PSA classification counts gross interest when identifying band',()=>{
    const r=run({employmentIncome:49500,savingsInterest:1000});
    ok('PSA should not exceed 500 where income plus interest places customer above UK basic-rate threshold',r.personalSavingsAllowance<=500);
  });

  t('Dividend allowance does not make dividend income disappear from audit',()=>{
    const r=run({employmentIncome:30000,dividends:500});
    eq('dividend allowance used',r.dividendAllowanceUsed,500);
    eq('taxable dividends',r.taxableDividends,0);
  });

  t('Close reconstruction yields Likely explanation only, not certainty',()=>{
    const first=run({employmentIncome:32000,savingsInterest:1800,taxAlreadyDeducted:3800});
    const r=run({employmentIncome:32000,savingsInterest:1800,taxAlreadyDeducted:3800,hmrcStatedUnderpayment:first.reconstructedUnderpayment});
    ok('confidence label',r.confidence==='Likely explanation');
  });

  t('Large mismatch yields Unable to reconcile',()=>{
    const r=run({employmentIncome:20000,taxAlreadyDeducted:1486,hmrcStatedUnderpayment:1500});
    ok('unable status',r.confidence==='Unable to reconcile');
  });

  t('IYA per-payday figure is explicitly indicative',()=>{
    const r=run({hmrcStatedUnderpayment:640,remainingPayPeriods:8});
    eq('indicative extra',r.iyaIllustration.indicativeExtraPerPayday,80);
    ok('warning present',/Illustrative only/i.test(r.iyaIllustration.warning));
  });

  window.PAYEForensicsRegressionResults=results;
  console.table(results);
  const failed=results.filter(x=>x.status==='FAIL');
  if (failed.length) console.error(`${failed.length} PAYE Forensics regression test(s) failed`,failed);
  else console.info(`All ${results.length} PAYE Forensics regression tests passed`);
})();
