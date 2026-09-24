'use strict';

const fs = require('node:fs');
const path = require('node:path');

const LEDGER_PATH = path.join(__dirname, 'data', 'ledger.json');

function readLedger() {
  if (!fs.existsSync(LEDGER_PATH)) return [];
  const raw = fs.readFileSync(LEDGER_PATH, 'utf8').trim();
  if (!raw) return [];
  return JSON.parse(raw);
}

function writeLedger(entries) {
  fs.mkdirSync(path.dirname(LEDGER_PATH), { recursive: true });
  fs.writeFileSync(LEDGER_PATH, JSON.stringify(entries, null, 2) + '\n');
}

function makeEntryId() {
  const ts = new Date().toISOString().replace(/[:.]/g, '-');
  const rand = Math.random().toString(36).slice(2, 8);
  return `${ts}_${rand}`;
}

/**
 * entry: { operation, model, params, task_id, status, estimated_cost_usd, human_approval }
 */
function appendEntry(entry) {
  const entries = readLedger();
  const full = {
    id: makeEntryId(),
    operation: entry.operation,
    model: entry.model,
    params: entry.params || {},
    task_id: entry.task_id || null,
    status: entry.status || 'submitted',
    estimated_cost_usd: entry.estimated_cost_usd ?? null,
    actual_cost_usd: null,
    credits_cost: null,
    timestamp_submitted: new Date().toISOString(),
    timestamp_completed: null,
    result_urls: [],
    downloaded_paths: [],
    human_approval: entry.human_approval || null,
    error: null,
  };
  entries.push(full);
  writeLedger(entries);
  return full;
}

function updateEntryByTaskId(taskId, patch) {
  const entries = readLedger();
  const idx = entries.findIndex((e) => e.task_id === taskId);
  if (idx === -1) {
    throw new Error(`No hay entrada de ledger con task_id ${taskId}`);
  }
  entries[idx] = { ...entries[idx], ...patch };
  writeLedger(entries);
  return entries[idx];
}

/**
 * Suma gasto: usa actual_cost_usd (fuente de verdad, viene del status real de
 * APIMart) cuando existe; para tareas aún no completadas, cae a estimated_cost_usd
 * como aproximación conservadora del compromiso pendiente.
 */
function sumSpentUsd({ operation, operations } = {}) {
  const allowed = operations || (operation ? [operation] : null);
  const entries = readLedger().filter((e) => !allowed || allowed.includes(e.operation));
  return entries.reduce((sum, e) => {
    const cost = e.actual_cost_usd ?? e.estimated_cost_usd ?? 0;
    return sum + cost;
  }, 0);
}

module.exports = {
  LEDGER_PATH,
  readLedger,
  appendEntry,
  updateEntryByTaskId,
  sumSpentUsd,
};
