'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { BASE_URL, requireApiKey } = require('./config.cjs');

const ERROR_HINTS = {
  400: 'Parámetros inválidos.',
  401: 'Autenticación fallida — revisa APIMART_API_KEY en tools/apimart/.env.',
  402: 'Saldo insuficiente en la cuenta de APIMart.',
  403: 'Permiso denegado para esta operación/modelo.',
  429: 'Límite de tasa excedido — reintenta más tarde.',
  500: 'Error del servidor de APIMart.',
  502: 'Error de gateway de APIMart.',
};

async function apimartFetch(pathname, { method = 'GET', body } = {}) {
  const apiKey = requireApiKey();
  const url = new URL(pathname, BASE_URL);
  const res = await fetch(url, {
    method,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  let json;
  try {
    json = await res.json();
  } catch {
    json = null;
  }

  if (!res.ok) {
    const hint = ERROR_HINTS[res.status] || 'Error no clasificado.';
    const message = json?.message || json?.error || '(sin detalle en el body)';
    const err = new Error(`APIMart ${res.status}: ${hint} ${message}`);
    err.status = res.status;
    err.body = json;
    throw err;
  }

  return json;
}

/**
 * Genera o edita una imagen. Para edición/referencia, pasar image_urls poblado —
 * es el mismo endpoint, no existe uno separado según la doc real de APIMart.
 */
async function generateImage({ model, prompt, size, resolution, n, image_urls, mask_url } = {}) {
  if (!model) throw new Error('generateImage requiere "model".');
  if (!prompt) throw new Error('generateImage requiere "prompt".');
  const body = { model, prompt };
  if (size) body.size = size;
  if (resolution) body.resolution = resolution;
  if (n) body.n = n;
  if (image_urls) body.image_urls = image_urls;
  if (mask_url) body.mask_url = mask_url;
  return apimartFetch('/v1/images/generations', { method: 'POST', body });
}

async function generateVideo({
  model,
  prompt,
  duration,
  aspect_ratio,
  image_urls,
  resolution,
  generation_type,
} = {}) {
  if (!model) throw new Error('generateVideo requiere "model".');
  if (!prompt) throw new Error('generateVideo requiere "prompt".');
  const body = { model, prompt };
  if (duration) body.duration = duration;
  if (aspect_ratio) body.aspect_ratio = aspect_ratio;
  if (image_urls) body.image_urls = image_urls;
  if (resolution) body.resolution = resolution;
  if (generation_type) body.generation_type = generation_type;
  return apimartFetch('/v1/videos/generations', { method: 'POST', body });
}

async function getStatus(taskId, language = 'en') {
  if (!taskId) throw new Error('getStatus requiere "taskId".');
  return apimartFetch(`/v1/tasks/${encodeURIComponent(taskId)}?language=${encodeURIComponent(language)}`);
}

/**
 * Descarga una URL de resultado (imagen/video) a un archivo local.
 * No loguea la URL completa (puede llevar firma/token) — solo el destino.
 */
async function downloadFile(url, destPath) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Descarga fallida (${res.status}) hacia ${destPath}`);
  }
  const buffer = Buffer.from(await res.arrayBuffer());
  fs.mkdirSync(path.dirname(destPath), { recursive: true });
  fs.writeFileSync(destPath, buffer);
  return destPath;
}

module.exports = { generateImage, generateVideo, getStatus, downloadFile };
