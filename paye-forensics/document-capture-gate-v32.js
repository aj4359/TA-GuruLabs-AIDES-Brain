// TA GuruLabs PAYE Forensics v32 - document capture candidate gate
// Copyright © TA GuruLabs. Confidential implementation concept.
// Extraction output is NEVER treated as tax fact until customer confirms it.

const norm = v => String(v ?? '').trim();
const money = v => {
  const cleaned = String(v ?? '').replace(/[£,\s]/g,'');
  const parsed = Number(cleaned);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
};
const code = v => norm(v).toUpperCase().replace(/\s+/g,'');

export function createCaptureCandidate({
  id,
  documentType='unknown',
  documentLabel='Uploaded document',
  capturedAt=null,
  extractionProvider='candidate-extractor',
  fields={}
}={}) {
  const raw = {
    label: norm(fields.label),
    type: norm(fields.type),
    annualIncome: money(fields.annualIncome),
    taxCode: code(fields.taxCode),
    taxDeducted: money(fields.taxDeducted),
    sourceDate: norm(fields.sourceDate) || null
  };
  return {
    id: id || `capture-${Date.now()}`,
    documentType,
    documentLabel,
    capturedAt,
    extractionProvider,
    status:'CANDIDATE',
    evidenceClass:'UNCONFIRMED',
    fields:raw,
    customerEdits:{},
    audit:[{event:'CANDIDATE_CREATED',at:capturedAt || null}],
    warning:'We found possible values in your document. Check every value before it is used in your tax calculation.'
  };
}

export function editCaptureCandidate(candidate, edits={}) {
  if (!candidate || candidate.status === 'REJECTED') return candidate;
  const next = structuredClone(candidate);
  const cleanEdits = {};
  if ('label' in edits) cleanEdits.label = norm(edits.label);
  if ('type' in edits) cleanEdits.type = norm(edits.type);
  if ('annualIncome' in edits) cleanEdits.annualIncome = money(edits.annualIncome);
  if ('taxCode' in edits) cleanEdits.taxCode = code(edits.taxCode);
  if ('taxDeducted' in edits) cleanEdits.taxDeducted = money(edits.taxDeducted);
  if ('sourceDate' in edits) cleanEdits.sourceDate = norm(edits.sourceDate) || null;
  next.customerEdits = {...next.customerEdits, ...cleanEdits};
  next.status = 'REVIEWED';
  next.audit.push({event:'CUSTOMER_EDITED',fields:Object.keys(cleanEdits)});
  return next;
}

export function confirmCaptureCandidate(candidate) {
  if (!candidate || candidate.status === 'REJECTED') return {ok:false,error:'Candidate cannot be confirmed.'};
  const f = {...candidate.fields, ...candidate.customerEdits};
  const missing = [];
  if (!f.label) missing.push('label');
  if (!['employment','private-pension','other'].includes(f.type)) missing.push('type');
  if (f.annualIncome === null) missing.push('annualIncome');
  if (!f.taxCode) missing.push('taxCode');
  if (f.taxDeducted === null) missing.push('taxDeducted');
  if (missing.length) return {ok:false,error:`Please confirm: ${missing.join(', ')}.`};

  const promoted = {
    id:candidate.id,
    label:f.label,
    type:f.type,
    annualIncome:f.annualIncome,
    taxCode:f.taxCode,
    taxDeducted:f.taxDeducted,
    active:true,
    confirmed:true,
    evidenceType:candidate.documentType,
    evidenceLabel:`Customer confirmed from ${candidate.documentLabel}`,
    sourceDate:f.sourceDate || null,
    provenance:{
      documentType:candidate.documentType,
      documentLabel:candidate.documentLabel,
      extractionProvider:candidate.extractionProvider,
      promotedFrom:'UNCONFIRMED',
      promotedTo:'OBSERVED'
    }
  };
  return {ok:true,source:promoted,audit:[...candidate.audit,{event:'CUSTOMER_CONFIRMED',evidenceClass:'OBSERVED'}]};
}

export function rejectCaptureCandidate(candidate, reason='Customer rejected extracted values') {
  if (!candidate) return candidate;
  const next = structuredClone(candidate);
  next.status='REJECTED';
  next.evidenceClass='REJECTED';
  next.audit.push({event:'CUSTOMER_REJECTED',reason});
  return next;
}
