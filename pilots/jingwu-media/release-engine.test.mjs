import test from "node:test";
import assert from "node:assert/strict";
import {STATES,newRelease,advance,verifyLedger} from "./release-engine.mjs";
test("release cannot skip rights approval",()=>{
 const r=newRelease({id:"sicario-001",title:"Sicario Episode 1"});
 assert.throws(()=>advance(r,"QA_PASSED",{qa_evidence:"checked"}),/one stage/);
});
test("each approval step requires evidence",()=>{
 let r=newRelease({id:"sicario-001",title:"Sicario Episode 1"});
 assert.throws(()=>advance(r,"ASSETS_VERIFIED"),/Missing evidence/);
 const evidence={
 ASSETS_VERIFIED:{asset_sha256:"abc123",asset_uri:"private://sicario.mp4"},
 RIGHTS_APPROVED:{rights_evidence:"original character and audio licences approved"},
 QA_PASSED:{qa_evidence:"mobile playback tested"},
 LISTING_PREPARED:{listing_evidence:"draft listing reviewed"},
 APPROVED_FOR_RELEASE:{human_approval_evidence:"owner approval record"},
 PUBLISHED_VERIFIED:{verified_publication_url:"https://example.org/verified-release"},
 RECONCILED:{settlement_evidence:"verified settlement report"}
 };
 for(const state of STATES.slice(1)) r=advance(r,state,evidence[state]);
 assert.equal(r.state,"RECONCILED");
 assert.equal(r.history.length,STATES.length);
});
test("no published stage without URL",()=>{
 let r=newRelease({id:"x",title:"x"});
 for(const [state,evidence] of [
 ["ASSETS_VERIFIED",{asset_uri:"a",asset_sha256:"abc"}],
 ["RIGHTS_APPROVED",{rights_evidence:"yes"}],
 ["QA_PASSED",{qa_evidence:"yes"}],
 ["LISTING_PREPARED",{listing_evidence:"yes"}],
 ["APPROVED_FOR_RELEASE",{human_approval_evidence:"yes"}]
 ]) r=advance(r,state,evidence);
 assert.throws(()=>advance(r,"PUBLISHED_VERIFIED",{verified_publication_url:"http://unsafe.test"}),/HTTPS/);
});
test("settlement distinguishes actual paid status",()=>{
 assert.deepEqual(verifyLedger({gross:4.99,fees:0.59,tax:0.5}),{gross:4.99,fees:0.59,tax:0.5,net:3.9,currency:"GBP",paid:false});
 assert.throws(()=>verifyLedger({gross:1,fees:3}),/Invalid/);
});
