#!/usr/bin/env node
'use strict';

const path = require('node:path');
const fs = require('node:fs');
const crypto = require('node:crypto');
const config = require('./config.cjs');
const pricing = require('./pricing.cjs');
const client = require('./client.cjs');
const ledger = require('./ledger.cjs');

const IMAGE_OPS = ['generate-image', 'edit-image'];

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const tok = argv[i];
    if (!tok.startsWith('--')) continue;
    const key = tok.slice(2);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i++;
    }
  }
  return args;
}

function splitUrls(value) {
  if (!value) return undefined;
  return String(value)
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

function printUsage() {
  console.log(`Artidoro Hero Lab — APIMart Media Generator

Uso:
  node cli.cjs generate-image --model <modelo> --prompt "<texto>" [--size 1:1] [--n 1] [--override-budget "<motivo>"]
  node cli.cjs edit-image     --model <modelo> --prompt "<texto>" --image-urls url1,url2 [--mask-url url] [--override-budget "<motivo>"]
  node cli.cjs generate-video --model <modelo> --prompt "<texto>" --human-approval "<texto no vacío>" [...]
  node cli.cjs status         --task-id <task_id> [--language en]
  node cli.cjs download       --task-id <task_id> [--out <carpeta>]

Presupuesto activo: TOTAL_BUDGET_USD=${config.TOTAL_BUDGET_USD} IMAGE_AUTO_BUDGET_USD=${config.IMAGE_AUTO_BUDGET_USD} VIDEO_REQUIRES_APPROVAL=${config.VIDEO_REQUIRES_APPROVAL}
`);
}

function checkImageBudget({ operation, model, n, resolution }) {
  const estimate = pricing.estimateCost(model, n, resolution);
  const estimatedUsd = estimate ? estimate.estimatedUsd : null;

  const spentTotal = ledger.sumSpentUsd(); // todas las operaciones, para el techo duro
  const spentImages = ledger.sumSpentUsd({ operations: IMAGE_OPS });

  const projectedTotal = spentTotal + (estimatedUsd ?? 0);
  const projectedImages = spentImages + (estimatedUsd ?? 0);

  if (projectedTotal > config.TOTAL_BUDGET_USD) {
    throw new Error(
      `Bloqueado: TOTAL_BUDGET_USD=${config.TOTAL_BUDGET_USD} es un techo duro sin excepción. ` +
        `Gastado hasta ahora: $${spentTotal.toFixed(4)}. Proyectado con esta operación: $${projectedTotal.toFixed(4)}.`
    );
  }

  return { estimate, spentImages, projectedImages, spentTotal, projectedTotal };
}

async function cmdGenerateOrEditImage(op, args) {
  const model = args.model;
  const prompt = args.prompt;
  if (!model || !prompt) {
    throw new Error(`${op} requiere --model y --prompt.`);
  }
  const n = args.n ? Number.parseInt(args.n, 10) : 1;
  const remoteUrls = splitUrls(args['image-urls']) || [];
  const imageFiles = (splitUrls(args['image-files']) || []).map(file => {
    const absolute = path.resolve(file);
    const mime = {'.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp'}[path.extname(absolute).toLowerCase()];
    if (!mime) throw new Error('Unsupported reference image format');
    const data = fs.readFileSync(absolute);
    if (data.length > 30 * 1024 * 1024) throw new Error('Reference image exceeds 30MB');
    return {path:absolute,sha256:crypto.createHash('sha256').update(data).digest('hex'),uri:`data:${mime};base64,${data.toString('base64')}`};
  });
  const allReferences = [...imageFiles.map(f=>f.uri), ...remoteUrls];
  const image_urls = allReferences.length ? allReferences : undefined;
  if (op === 'edit-image' && (!image_urls || image_urls.length === 0)) {
    throw new Error('edit-image requiere --image-urls o --image-files (al menos una referencia).');
  }

  const { estimate, projectedImages } = checkImageBudget({ operation: op, model, n, resolution: args.resolution });

  if (estimate === null && !args['override-budget']) {
    throw new Error(
      `El modelo "${model}" no tiene tarifa tabulada en pricing.cjs (no se puede estimar coste previo con confianza). ` +
        'Pasa --override-budget "<motivo>" para continuar bajo tu propio criterio, o usa un modelo tabulado (ver pricing.cjs).'
    );
  }

  if (estimate !== null && projectedImages > config.IMAGE_AUTO_BUDGET_USD && !args['override-budget']) {
    throw new Error(
      `Bloqueado: IMAGE_AUTO_BUDGET_USD=${config.IMAGE_AUTO_BUDGET_USD}. ` +
        `Proyectado en imágenes: $${projectedImages.toFixed(4)}. ` +
        'Pasa --override-budget "<motivo>" para continuar de todas formas (queda registrado en el ledger).'
    );
  }

  console.log(
    `[${op}] modelo=${model} n=${n} estimado=${estimate ? '$' + estimate.estimatedUsd.toFixed(4) : 'desconocido'}` +
      (args['override-budget'] ? ` override="${args['override-budget']}"` : '')
  );

  const response = await client.generateImage({
    model,
    prompt,
    size: args.size,
    resolution: args.resolution,
    n,
    image_urls,
    mask_url: args['mask-url'],
  });

  const data = response?.data?.[0];
  if (!data?.task_id) {
    throw new Error('Respuesta de APIMart sin task_id: ' + JSON.stringify(response));
  }

  const entry = ledger.appendEntry({
    operation: op,
    model,
    params: { prompt, size: args.size, resolution: args.resolution, n, image_urls: remoteUrls, image_files: imageFiles.map(({path,sha256})=>({path,sha256})), reference_order:'local files, then remote URLs', mask_url: args['mask-url'] || null },
    task_id: data.task_id,
    status: data.status || 'submitted',
    estimated_cost_usd: estimate ? estimate.estimatedUsd : null,
    human_approval: args['override-budget'] || null,
  });

  console.log(`Enviado. task_id=${entry.task_id} status=${entry.status}`);
  console.log(`Consulta con: node cli.cjs status --task-id ${entry.task_id}`);
}

async function cmdGenerateVideo(args) {
  const model = args.model;
  const prompt = args.prompt;
  if (!model || !prompt) {
    throw new Error('generate-video requiere --model y --prompt.');
  }

  if (config.VIDEO_REQUIRES_APPROVAL && (!args['human-approval'] || args['human-approval'] === true)) {
    throw new Error(
      'Bloqueado: la generación de video SIEMPRE requiere --human-approval "<texto de aprobación>" no vacío. ' +
        'No se ha llamado a la API de APIMart.'
    );
  }

  const spentTotal = ledger.sumSpentUsd();
  console.log(
    `[generate-video] modelo=${model} — coste no estimable con confianza (no tabulado). ` +
      `Gasto acumulado hasta ahora: $${spentTotal.toFixed(4)} de TOTAL_BUDGET_USD=${config.TOTAL_BUDGET_USD}.`
  );

  const response = await client.generateVideo({
    model,
    prompt,
    duration: args.duration ? Number.parseInt(args.duration, 10) : undefined,
    aspect_ratio: args['aspect-ratio'],
    image_urls: splitUrls(args['image-urls']),
    resolution: args.resolution,
    generation_type: args['generation-type'],
  });

  const data = response?.data?.[0];
  if (!data?.task_id) {
    throw new Error('Respuesta de APIMart sin task_id: ' + JSON.stringify(response));
  }

  const entry = ledger.appendEntry({
    operation: 'generate-video',
    model,
    params: { prompt, duration: args.duration, aspect_ratio: args['aspect-ratio'] },
    task_id: data.task_id,
    status: data.status || 'submitted',
    estimated_cost_usd: null,
    human_approval: args['human-approval'],
  });

  console.log(`Enviado. task_id=${entry.task_id} status=${entry.status}`);
}

function extractResultUrls(statusData) {
  const images = statusData?.result?.images || [];
  const videos = statusData?.result?.videos || [];
  const urls = [];
  for (const item of [...images, ...videos]) {
    const u = Array.isArray(item.url) ? item.url : [item.url];
    urls.push(...u.filter(Boolean));
  }
  return urls;
}

async function cmdStatus(args) {
  const taskId = args['task-id'];
  if (!taskId) throw new Error('status requiere --task-id.');
  const response = await client.getStatus(taskId, args.language || 'en');
  const data = response?.data;
  console.log(JSON.stringify(data, null, 2));

  if (data?.status === 'completed') {
    const resultUrls = extractResultUrls(data);
    ledger.updateEntryByTaskId(taskId, {
      status: data.status,
      actual_cost_usd: typeof data.cost === 'number' ? data.cost : null,
      credits_cost: data.credits_cost ?? null,
      timestamp_completed: new Date().toISOString(),
      result_urls: resultUrls,
    });
    console.log(`Ledger actualizado. cost real=${data.cost ?? 'no reportado'} USD`);
  } else if (data?.status) {
    try {
      ledger.updateEntryByTaskId(taskId, { status: data.status });
    } catch {
      // La tarea puede no estar en el ledger local (ej. consultada manualmente); no es fatal.
    }
  }
}

async function cmdDownload(args) {
  const taskId = args['task-id'];
  if (!taskId) throw new Error('download requiere --task-id.');

  const entries = ledger.readLedger();
  let entry = entries.find((e) => e.task_id === taskId);

  if (!entry || !entry.result_urls || entry.result_urls.length === 0) {
    // refrescar desde la API por si status no se consultó aún
    const response = await client.getStatus(taskId, 'en');
    const data = response?.data;
    if (data?.status !== 'completed') {
      throw new Error(`La tarea ${taskId} no está completada todavía (status=${data?.status}).`);
    }
    const resultUrls = extractResultUrls(data);
    entry = ledger.updateEntryByTaskId(taskId, {
      status: data.status,
      actual_cost_usd: typeof data.cost === 'number' ? data.cost : entry?.actual_cost_usd ?? null,
      credits_cost: data.credits_cost ?? entry?.credits_cost ?? null,
      timestamp_completed: entry?.timestamp_completed || new Date().toISOString(),
      result_urls: resultUrls,
    });
  }

  const outDir = args.out || path.join(__dirname, 'data', 'downloads', taskId);
  const downloaded = [];
  for (let i = 0; i < entry.result_urls.length; i++) {
    const url = entry.result_urls[i];
    const ext = url.split('?')[0].split('.').pop().slice(0, 5) || 'bin';
    const dest = path.join(outDir, `${taskId}_${i}.${ext}`);
    await client.downloadFile(url, dest);
    downloaded.push(dest);
    console.log(`Descargado: ${dest}`);
  }

  ledger.updateEntryByTaskId(taskId, { downloaded_paths: downloaded });
}

async function main() {
  const [, , command, ...rest] = process.argv;
  const args = parseArgs(rest);

  if (!command || command.startsWith('--') || args.help || args.h) {
    printUsage();
    return;
  }

  switch (command) {
    case 'generate-image':
      return cmdGenerateOrEditImage('generate-image', args);
    case 'edit-image':
      return cmdGenerateOrEditImage('edit-image', args);
    case 'generate-video':
      return cmdGenerateVideo(args);
    case 'status':
      return cmdStatus(args);
    case 'download':
      return cmdDownload(args);
    default:
      printUsage();
      throw new Error(`Comando desconocido: ${command}`);
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exitCode = 1;
});
