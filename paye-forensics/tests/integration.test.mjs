import test from 'node:test';
import assert from 'node:assert/strict';
import { buildAllowanceCollisionCase } from '../allowance-collision-engine.js';
import { buildPensionerAllowanceSplit } from '../pensioner-allowance-split-v24.js';
import { compileTaxVisualStory } from '../tax-visual-engine-v27.js';
import { choosePayeJourney } from '../app-router-v29.js';

test('two 1257-family codes raise a collision signal', () => {
  const out = buildAllowanceCollisionCase({sources:[
    {id:'a',label:'Job 1',income:26000,taxCode:'1257L',active:true},
    {id:'b',label:'Job 2',income:9000,taxCode:'1257L',active:true}
  ]});
  assert.equal(out.status, 'CHECK_NOW');
  assert.ok(out.findings.some(f => f.id === 'possible-duplicate-full-allowance'));
});

test('1257L plus BR does not create duplicate full-allowance finding', () => {
  const out = buildAllowanceCollisionCase({sources:[
    {income:26000,taxCode:'1257L'},
    {income:9000,taxCode:'BR'}
  ]});
  assert.equal(out.findings.some(f => f.id === 'possible-duplicate-full-allowance'), false);
});

test('pension split never allocates more than its illustrative allowance pool', () => {
  const out = buildPensionerAllowanceSplit({
    personalAllowance:12570,
    statePension:6000,
    untaxedInterest:1500,
    savingsZeroRateCoverage:500,
    pensions:[
      {label:'Pension 1',annualIncome:3000,taxCode:'300L'},
      {label:'Pension 2',annualIncome:2500,taxCode:'250L'},
      {label:'Pension 3',annualIncome:2200,taxCode:'BR'}
    ]
  });
  assert.ok(out.totalAllocated <= out.illustrativeNetAllowancePool);
  assert.equal(out.allocations.length, 3);
});

test('presentation levels preserve figures and evidence state', () => {
  const data={incomeTotal:30000,personalAllowance:12570,taxDue:3400,taxDeducted:2600,underpayment:800,kCode:'K154',iyaAmount:640,allowanceCollision:true};
  const simple=compileTaxVisualStory(data,{languageLevel:'SIMPLE'});
  const normal=compileTaxVisualStory(data,{languageLevel:'NORMAL'});
  const adviser=compileTaxVisualStory(data,{languageLevel:'ADVISER'});
  const shape=s=>s.scenes.map(x=>({id:x.id,kind:x.kind,amount:x.amount ?? null,evidenceClass:x.evidenceClass}));
  assert.deepEqual(shape(simple), shape(normal));
  assert.deepEqual(shape(normal), shape(adviser));
});

test('router sends new starter to Guardian and pension cases to pension journey', () => {
  const starter=choosePayeJourney({startedNewJob:true,hasBeenPaid:false,activePayeSources:1});
  assert.match(starter.primaryJourney,/NEW_JOB/i);
  const pension=choosePayeJourney({privatePension:4000,statePension:7000,activePayeSources:3});
  assert.ok(/PENSION|MULTI/i.test(pension.primaryJourney));
});
