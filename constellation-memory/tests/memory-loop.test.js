import assert from "node:assert/strict";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { JsonMemoryStore, ingestFinding, recordCorrection } from "../src/index.js";

const at = (day) => `2026-09-${String(day).padStart(2, "0")}T07:00:00.000Z`;

function finding(id, statement, day, materiality = 0.8) {
  return {
    id,
    type: "fact",
    subject: "Competitor Pro price",
    statement,
    domain: "competitive-intelligence",
    product: "AIDES OS",
    confidence: 0.95,
    observedAt: at(day),
    materiality,
    evidence: [{ source: "https://competitor.example/pricing", checkedAt: at(day), supports: true }],
    permissions: { scope: "research", allowedActors: ["Scout", "Aureus"] }
  };
}

async function setup() {
  const directory = await mkdtemp(join(tmpdir(), "constellation-memory-"));
  return { store: new JsonMemoryStore(join(directory, "memory.json")), directory };
}

test("changed facts supersede history without deleting it", async () => {
  const { store } = await setup();
  assert.equal((await ingestFinding(store, finding("price-1", "Pro costs £29", 1))).delta, "NEW");
  const changed = await ingestFinding(store, finding("price-2", "Pro costs £39", 2));
  assert.equal(changed.delta, "CHANGED");
  assert.deepEqual(changed.record.supersedes, ["price-1"]);

  const current = await store.current("competitive-intelligence", "Competitor Pro price");
  assert.equal(current.id, "price-2");
  const history = await store.records({ domain: "competitive-intelligence", includeHistorical: true });
  assert.equal(history.find(({ id }) => id === "price-1").status, "SUPERSEDED");
  assert.equal(history.find(({ id }) => id === "price-1").validUntil, at(2));
});

test("a human correction changes the next run", async () => {
  const { store } = await setup();
  await ingestFinding(store, finding("noise-1", "Pro costs £29", 1, 0.6));
  await recordCorrection(store, {
    id: "correction-1",
    targetId: "noise-1",
    reason: "Only alert Scout when materiality is at least 0.75.",
    actor: "Anthony",
    observedAt: at(2),
    rule: { id: "rule-minimum-materiality", kind: "minimum-materiality", value: 0.75 }
  });

  const nextRun = await ingestFinding(store, finding("noise-2", "Pro costs £31", 3, 0.7));
  assert.equal(nextRun.accepted, false);
  assert.equal(nextRun.materiality.threshold, 0.75);
  assert.deepEqual(nextRun.materiality.appliedRuleIds, ["rule-minimum-materiality"]);
});

test("persistence survives a new store instance", async () => {
  const { store, directory } = await setup();
  await ingestFinding(store, finding("persisted-1", "Pro costs £29", 1));
  const reloaded = new JsonMemoryStore(join(directory, "memory.json"));
  assert.equal((await reloaded.current("competitive-intelligence", "Competitor Pro price")).id, "persisted-1");
  assert.doesNotReject(() => readFile(join(directory, "memory.json"), "utf8"));
});

test("duplicate evidence cannot silently overwrite memory", async () => {
  const { store } = await setup();
  await ingestFinding(store, finding("unique-1", "Pro costs £29", 1));
  await assert.rejects(
    () => ingestFinding(store, finding("unique-1", "Pro costs £39", 2)),
    /Duplicate record id/
  );
});
