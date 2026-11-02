// Jingwu Media pilot — zero-dependency release workflow. No external publishing.
export const STATES = Object.freeze(["DRAFT","ASSETS_VERIFIED","RIGHTS_APPROVED","QA_PASSED","LISTING_PREPARED","APPROVED_FOR_RELEASE","PUBLISHED_VERIFIED","RECONCILED"]);
export const REQUIREMENTS = Object.freeze({
  ASSETS_VERIFIED:["asset_sha256","asset_uri"],
  RIGHTS_APPROVED:["rights_evidence"],
  QA_PASSED:["qa_evidence"],
  LISTING_PREPARED:["listing_evidence"],
  APPROVED_FOR_RELEASE:["human_approval_evidence"],
  PUBLISHED_VERIFIED:["verified_publication_url"],
  RECONCILED:["settlement_evidence"]
});
export function newRelease({id,title,kind="video_comic",price_gbp=2.99}){
  if(!id || !title) throw Error("Release ID and title required");
  if(!Number.isFinite(price_gbp)||price_gbp<0) throw Error("Invalid price");
  return {id,title,kind,price_gbp,state:"DRAFT",evidence:{},history:[{state:"DRAFT",at:new Date().toISOString()}]};
}
export function advance(release,next,evidence={}){
  if(!release || !STATES.includes(release.state)) throw Error("Invalid release");
  const idx=STATES.indexOf(release.state);
  if(STATES[idx+1]!==next) throw Error("Transitions must advance exactly one stage");
  const merged={...release.evidence,...evidence};
  for(const key of (REQUIREMENTS[next]||[])) if(typeof merged[key]!=="string"||!merged[key].trim()) throw Error("Missing evidence: "+key);
  if(next==="PUBLISHED_VERIFIED" && !/^https:\/\//.test(merged.verified_publication_url)) throw Error("Publication must use an HTTPS link");
  return {...release,evidence:merged,state:next,history:[...release.history,{state:next,at:new Date().toISOString()}]};
}
export function verifyLedger({gross,fees=0,tax=0,currency="GBP",paid=false}){
  if(![gross,fees,tax].every(n=>Number.isFinite(n)&&n>=0)||fees+tax>gross) throw Error("Invalid settlement amounts");
  return {gross,fees,tax,net:Math.round((gross-fees-tax)*100)/100,currency,paid:paid===true};
}
