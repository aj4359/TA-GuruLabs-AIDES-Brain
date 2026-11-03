// Pure adapter for Payhip paid/refunded webhook payloads.
// Caller MUST authenticate event signature server-side before using this adapter.
// Payhip signature is SHA256(API key), so it proves key knowledge but is not a per-payload MAC.
// Protect against replay with durable idempotency and reconciliation.
export function normalizePayhipEvent(event) {
 if (!event || typeof event !== "object" || !["paid","refunded"].includes(event.type)) throw Error("Unsupported event");
 if (typeof event.id !== "string" || !event.id.trim() || typeof event.currency !== "string" || !/^[A-Z]{3}$/.test(event.currency)) throw Error("Missing transaction or currency");
 for (const key of ["price","stripe_fee","payhip_fee"]) if (!Number.isSafeInteger(event[key]) || event[key] < 0) throw Error("Invalid money field "+key);
 if (!Array.isArray(event.items) || event.items.length === 0) throw Error("Missing line items");
 const refund = event.type === "refunded" ? event.amount_refunded : 0;
 if (!Number.isSafeInteger(refund)||refund<0||refund>event.price) throw Error("Invalid refund");
 const platformFees = event.stripe_fee + event.payhip_fee;
 return {
   event_key: event.id+":"+event.type+":"+(event.type==="refunded"?(event.date_refunded??"unknown")+":"+refund:"0"),
   transaction_id:event.id,type:event.type,currency:event.currency,
   gross_minor:event.price,platform_fees_minor:platformFees,refunded_minor:refund,
   reported_net_before_tax_minor:event.price-platformFees-refund,
   items:event.items.map(x=>({product_id:String(x.product_id??""),product_key:String(x.product_key??""),quantity:Number(x.quantity)||1})),
   status:"UNRECONCILED",
   // Do not replicate buyer email, IP, payment method or licence key into general analytics.
 };
}
export function applyEvent(ledger, normalized) {
 const events = Array.isArray(ledger)?ledger:[];
 if(events.some(x=>x.event_key===normalized.event_key)) return events;
 return [...events,normalized];
}
