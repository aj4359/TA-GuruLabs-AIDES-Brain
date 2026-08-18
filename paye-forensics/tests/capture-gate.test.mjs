import test from 'node:test';
import assert from 'node:assert/strict';
import {
  createCaptureCandidate,
  editCaptureCandidate,
  confirmCaptureCandidate,
  rejectCaptureCandidate
} from '../document-capture-gate-v32.js';
import { buildConfirmedSourceSet } from '../multi-source-capture-v31.js';

test('unconfirmed extraction is excluded from deterministic source totals', () => {
  const candidate = createCaptureCandidate({
    id:'job-1', documentType:'payslip', documentLabel:'May payslip',
    fields:{label:'Job 1', type:'employment', annualIncome:'£26,000', taxCode:'1257L', taxDeducted:'2600'}
  });
  const set = buildConfirmedSourceSet({sources:[{...candidate.fields,id:candidate.id,confirmed:false}]});
  assert.equal(set.confirmed.length, 0);
  assert.equal(set.totals.employmentIncome, 0);
  assert.equal(set.totals.taxAlreadyDeducted, 0);
});

test('confirmed extracted source is promoted with provenance', () => {
  const candidate = createCaptureCandidate({
    id:'pension-1', documentType:'payslip', documentLabel:'Pension payslip',
    fields:{label:'Pension 1', type:'private-pension', annualIncome:'4200', taxCode:'300L', taxDeducted:'120'}
  });
  const result = confirmCaptureCandidate(candidate);
  assert.equal(result.ok, true);
  assert.equal(result.source.confirmed, true);
  assert.equal(result.source.provenance.promotedFrom, 'UNCONFIRMED');
  assert.equal(result.source.provenance.promotedTo, 'OBSERVED');
  const set = buildConfirmedSourceSet({sources:[result.source]});
  assert.equal(set.totals.privatePension, 4200);
  assert.equal(set.totals.taxAlreadyDeducted, 120);
});

test('partial extraction cannot silently promote', () => {
  const candidate = createCaptureCandidate({fields:{label:'Job 2', type:'employment', annualIncome:'9000'}});
  const result = confirmCaptureCandidate(candidate);
  assert.equal(result.ok, false);
  assert.match(result.error, /taxCode/);
});

test('customer edits still require explicit confirmation', () => {
  let candidate = createCaptureCandidate({fields:{label:'Job 2', type:'employment', annualIncome:'9000'}});
  candidate = editCaptureCandidate(candidate,{taxCode:'BR',taxDeducted:'900'});
  assert.equal(candidate.status, 'REVIEWED');
  const result = confirmCaptureCandidate(candidate);
  assert.equal(result.ok, true);
  assert.equal(result.source.taxCode, 'BR');
});

test('rejected candidate cannot promote', () => {
  const candidate = rejectCaptureCandidate(createCaptureCandidate({
    fields:{label:'Job 1', type:'employment', annualIncome:'26000', taxCode:'1257L', taxDeducted:'2600'}
  }));
  assert.equal(confirmCaptureCandidate(candidate).ok, false);
});
