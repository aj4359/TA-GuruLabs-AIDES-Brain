import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { dirname } from "node:path";

const CURRENT_STATUSES = new Set(["NEW", "CURRENT", "CONFIRMED", "APPROVED", "EXPERIMENTAL"]);

export class JsonMemoryStore {
  constructor(filePath) {
    this.filePath = filePath;
  }

  async load() {
    try {
      return JSON.parse(await readFile(this.filePath, "utf8"));
    } catch (error) {
      if (error.code === "ENOENT") return { version: 1, records: [], rules: [] };
      throw error;
    }
  }

  async save(state) {
    await mkdir(dirname(this.filePath), { recursive: true });
    const temporary = `${this.filePath}.tmp`;
    await writeFile(temporary, `${JSON.stringify(state, null, 2)}\n`, "utf8");
    await rename(temporary, this.filePath);
  }

  async transact(mutator) {
    const state = await this.load();
    const result = await mutator(state);
    await this.save(state);
    return result;
  }

  async put(record) {
    validateRecord(record);
    return this.transact((state) => {
      if (state.records.some(({ id }) => id === record.id)) throw new Error(`Duplicate record id: ${record.id}`);
      state.records.push(structuredClone(record));
      return record;
    });
  }

  async records({ domain, subject, includeHistorical = false } = {}) {
    const { records } = await this.load();
    return records.filter((record) =>
      (!domain || record.domain === domain) &&
      (!subject || record.subject === subject) &&
      (includeHistorical || CURRENT_STATUSES.has(record.status))
    );
  }

  async current(domain, subject) {
    const records = await this.records({ domain, subject });
    return records.sort((a, b) => Date.parse(b.observedAt) - Date.parse(a.observedAt))[0] ?? null;
  }
}

export function validateRecord(record) {
  for (const key of ["id", "type", "subject", "statement", "domain", "status", "observedAt"]) {
    if (!record[key]) throw new Error(`Memory record requires ${key}`);
  }
  if (!Number.isFinite(record.confidence) || record.confidence < 0 || record.confidence > 1) {
    throw new Error("Memory record confidence must be between 0 and 1");
  }
  if (!record.evidence?.length) throw new Error("Memory record requires evidence");
  if (!record.permissions?.scope) throw new Error("Memory record requires permissions.scope");
}
