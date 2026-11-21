import test from "node:test";
import assert from "node:assert/strict";
import {normalizePayhipEvent,applyEvent} from "./payhip-events.mjs";
const sample={id:"ORDER-1",email:"someone@example.com",ip_address:"127.0.0.1",currency:"GBP",price:499,stripe_fee:25,payhip_fee:25,items:[{product_id:"a",product_key:"q",quantity:"1",license_key:"secret"}],type:"paid"};
test("normalises amounts in minor units, excludes personal data and cannot imply payout",()=>{
 const x=normalizePayhipEvent(sample);
 assert.equal(x.reported_net_before_tax_minor,449);
 assert.equal(x.status,"UNRECONCILED");
 assert.equal(JSON.stringify(x).includes("someone@example.com"),false);
 assert.equal(JSON.stringify(x).includes("secret"),false);
});
test("deduplicates retries and handles partial refunds",()=>{
 const first=normalizePayhipEvent(sample);
 const refund=normalizePayhipEvent({...sample,type:"refunded",amount_refunded:199,date_refunded:1740000000});
 const rows=applyEvent(applyEvent(applyEvent([],first),first),refund);
 assert.equal(rows.length,2);
 assert.equal(refund.refunded_minor,199);
 assert.equal(refund.reported_net_before_tax_minor,250);
});
test("rejects malformed and unsupported events",()=>{
 assert.throws(()=>normalizePayhipEvent({...sample,type:"subscription.created"}),/Unsupported/);
 assert.throws(()=>normalizePayhipEvent({...sample,price:-1}),/Invalid/);
 assert.throws(()=>normalizePayhipEvent({...sample,type:"refunded",amount_refunded:999}),/Invalid/);
});
