// TA GuruLabs PAYE Forensics v27 - Tax Visual Engine orchestration layer
// Copyright © TA GuruLabs. Confidential implementation concept.
// Public clients should consume structured scene output, not proprietary ranking/orchestration internals.

const norm = v => String(v || '').trim();
const money = v => Math.round(Number(v || 0) * 100) / 100;

const LANGUAGE_LEVELS = new Set(['SIMPLE','NORMAL','ADVISER']);

function labelEvidence(value) {
  const v = String(value || 'INFERRED').toUpperCase();
  return ['OBSERVED','INFERRED','ILLUSTRATIVE'].includes(v) ? v : 'INFERRED';
}

function explainScene(scene, level) {
  const evidenceClass = labelEvidence(scene.evidenceClass);
  const base = { ...scene, evidenceClass };

  if (level === 'ADVISER') return {
    ...base,
    title: scene.adviserTitle || scene.title,
    text: scene.adviserText || scene.normalText || scene.simpleText || scene.text,
    showRuleIds: true,
    showSourceIds: true,
    showAssumptions: true
  };

  if (level === 'SIMPLE') return {
    ...base,
    title: scene.simpleTitle || scene.title,
    text: scene.simpleText || scene.normalText || scene.text,
    showRuleIds: false,
    showSourceIds: false,
    showAssumptions: false
  };

  return {
    ...base,
    title: scene.normalTitle || scene.title,
    text: scene.normalText || scene.text || scene.simpleText,
    showRuleIds: false,
    showSourceIds: true,
    showAssumptions: false
  };
}

function buildCoreScenes(caseData = {}) {
  const scenes = [];
  if (caseData.incomeTotal != null) scenes.push({
    id:'INCOME', kind:'MONEY_IN', evidenceClass:'OBSERVED', amount:money(caseData.incomeTotal),
    simpleTitle:'Money comes in', simpleText:`You have about £${money(caseData.incomeTotal).toFixed(2)} of income in this picture.`,
    normalTitle:'Income', normalText:`Confirmed income used in this reconstruction: £${money(caseData.incomeTotal).toFixed(2)}.`,
    adviserTitle:'Observed income base', adviserText:'Income entered or confirmed from source documents is the starting fact set for the tax calculation.'
  });

  if (caseData.personalAllowance != null) scenes.push({
    id:'PA', kind:'ALLOWANCE_BUCKET', evidenceClass:'INFERRED', amount:money(caseData.personalAllowance),
    simpleTitle:'Your tax-free bucket', simpleText:`Up to £${money(caseData.personalAllowance).toFixed(2)} can sit in your tax-free bucket, subject to your circumstances.`,
    normalTitle:'Personal Allowance', normalText:`Personal Allowance used in this reconstruction: £${money(caseData.personalAllowance).toFixed(2)}.`,
    adviserTitle:'Personal Allowance applied', adviserText:'Allowance is derived from the applicable tax-year rules and any entered adjusted-net-income facts.',
    ruleIds:caseData.paRuleIds||[], sourceIds:caseData.paSourceIds||[]
  });

  if (caseData.taxDue != null) scenes.push({
    id:'TAX_DUE', kind:'TAX_BANDS', evidenceClass:'INFERRED', amount:money(caseData.taxDue),
    simpleTitle:'The tax calculation', simpleText:`After the tax-free parts and tax bands are applied, this picture gives about £${money(caseData.taxDue).toFixed(2)} of tax.`,
    normalTitle:'Reconstructed tax due', normalText:`The deterministic reconstruction gives £${money(caseData.taxDue).toFixed(2)} of tax due on the supplied facts.`,
    adviserTitle:'Deterministic liability output', adviserText:'Tax due is calculated from the tax-year rule set, allowance allocation and applicable rate-band slices.',
    ruleIds:caseData.taxRuleIds||[], sourceIds:caseData.taxSourceIds||[]
  });

  if (caseData.taxDeducted != null) scenes.push({
    id:'DEDUCTED', kind:'PAYROLL_TAKEN', evidenceClass:'OBSERVED', amount:money(caseData.taxDeducted),
    simpleTitle:'Tax already taken', simpleText:`Payroll has already taken £${money(caseData.taxDeducted).toFixed(2)}.`,
    normalTitle:'Tax already deducted', normalText:`Confirmed tax deducted: £${money(caseData.taxDeducted).toFixed(2)}.`,
    adviserTitle:'Observed PAYE deducted', adviserText:'This figure should come from confirmed payslip/P60/P45 or HMRC-held evidence.'
  });

  const diff = caseData.underpayment != null ? money(caseData.underpayment) : null;
  if (diff != null) scenes.push({
    id:'UNDERPAYMENT', kind:'MISSING_PIECE', evidenceClass:'INFERRED', amount:diff,
    simpleTitle:'The missing bit', simpleText:`This leaves about £${diff.toFixed(2)} of tax still missing in our reconstruction.`,
    normalTitle:'Possible underpayment', normalText:`Reconstructed underpayment: £${diff.toFixed(2)}.`,
    adviserTitle:'Reconciliation residual', adviserText:'This is the deterministic difference between reconstructed liability and confirmed tax already deducted, before unresolved adjustments.'
  });

  return scenes;
}

