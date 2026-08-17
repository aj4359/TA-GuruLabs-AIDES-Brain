// TA GuruLabs PAYE Forensics v28 - Unified Tax Visual Adapter
// Copyright © TA GuruLabs. Confidential implementation concept.
// Connects deterministic PAYE outputs and specialist diagnostic modules to the Tax Visual Engine.

import { compileTaxVisualStory } from './tax-visual-engine-v27.js';
import { buildPensionerAllowanceSplit } from './pensioner-allowance-split-v24.js';
import { buildKCodeIYAStory } from './kcode-iya-underpayment-v25.js';
import { buildAllowanceCollisionCase } from './allowance-collision-engine.js';

const n = v => Math.max(0, Number(v || 0));
const round2 = v => Math.round((Number(v || 0) + Number.EPSILON) * 100) / 100;

function requireDeterministicEngine() {
  if (!window.PAYEForensicsV2 || typeof window.PAYEForensicsV2.calculate !== 'function') {
    throw new Error('PAYEForensicsV2 deterministic engine is not loaded. Load rules-2026-27.js and engine-v2.js first.');
  }
  return window.PAYEForensicsV2;
}

function taxRuleIds(result) {
  return [
    ...(result.nonSavingsTax?.rows || []).map(r => r.ruleId),
    ...(result.savingsTax?.rows || []).map(r => r.ruleId),
    ...(result.dividendTax?.rows || []).map(r => r.ruleId)
  ].filter(Boolean);
}

function specialistScenes({ pensioner, kIya, collision }) {
  const scenes = [];

  if (pensioner) {
    scenes.push({
      id:'PENSIONER_ALLOWANCE_SPLIT', kind:'ALLOWANCE_FLOW', evidenceClass:'ILLUSTRATIVE',
      simpleTitle:'One tax-free bucket, several pensions',
      simpleText:`After State Pension and savings are considered, about £${pensioner.illustrativeNetAllowancePool.toFixed(2)} is left in this picture to spread across the pension sources.`,
      normalTitle:'Illustrative pension allowance split',
      normalText:`The explanatory model leaves £${pensioner.illustrativeNetAllowancePool.toFixed(2)} of allowance capacity for ${pensioner.allocations.length} private/occupational pension source(s).`,
      adviserTitle:'Pension-source allowance allocation model',
      adviserText:'Illustrative allocation only. Compare observed P2 code breakdowns and actual HMRC allocation before drawing conclusions.',
      assumptions:[pensioner.guardrail]
    });
    pensioner.allocations.forEach((a, i) => scenes.push({
      id:`PENSION_${i+1}`, kind:'SOURCE_ALLOCATION', evidenceClass:a.observed ? 'OBSERVED' : 'ILLUSTRATIVE',
      simpleTitle:a.label,
      simpleText:`Income £${round2(a.annualIncome).toFixed(2)}. About £${round2(a.illustrativeAllowanceAllocated).toFixed(2)} of the bucket is shown working here.`,
      normalTitle:`${a.label} allowance map`,
      normalText:`Income £${round2(a.annualIncome).toFixed(2)}; illustrated allowance £${round2(a.illustrativeAllowanceAllocated).toFixed(2)}; illustrated taxable remainder £${round2(a.illustrativeTaxableRemainder).toFixed(2)}.`,
      adviserTitle:`${a.label} allocation trace`,
      adviserText:`Observed code ${a.taxCode || 'not supplied'}; model role ${a.allocationRole}.`
    }));
  }

  if (kIya) {
    (kIya.scenes || []).forEach((s, i) => scenes.push({
      id:`KIYA_${i+1}`, kind:s.id === 'KCODE' ? 'K_CODE_FLIP' : s.id === 'IYA' ? 'CATCH_UP' : 'EXPLAINER',
      evidenceClass:s.evidenceClass || 'INFERRED',
      simpleTitle:s.title,
      simpleText:s.detail || s.guardrail || '',
      normalTitle:s.title,
      normalText:s.detail || '',
      adviserTitle:s.title,
      adviserText:[s.detail, s.guardrail].filter(Boolean).join(' ')
    }));
  }

  if (collision?.findings?.length) {
    collision.findings.forEach((f, i) => scenes.push({
      id:`COLLISION_${i+1}`, kind:'ALLOWANCE_COLLISION', evidenceClass:f.evidenceClass || 'INFERRED',
      simpleTitle:'Your tax-free bucket may be showing twice',
      simpleText:f.explanation,
      normalTitle:f.title,
      normalText:f.explanation,
      adviserTitle:f.title,
      adviserText:`${f.explanation} Next action: ${f.nextAction}`
    }));
  }

  return scenes;
}

export function buildUnifiedTaxVisualCase(input = {}, options = {}) {
  const calc = requireDeterministicEngine().calculate(input);

  const pensioner = options.includePensionerSplit ? buildPensionerAllowanceSplit({
    personalAllowance: calc.personalAllowance,
    pensions: options.pensions || [],
    statePension: n(input.statePension),
    untaxedInterest: n(input.savingsInterest),
    savingsZeroRateCoverage: round2(calc.savingsStartUsed + calc.personalSavingsAllowanceUsed)
  }) : null;

  const kIya = (options.taxCode || input.newTaxCode || input.taxCode || options.iyaAmount) ? buildKCodeIYAStory({
    taxCode: options.taxCode || input.newTaxCode || input.taxCode,
    previousCode: input.oldTaxCode,
    iyaAmount: n(options.iyaAmount),
    previousYearUnderpayment: n(options.previousYearUnderpayment),
    statePension: n(input.statePension),
    taxableBenefits: n(input.benefitsInKind),
    taxableInterestEstimate: n(input.savingsInterest),
    remainingPayPeriods: n(input.remainingPayPeriods)
  }) : null;

  const collision = Array.isArray(options.activeSources) && options.activeSources.length
    ? buildAllowanceCollisionCase({ sources: options.activeSources, personalAllowance: calc.personalAllowance })
    : null;

  const caseData = {
    incomeTotal: round2(calc.nonSavingsGross + calc.savingsGross + calc.dividendsGross),
    personalAllowance: calc.personalAllowance,
    taxDue: calc.taxDue,
    taxDeducted: calc.taxAlreadyDeducted,
    underpayment: calc.reconstructedUnderpayment,
    paRuleIds:['PERSONAL_ALLOWANCE_2026_27'],
    taxRuleIds:taxRuleIds(calc),
    kCode:kIya?.kCode?.code || null,
    iyaAmount:kIya?.iyaAmount || 0,
    allowanceCollision:Boolean(collision?.findings?.length),
    extraScenes:specialistScenes({pensioner,kIya,collision})
  };

  const story = compileTaxVisualStory(caseData, { languageLevel: options.languageLevel || 'NORMAL' });

  return {
    version:'28',
    taxYear:calc.taxYear,
    deterministicResult:calc,
    pensionerSplit:pensioner,
    kCodeIya:kIya,
    allowanceCollision:collision,
    visualStory:story,
    reconciliation:{
      hmrcStatedUnderpayment:calc.hmrcStatedUnderpayment,
      reconstructedUnderpayment:calc.reconstructedUnderpayment,
      difference:calc.difference,
      confidence:calc.confidence
    },
    guardrails:[
      'The deterministic PAYE result is calculated once and reused across all presentation levels.',
      'Specialist pension/K-code/IYA/collision scenes remain explanatory or diagnostic unless backed by observed evidence.',
      'Visual presentation does not issue a tax code, reproduce HMRC NPS, or establish fault.'
    ]
  };
}
