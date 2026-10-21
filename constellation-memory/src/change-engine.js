import { validateRecord } from "./memory-store.js";

const ACTIVE = new Set(["NEW", "CURRENT", "CONFIRMED", "APPROVED", "EXPERIMENTAL"]);

export function classifyFinding(previous, finding) {
  if (!previous) return "NEW";

  const sameStatement = normalise(previous.statement) === normalise(finding.statement);
  const evidenceConflict = finding.evidence?.some((item) => item.supports === false);
  if (evidenceConflict) return "CONTRADICTED";
  if (sameStatement) return "CONFIRMED";
  return "CHANGED";
}

export function applyMaterialityRules(finding, rules = []) {
  const matchingRules = rules.filter((rule) => rule.active && (!rule.domain || rule.domain === finding.domain));
  const threshold = matchingRules.reduce((current, rule) =>
    rule.kind === "minimum-materiality" ? Math.max(current, rule.value) : current, 0.5);
  const ignoredSubjects = matchingRules
    .filter((rule) => rule.kind === "ignore-subject")
    .map((rule) => normalise(rule.value));

  const score = finding.materiality ?? 0;
  return {
    material: score >= threshold && !ignoredSubjects.includes(normalise(finding.subject)),
    score,
    threshold,
    appliedRuleIds: matchingRules.map(({ id }) => id)
  };
}

export async function ingestFinding(store, finding) {
  const state = await store.load();
  if (state.records.some(({ id }) => id === finding.id)) throw new Error(`Duplicate record id: ${finding.id}`);
  const previous = state.records
    .filter((record) => record.domain === finding.domain && record.subject === finding.subject && ACTIVE.has(record.status))
    .sort((a, b) => Date.parse(b.observedAt) - Date.parse(a.observedAt))[0] ?? null;
  const delta = classifyFinding(previous, finding);
  const materiality = applyMaterialityRules(finding, state.rules);

  if (!materiality.material) return { accepted: false, delta, materiality, previous };

  const record = { ...finding, status: delta === "CHANGED" ? "CURRENT" : delta };
  if (delta === "CHANGED") record.supersedes = [...new Set([...(record.supersedes ?? []), previous.id])];
  validateRecord(record);

  await store.transact((draft) => {
    if (previous && delta === "CHANGED") {
      const old = draft.records.find(({ id }) => id === previous.id);
      old.status = "SUPERSEDED";
      old.validUntil = finding.observedAt;
    }
    draft.records.push(record);
  });
  return { accepted: true, delta, materiality, previous, record };
}

function normalise(value) {
  return String(value ?? "").trim().toLowerCase().replace(/\s+/g, " ");
}
