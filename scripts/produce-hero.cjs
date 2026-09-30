'use strict';
// L28 hero clips «Del cafetal a tu bolsa». Uses the existing APIMart client without changing tooling.
// Every POST is explicit; status only polls. Never prints credentials or signed URLs.
// Use: node scripts/produce-hero.cjs video desktop|mobile origin|beans   or   status TASK_ID
const client = require('../tools/apimart/client.cjs');
const ledger = require('../tools/apimart/ledger.cjs');
const config = require('../tools/apimart/config.cjs');

// First/last frame task IDs (gemini-3-pro-image-preview, 2026-09-30; recorded in audit/source/hero-generation.json).
const frames = {
  desktop: {origin: 'task_01M3SKD8JHE7PG5AD8702ZNTNV', cherries: 'task_01M3SKD9NJHCCWQQQ4B614GHJT', beans: 'task_01M3SKDAW86G6RWWRZP5XE3YYH'},
  mobile: {origin: 'task_01M3SSQRNR8BSNK966VBR9B3PF', cherries: 'task_01M3SSRKE915Z4BZEGCANVV1V3', beans: 'task_01M3SSRN8XBPRYBDNPD1WFPGVC'},
};
const clips = {
  origin: {from: 'origin', to: 'cherries', prompt: 'One continuous premium coffee cinematography shot. Start exactly on the first image: dawn aerial drone view over misty cloud-forest mountains in northern Peru with coffee plantations on the slopes. The camera smoothly descends and glides forward through the drifting mist, down into the canopy of the coffee plantation, arriving in an intimate close-up of an arabica coffee branch with glossy leaves and ripe red cherries, exactly matching the final image, where a few cherries float in the air turning into coffee beans. One fluid graceful camera move, no cut; the landscape never morphs into objects: soft mist passes in front of the lens to bridge the change of scale. Natural dawn light, deep forest-green tones, copper-gold highlights, photorealistic. No people, no animals, no text, no logos, no sound. The camera eases to rest in the last half second.'},
  beans: {from: 'cherries', to: 'beans', prompt: 'One continuous premium coffee cinematography shot. Start exactly on the first image: close-up of an arabica coffee branch with ripe red cherries, a few cherries floating in the air turning into beans. The floating cherries drift slowly to the right and toward the camera, turning into glossy medium-roasted coffee beans that multiply into a flowing slow-motion cascade, while the misty forest background gradually darkens into deep forest-green darkness, arriving exactly at the final image: a curved cascade of roasted beans falling toward a dark walnut surface. Smooth slow motion, physically plausible bean motion, no cut, no flicker. Warm copper-gold rim light. No packaging, no bag, no cup, no hands, no people, no text, no logos, no sound. The motion eases in the last half second.'},
};
const approval = 'L28: user explicitly approved generated video for the home hero on 2026-09-30 («go!»; budget raised by the user to TOTAL_BUDGET_USD=8.00).';

async function main() {
  const [command, device, clipName] = process.argv.slice(2);
  if (command === 'status') {
    const {data} = await client.getStatus(device);
    const patch = {status: data.status};
    if (data.status === 'completed') {
      Object.assign(patch, {actual_cost_usd: data.cost ?? null, credits_cost: data.credits_cost ?? null,
        timestamp_completed: new Date().toISOString(),
        result_urls: [...(data.result?.images || []), ...(data.result?.videos || [])].flatMap(x => x.url)});
    }
    if (data.error) patch.error = data.error;
    ledger.updateEntryByTaskId(device, patch);
    console.log(JSON.stringify({task: device, status: data.status, cost: data.cost, error: data.error}));
    return;
  }
  const clip = clips[clipName];
  if (command !== 'video' || !frames[device] || !clip) throw new Error('Use: video desktop|mobile origin|beans, or status TASK_ID');
  const duration = 5;
  // Provider public pricing, checked 2026-09-25: standard 720p, no audio, $0.0672/s.
  const estimate = duration * 0.0672;
  if (ledger.sumSpentUsd() + estimate > config.TOTAL_BUDGET_USD) throw new Error('Configured total budget would be exceeded.');
  const entries = ledger.readLedger();
  const ids = [frames[device][clip.from], frames[device][clip.to]];
  const image_urls = ids.map(id => entries.find(e => e.task_id === id)?.result_urls?.[0]);
  if (image_urls.some(x => !x)) throw new Error('Both completed first/last frame URLs are required.');
  const params = {model: 'kling-v3', prompt: clip.prompt, duration, aspect_ratio: device === 'mobile' ? '9:16' : '16:9', image_urls};
  const response = await client.generateVideo(params);
  const task = response?.data?.[0];
  if (!task?.task_id) throw new Error('No task ID returned');
  ledger.appendEntry({operation: 'generate-video', model: params.model,
    params: {prompt: clip.prompt, duration, aspect_ratio: params.aspect_ratio, frame_task_ids: ids, clip: clipName, mode: 'std (provider default)', audio: false},
    task_id: task.task_id, status: task.status, estimated_cost_usd: estimate, human_approval: approval});
  console.log(JSON.stringify({device, clip: clipName, task: task.task_id, status: task.status, estimated_usd: estimate}));
}
main().catch(e => { console.error(e.message); process.exitCode = 1; });
