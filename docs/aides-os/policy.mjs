/**
 * Pure policy prototype. Do NOT rely on this function as the only production gate.
 * Apply authorization/approval checks at the actual execution boundary.
 */
export const LOW_RISK = Object.freeze([
  "read_approved_source",
  "draft_internal_report",
  "propose_action"
]);
export const HIGH_IMPACT = Object.freeze([
  "send_external_message",
  "publish_external_content",
  "pay",
  "change_permissions",
  "delete_data",
  "disclose_sensitive_data",
  "write_production"
]);
export function assessAction(task, action, usage = {}) {
  if (!task || !action || typeof action.type !== "string") return { allowed: false, reason: "invalid_input" };
  if (!Array.isArray(task.allowed_actions) || !Array.isArray(task.source_scopes)) return { allowed: false, reason: "invalid_task" };
  if (task.status !== "running") return { allowed: false, reason: "task_not_running" };
  if (HIGH_IMPACT.includes(action.type)) return { allowed: false, reason: "human_approval_and_authorized_adapter_required" };
  if (!LOW_RISK.includes(action.type) || !task.allowed_actions.includes(action.type)) return { allowed: false, reason: "action_not_allowed" };
  if (action.type === "read_approved_source" && (typeof action.resource !== "string" || !task.source_scopes.includes(action.resource))) return { allowed: false, reason: "resource_not_in_scope" };
  const steps = usage.steps ?? 0, calls = usage.tool_calls ?? 0, cost = usage.cost_gbp ?? 0;
  if (![steps, calls, cost].every(v => Number.isFinite(v) && v >= 0)) return { allowed: false, reason: "invalid_usage" };
  if (![task.max_steps, task.max_tool_calls, task.max_cost_gbp].every(v => Number.isFinite(v) && v >= 0)) return { allowed: false, reason: "invalid_limits" };
  if (steps >= task.max_steps || calls >= task.max_tool_calls || cost >= task.max_cost_gbp) return { allowed: false, reason: "budget_exhausted" };
  return { allowed: true, reason: "permitted_read_only_or_draft" };
}
