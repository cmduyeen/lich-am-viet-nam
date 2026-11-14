import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import http from 'node:http';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {chromium} from 'playwright';
import {marked} from 'marked';
import {readCalendar} from './reader.mjs';

const directory=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(directory,'../..');
const evidence=path.resolve(process.env.EVIDENCE_DIR || path.join(directory,'artifacts'));
await fs.mkdir(evidence,{recursive:true});
const checks=[];const errors=[];let browser,server;
const temp=await fs.mkdtemp(path.join(os.tmpdir(),'lunar-consumer-'));
const python=process.env.PYTHON || 'python';
function check(label,value=true){assert(value,label);checks.push(label);}
function sha(raw){return createHash('sha256').update(raw).digest('hex');}
const docStyle=`*{box-sizing:border-box;cursor:none!important}body{margin:0;color:#1f2328;background:#f6f8fa;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}article{max-width:1060px;margin:26px auto;padding:32px 46px;background:white;border:1px solid #d1d9e0;border-radius:8px}h1,h2{line-height:1.3;border-bottom:1px solid #d8dee4;padding-bottom:10px}h1{font-size:30px}h2{font-size:23px;margin-top:26px}a{color:#0969da;text-decoration:none}p{margin:14px 0}pre{padding:16px;background:#f6f8fa;border-radius:6px;overflow:auto;font-size:13px;line-height:1.7}code{font-family:Consolas,monospace}summary{padding:9px 0;color:#34495e}blockquote{border-left:3px solid #d0d7de;margin-left:0;padding-left:16px;color:#59636e}table{border-collapse:collapse}td,th{border:1px solid #d1d9e0;padding:7px 12px}img{max-width:100%}.label{font-size:11px;letter-spacing:1px;color:#6e7781;text-transform:uppercase;margin:0 0 22px}@media(max-width:600px){article{margin:0;border:0;padding:20px}h1{font-size:25px}h2{font-size:21px}body{font-size:14px}}`;
function buildCustom(color){
 const config=path.join(temp,'calendar.json');
 const args=[path.join(root,'main.py'),'--config',config,'--output-dir',temp];
 if(color)args.push('--holiday-color',color);
 const result=spawnSync(python,args,{encoding:'utf8',env:{...process.env,PYTHONUTF8:'1'}});
 assert.equal(result.status,0,result.stderr||result.stdout);
}
try{
 const inventory=JSON.parse(await fs.readFile(path.join(root,'output/index.json'),'utf8'));
 let totalEvents=0;
 for(const entry of inventory){
  const raw=await fs.readFile(path.join(root,'output',entry.file));
  assert.equal(sha(raw),entry.sha256,entry.file);
  const parsed=readCalendar(raw.toString('utf8'));
  assert.equal(parsed.events.length,entry.events,entry.file);
  for(const event of parsed.events){assert(event.start>=`${entry.start_year}-01-01`&&event.start<=`${entry.end_year}-12-31`);}
  totalEvents+=parsed.events.length;
 }
 check(`Independent ICAL.js parse, checksums, UIDs and all-day boundaries: ${inventory.length} feeds / ${totalEvents} events`);
 await fs.writeFile(path.join(temp,'calendar.json'),JSON.stringify({country:'VN',content:'festivals',language:'vi',feed_name:'consumer-test',start_year:2026,end_year:2027}));
 buildCustom();
 server=http.createServer(async(req,res)=>{
  try{
   const url=new URL(req.url,'http://localhost');
   let file;
   if(url.pathname==='/viewer')file=path.join(directory,'viewer.html');
   else if(url.pathname==='/custom.ics')file=path.join(temp,'custom_consumer-test_latest.ics');
   else {file=path.resolve(root,'.'+decodeURIComponent(url.pathname));if(!file.startsWith(root+path.sep))throw new Error('Outside root');}
   let raw=await fs.readFile(file);
   if(file.endsWith('.md'))raw=Buffer.from(`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>${docStyle}</style><article><p class="label">Repository README · local rendering</p>${marked.parse(raw.toString('utf8'))}</article>`);
   const etag='"'+sha(raw)+'"';res.setHeader('ETag',etag);res.setHeader('Cache-Control','no-cache');
   if(req.headers['if-none-match']===etag){res.writeHead(304);res.end();return;}
   const type=file.endsWith('.md')||file.endsWith('.html')?'text/html':file.endsWith('.ics')?'text/calendar':file.endsWith('.json')?'application/json':file.endsWith('.js')||file.endsWith('.mjs')?'text/javascript':'application/octet-stream';
   res.setHeader('Content-Type',type+'; charset=utf-8');res.end(raw);
  }catch(error){res.writeHead(404);res.end('Not found');}
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base=`http://127.0.0.1:${server.address().port}`;
 browser=await chromium.launch(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{});
 const context=await browser.newContext({viewport:{width:1440,height:1050},timezoneId:'America/Los_Angeles',deviceScaleFactor:1});
 const page=await context.newPage();page.on('pageerror',error=>errors.push(error.message));
 await page.goto(base+'/README.md');
 check('Root region lists collapsed by default',await page.locator('details[open]').count()===0);
 await page.locator('summary').filter({hasText:/^East Asia$/}).click();
 check('Region expands and exposes country links',await page.locator('a[href="china/README.md"]').isVisible());
 await page.locator('summary').filter({hasText:/^Southeast Asia$/}).click();
 await page.screenshot({path:path.join(evidence,'01-country-selector.png')});
 await page.getByRole('link',{name:'Tiếng Việt',exact:true}).click();
 const copyUrl=await page.locator('pre code').first().textContent();
 check('Vietnam native guide exposes one clean subscription URL',copyUrl.trim()==='https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_vn_vietnamese_vi_festivals_latest.ics');
 check('Vietnam guide keeps secondary choices collapsed',await page.locator('details[open]').count()===0);
 await page.screenshot({path:path.join(evidence,'02-vietnam-guide.png')});
 const guides=['vietnam/README.vi.md','china/README.zh-Hans.md','taiwan/README.zh-Hant.md','hong-kong/README.zh-Hant.md','macao/README.zh-Hant.md','south-korea/README.ko.md','singapore/README.zh-Hans.md','malaysia/README.ms.md'];
 for(const guide of guides){
  await page.goto(base+'/'+guide);assert(await page.locator('pre code').first().isVisible());
  const mobile=await context.newPage({viewport:{width:390,height:844}});
  await mobile.setViewportSize({width:390,height:844});await mobile.goto(base+'/'+guide);
  assert(await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),guide+' horizontal overflow');
  if(guide==='malaysia/README.ms.md')await page.screenshot({path:path.join(evidence,'03-malaysia-guide.png')});
  if(guide==='vietnam/README.vi.md')await mobile.screenshot({path:path.join(evidence,'04-vietnam-mobile.png')});
  await mobile.close();
 }
 check('Eight native country guides: desktop URL visibility and 390px layout without horizontal overflow');
 async function show(feed,date){await page.goto(`${base}/viewer?feed=${encodeURIComponent(feed)}&date=${date}`);await page.waitForFunction(()=>window.ready===true);}
 await show('/output/lunar_hk_chinese_zh-Hant_festivals_latest.ics','2026-05-01');
 check('HK May 24 renders both Buddha and Tam Kung festivals',await page.locator('.fc-daygrid-day[data-date="2026-05-24"] .fc-event').count()===2);
 await page.screenshot({path:path.join(evidence,'05-hong-kong-calendar.png')});
 await show('/output/lunar_kr_korean_ko_festivals_latest.ics','2026-09-01');
 for(const date of ['2026-09-24','2026-09-25','2026-09-26'])assert(await page.locator(`.fc-daygrid-day[data-date="${date}"] .fc-event`).count()>=1,date);
 check('Korean Chuseok spans its three separate all-day dates in the rendered calendar');
 await page.screenshot({path:path.join(evidence,'06-korea-calendar.png')});
 await show('/custom.ics','2026-02-01');
 const before=await page.evaluate(()=>window.calendar.getEvents().map(e=>[e.id,e.startStr,e.endStr]));
 await page.evaluate(()=>window.refreshFeed());
 check('Unchanged subscription receives HTTP 304',await page.locator('#status').textContent()==='Unchanged · HTTP 304');
 buildCustom('#123ABC');await page.evaluate(()=>window.refreshFeed());
 const after=await page.evaluate(()=>window.calendar.getEvents().map(e=>[e.id,e.startStr,e.endStr]));
 assert.deepEqual(after,before);
 check('CLI update → HTTP feed → browser refresh preserves dates/UIDs with zero duplicate events');
 check('Updated event revisions visible through independent parser',await page.evaluate(()=>window.loadedEvents.every(e=>e.extendedProps.sequence===1)));
 await page.screenshot({path:path.join(evidence,'07-custom-subscription.png')});
 for(const zone of ['Asia/Ho_Chi_Minh','Asia/Shanghai','Asia/Seoul','America/New_York']){
  const zoneContext=await browser.newContext({timezoneId:zone});const zonePage=await zoneContext.newPage();
  await zonePage.goto(`${base}/viewer?feed=/output/lunar_us_vietnamese_en_festivals_latest.ics&date=2026-02-01`);await zonePage.waitForFunction(()=>window.ready);
  const value=await zonePage.evaluate(()=>window.calendar.getEvents().find(e=>e.extendedProps.identity==='lunar_new_year').startStr);
  assert.equal(value,'2026-02-17',zone);await zoneContext.close();
 }
 check('Four browser timezones preserve the source all-day date, including US residence feeds');
 assert.deepEqual(errors,[]);check('No browser JavaScript errors');
 await fs.writeFile(path.join(evidence,'results.json'),JSON.stringify({status:'passed',feeds:inventory.length,events:totalEvents,checks,screenshots:'Browser-native capture; no pointer overlay',scope:'Local actual ICS + ICAL.js + FullCalendar. Not Google/Apple/Outlook subscription certification.'},null,2)+'\n');
 console.log(JSON.stringify({status:'passed',feeds:inventory.length,events:totalEvents,checks:checks.length,evidence},null,2));
}finally{
 if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));
 const resolvedTemp=path.resolve(temp);
 if(path.dirname(resolvedTemp)!==path.resolve(os.tmpdir()) || !path.basename(resolvedTemp).startsWith('lunar-consumer-'))throw new Error('Unsafe temporary cleanup target');
 await fs.rm(resolvedTemp,{recursive:true,force:true});
}
