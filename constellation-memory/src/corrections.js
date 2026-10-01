export async function recordCorrection(store, correction) {
  const required = ["id", "targetId", "reason", "observedAt"];
  for (const key of required) if (!correction[key]) throw new Error(`Correction requires ${key}`);

  return store.transact((state) => {
    if (state.records.some(({ id }) => id === correction.id)) throw new Error(`Duplicate record id: ${correction.id}`);
    const target = state.records.find(({ id }) => id === correction.targetId);
    if (!target) throw new Error(`Correction target not found: ${correction.targetId}`);

    target.status = "REJECTED";
    const rule = correction.rule ? {
      id: correction.rule.id,
      kind: correction.rule.kind,
      value: correction.rule.value,
      domain: correction.rule.domain ?? target.domain,
      active: true,
      learnedFrom: correction.id,
      createdAt: correction.observedAt
    } : null;
    if (rule) {
      const existing = state.rules.findIndex(({ id }) => id === rule.id);
      if (existing >= 0) state.rules[existing] = rule;
      else state.rules.push(rule);
    }

    const record = {
      id: correction.id,
      type: "correction",
      subject: target.subject,
      statement: correction.reason,
      domain: target.domain,
      product: target.product ?? null,
      status: "APPROVED",
      confidence: 1,
      observedAt: correction.observedAt,
      evidence: [{ source: `human-correction:${correction.actor ?? "Anthony"}`, checkedAt: correction.observedAt, supports: true }],
      permissions: target.permissions,
      affectedDecisions: target.affectedDecisions ?? [],
      links: { interpretationId: target.id }
    };
    state.records.push(record);
    return { record, rule };
  });
}
