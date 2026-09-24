'use strict';

const fs = require('node:fs');
const path = require('node:path');

const ENV_PATH = path.join(__dirname, '.env');

function loadDotEnv(filePath) {
  if (!fs.existsSync(filePath)) return;
  const raw = fs.readFileSync(filePath, 'utf8');
  for (const line of raw.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    const value = trimmed.slice(eq + 1).trim();
    if (key && !(key in process.env)) {
      process.env[key] = value;
    }
  }
}

loadDotEnv(ENV_PATH);

function parseBool(value, fallback) {
  if (value === undefined || value === '') return fallback;
  return /^(1|true|yes)$/i.test(value.trim());
}

function parseFloatOr(value, fallback) {
  if (value === undefined || value === '') return fallback;
  const n = Number.parseFloat(value);
  return Number.isFinite(n) ? n : fallback;
}

const APIMART_API_KEY = process.env.APIMART_API_KEY || '';

const TOTAL_BUDGET_USD = parseFloatOr(process.env.TOTAL_BUDGET_USD, 5.0);
const IMAGE_AUTO_BUDGET_USD = parseFloatOr(process.env.IMAGE_AUTO_BUDGET_USD, 1.0);
const VIDEO_REQUIRES_APPROVAL = parseBool(process.env.VIDEO_REQUIRES_APPROVAL, true);

const BASE_URL = 'https://api.apimart.ai/v1/';

function requireApiKey() {
  if (!APIMART_API_KEY) {
    throw new Error(
      'APIMART_API_KEY no está configurada. Copia tools/apimart/.env.example a tools/apimart/.env y completa la clave (nunca la imprimas ni la commitees).'
    );
  }
  return APIMART_API_KEY;
}

// Nunca loguear el objeto completo de config (contiene la API key). Usar esto para logs/diagnóstico.
function safeConfigSummary() {
  return {
    baseUrl: BASE_URL,
    hasApiKey: Boolean(APIMART_API_KEY),
    totalBudgetUsd: TOTAL_BUDGET_USD,
    imageAutoBudgetUsd: IMAGE_AUTO_BUDGET_USD,
    videoRequiresApproval: VIDEO_REQUIRES_APPROVAL,
  };
}

module.exports = {
  BASE_URL,
  TOTAL_BUDGET_USD,
  IMAGE_AUTO_BUDGET_USD,
  VIDEO_REQUIRES_APPROVAL,
  requireApiKey,
  safeConfigSummary,
};