function appendSpecialScenes(scenes, caseData = {}) {
  if (caseData.kCode) scenes.push({
    id:'K_CODE', kind:'K_CODE_FLIP', evidenceClass:'OBSERVED',
    simpleTitle:'Your bucket has flipped', simpleText:'Your tax-free bucket has been used up, so the K code tells payroll to collect tax using a negative allowance-style adjustment. It is not a fine.',
    normalTitle:`K code ${norm(caseData.kCode)}`, normalText:'A K code indicates coding deductions exceed coding allowances. Payroll uses the code as a collection mechanism.',
    adviserTitle:'K-code collection state', adviserText:'K-code interpretation should be tied to the P2 breakdown, overriding-limit rules and the observed code basis.',
    sourceIds:caseData.kCodeSourceIds||[]
  });

  if (Number(caseData.iyaAmount||0) > 0) scenes.push({
    id:'IYA', kind:'CATCH_UP', evidenceClass:'OBSERVED', amount:money(caseData.iyaAmount),
    simpleTitle:'HMRC is trying to catch up', simpleText:`HMRC says about £${money(caseData.iyaAmount).toFixed(2)} of extra tax needs collecting during this tax year.`,
    normalTitle:'In-Year Adjustment', normalText:`Observed IYA amount: £${money(caseData.iyaAmount).toFixed(2)}. This is separate from the tax code itself.`,
    adviserTitle:'IYA / IYAR state', adviserText:'The IYA is the extra in-year tax amount identified; the associated restriction affects collection through PAYE.',
    sourceIds:caseData.iyaSourceIds||[]
  });

  if (caseData.allowanceCollision) scenes.push({
    id:'ALLOWANCE_COLLISION', kind:'ALLOWANCE_COLLISION', evidenceClass:'INFERRED',
    simpleTitle:'Your tax-free bucket may be showing twice', simpleText:'Two active jobs or pensions appear to be using a full allowance-style code. That can mean too little tax is taken during the year.',
    normalTitle:'Possible Personal Allowance collision', normalText:'More than one active PAYE source appears to carry a full-allowance code. This is a diagnostic signal, not proof of coding error.',
    adviserTitle:'Multi-source coded-allowance collision signal', adviserText:'Compare confirmed current codes and P2 breakdowns across all active PAYE sources before concluding fault.'
  });

  return scenes;
}

export function compileTaxVisualStory(caseData = {}, options = {}) {
  const languageLevel = String(options.languageLevel || 'NORMAL').toUpperCase();
  if (!LANGUAGE_LEVELS.has(languageLevel)) throw new Error('languageLevel must be SIMPLE, NORMAL or ADVISER');

  const scenes = appendSpecialScenes(buildCoreScenes(caseData), caseData)
    .concat(Array.isArray(caseData.extraScenes) ? caseData.extraScenes : [])
    .map(scene => explainScene(scene, languageLevel));

  return {
    engine:'TA-GuruLabs-Tax-Visual-Engine',
    version:'27',
    languageLevel,
    scenes,
    presentationOnly:true,
    evidenceModel:'OBSERVED_INFERRED_ILLUSTRATIVE',
    guardrails:[
      'Presentation level never changes the deterministic tax result.',
      'Simple wording never upgrades an inference into an observed fact.',
      'Customer-facing clients should not receive proprietary scenario-ranking weights or compiler heuristics.',
      'Tax codes are interpreted, not issued.'
    ]
  };
}
