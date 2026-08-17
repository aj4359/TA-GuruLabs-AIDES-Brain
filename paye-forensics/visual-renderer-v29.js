// TA GuruLabs PAYE Forensics v29 - lightweight animated SVG renderer
// Public renderer consumes compiled scenes only; it does not contain private ranking heuristics.

const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const money=n=>`£${Number(n||0).toLocaleString('en-GB',{minimumFractionDigits:2,maximumFractionDigits:2})}`;

export function renderSceneSvg(scene={}) {
  const kind=String(scene.kind||'').toUpperCase();
  const amount=Number(scene.amount||0);
  const common=`<text x="24" y="32" font-size="15" fill="currentColor">${esc(scene.title||kind)}</text>`;
  if(kind==='ALLOWANCE_BUCKET') return `<svg viewBox="0 0 520 170" role="img" aria-label="${esc(scene.title)}">${common}<rect x="24" y="55" width="472" height="72" rx="18" fill="none" stroke="currentColor" opacity=".35"/><rect x="24" y="55" width="472" height="72" rx="18" fill="currentColor" opacity=".14"><animate attributeName="width" from="0" to="472" dur=".8s" fill="freeze"/></rect><text x="260" y="101" text-anchor="middle" font-size="28" fill="currentColor">${money(amount)}</text></svg>`;
  if(kind==='TAX_BANDS') return `<svg viewBox="0 0 520 170" role="img">${common}<rect x="24" y="60" width="150" height="55" rx="10" fill="currentColor" opacity=".10"/><rect x="184" y="60" width="150" height="55" rx="10" fill="currentColor" opacity=".18"/><rect x="344" y="60" width="152" height="55" rx="10" fill="currentColor" opacity=".26"/><text x="260" y="148" text-anchor="middle" fill="currentColor">Tax in this reconstruction: ${money(amount)}</text></svg>`;
  if(kind==='K_CODE_FLIP') return `<svg viewBox="0 0 520 180" role="img">${common}<g transform="translate(260 105)"><rect x="-95" y="-42" width="190" height="84" rx="18" fill="currentColor" opacity=".14"><animateTransform attributeName="transform" type="rotate" from="0" to="180" dur=".9s" fill="freeze"/></rect><text x="0" y="8" text-anchor="middle" font-size="38" fill="currentColor">K</text></g><text x="260" y="166" text-anchor="middle" fill="currentColor">Allowance used up → collection state</text></svg>`;
  if(kind==='CATCH_UP') return `<svg viewBox="0 0 520 180" role="img">${common}<line x1="42" y1="100" x2="478" y2="100" stroke="currentColor" opacity=".3" stroke-width="8"/><circle cx="42" cy="100" r="16" fill="currentColor"><animate attributeName="cx" from="42" to="478" dur="1.4s" fill="freeze"/></circle><text x="260" y="150" text-anchor="middle" fill="currentColor">IYA ${money(amount)} being collected through later pay periods</text></svg>`;
  if(kind==='ALLOWANCE_COLLISION') return `<svg viewBox="0 0 520 190" role="img">${common}<circle cx="175" cy="105" r="55" fill="currentColor" opacity=".13"/><circle cx="345" cy="105" r="55" fill="currentColor" opacity=".13"/><text x="175" y="112" text-anchor="middle" font-size="24" fill="currentColor">1257L</text><text x="345" y="112" text-anchor="middle" font-size="24" fill="currentColor">1257L</text><path d="M230 105 L290 105" stroke="currentColor" stroke-width="4" stroke-dasharray="7 7"><animate attributeName="stroke-dashoffset" from="28" to="0" dur="1s" repeatCount="indefinite"/></path><text x="260" y="178" text-anchor="middle" fill="currentColor">Possible duplicate allowance signal</text></svg>`;
  return `<svg viewBox="0 0 520 150" role="img">${common}<text x="24" y="82" font-size="34" fill="currentColor">${amount?money(amount):esc(scene.text||'')}</text></svg>`;
}

export function renderStoryHtml(compiled={}) {
  return (compiled.scenes||[]).map((s,i)=>`<article class="tax-scene" data-kind="${esc(s.kind)}" data-evidence="${esc(s.evidenceClass)}"><div class="scene-no">${i+1}</div>${renderSceneSvg(s)}<p>${esc(s.text||'')}</p><small>${esc(s.evidenceClass||'')}</small></article>`).join('');
}
