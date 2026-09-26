'use strict';
// Uses the existing APIMart client without changing pre-existing tooling.
// Every POST is explicit; status only polls. Never prints credentials or signed URLs.
const client = require('../tools/apimart/client.cjs');
const ledger = require('../tools/apimart/ledger.cjs');
const config = require('../tools/apimart/config.cjs');
const frames = {
  desktop: ['task_01M3CN9DX8D1E6N2ZVV1DZJDT3', 'task_01M3CN3TTG0XWGX46M42YXSW46'],
  mobile: ['task_01M3CN9FYWMC008BB972DF258D', 'task_01M3CN9F19E18M5SPNT44Z8TCX'],
};
const approval = 'User explicitly authorized generated images/video for scene 03 and execution of the 01-05 home on 2026-09-25.';
async function main() {
  const [command, value] = process.argv.slice(2);
  if (command === 'status') {
    const {data} = await client.getStatus(value);
    const patch = {status: data.status};
    if (data.status === 'completed') {
      Object.assign(patch, {actual_cost_usd: data.cost ?? null, credits_cost: data.credits_cost ?? null,
        timestamp_completed: new Date().toISOString(),
        result_urls: [...(data.result?.images || []), ...(data.result?.videos || [])].flatMap(x => x.url)});
    }
    if (data.error) patch.error = data.error;
    ledger.updateEntryByTaskId(value, patch);
    console.log(JSON.stringify({task: value, status: data.status, cost: data.cost, error: data.error}));
    return;
  }
  if (command !== 'video' || !frames[value]) throw new Error('Use: video desktop|mobile, or status TASK_ID');
  const duration = 7;
  // Provider public pricing, checked 2026-09-25: standard 720p, no audio, $0.0672/s.
  const estimate = duration * 0.0672;
  if (ledger.sumSpentUsd() + estimate > config.TOTAL_BUDGET_USD) throw new Error('Configured total budget would be exceeded.');
  const entries = ledger.readLedger();
  const image_urls = frames[value].map(id => entries.find(e => e.task_id === id)?.result_urls[0]);
  if (image_urls.some(x => !x)) throw new Error('Both completed first/last frame URLs are required.');
  const prompt = 'One continuous premium coffee cinematography shot. Start exactly on the extreme macro first image: we are inside the dark surface of black filter coffee, a copper-gold ring ripple moving very gently. The camera smoothly dollies backward and rises, a dramatic but beautifully fluid change of scale. The coffee surface gets smaller, the real ivory ceramic cup rim gradually enters frame, then reveal the whole cup on the dark walnut table, arriving exactly at the supplied final frame. The liquid is always inside the SAME cup: no morph, no dissolve, no cut, no new objects. Subtle physically plausible surface ripples settling and delicate steam. Warm raking sunlight, deep forest-green shadows, cinematic chiaroscuro, photorealistic optical macro to medium shot. Keep the coffee dark, without crema, foam or milk. Cup remains stationary. No hands, no pouring, no ingredients, no text, no logos, no packaging, no sound. Camera eases to a complete rest in the last second. Preserve composition and lighting of the end frame.';
  const params = {model:'kling-v3',prompt,duration,aspect_ratio:value === 'mobile' ? '9:16':'16:9',image_urls};
  const response = await client.generateVideo(params);
  const task = response?.data?.[0];
  if (!task?.task_id) throw new Error('No task ID returned');
  ledger.appendEntry({operation:'generate-video',model:params.model,
    params:{prompt,duration,aspect_ratio:params.aspect_ratio,frame_task_ids:frames[value],mode:'std (provider default)',audio:false,pricing_source:'https://apimart.ai/blog/kling-3-0-fast-api-pricing-features-how-to-access-2026'},
    task_id:task.task_id,status:task.status,estimated_cost_usd:estimate,human_approval:approval});
  console.log(JSON.stringify({device:value,task:task.task_id,status:task.status,estimated_usd:estimate}));
}
main().catch(e => {console.error(e.message);process.exitCode=1;});
