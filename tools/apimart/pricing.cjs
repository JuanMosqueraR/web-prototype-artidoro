'use strict';

// NO es fuente de verdad. Solo ayuda a estimar ANTES de enviar una operación,
// para decidir si cabe dentro de IMAGE_AUTO_BUDGET_USD. El coste real y
// autoritativo siempre viene del campo `cost` que devuelve GET /v1/tasks/{task_id}
// una vez completada la tarea (ver ledger.cjs). Los precios de APIMart cambian;
// esta tabla puede quedar desactualizada.
//
// Fuente: https://apimart.ai/pricing y https://docs.apimart.ai (verificado 17-sep-2026).
const KNOWN_RATES_USD = {
  'z-image-turbo': {
    usdPerImage: 0.01,
    source: 'apimart.ai/pricing — Z Image Turbo, default',
    checkedAt: '2026-09-17',
  },
  'gpt-image-2-1k': {
    usdPerImage: 0.0085,
    source: 'apimart.ai/pricing — GPT Image 2, 1K/default',
    checkedAt: '2026-09-17',
  },
  'gpt-image-2-2k': {
    usdPerImage: 0.014,
    source: 'apimart.ai/pricing — GPT Image 2, 2K',
    checkedAt: '2026-09-17',
  },
  'gpt-image-2-4k': {
    usdPerImage: 0.021,
    source: 'apimart.ai/pricing — GPT Image 2, 4K',
    checkedAt: '2026-09-17',
  },
};

/**
 * Devuelve una estimación en USD, o null si el modelo no está tabulado
 * o la tarifa no se considera suficientemente fiable. Nunca inventa un número.
 */
function estimateCost(model, n = 1, resolution) {
  let rate = KNOWN_RATES_USD[model];
  if (['gemini-3-pro-image-preview', 'nano-banana-pro-ext'].includes(model)) {
    const tier = String(resolution || '1K').toUpperCase();
    if (!['1K', '2K', '4K'].includes(tier)) return null;
    rate = {
      usdPerImage: tier === '4K' ? 0.04 : 0.03,
      source: 'https://apimart.ai/pricing — nano-banana-pro-ext (compatible alias), ' + tier,
      checkedAt: '2026-09-17',
    };
  }
  if (!rate) return null;
  return {
    estimatedUsd: rate.usdPerImage * n,
    perUnitUsd: rate.usdPerImage,
    source: rate.source,
    checkedAt: rate.checkedAt,
  };
}

module.exports = { KNOWN_RATES_USD, estimateCost };
