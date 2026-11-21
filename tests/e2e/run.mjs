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
const output=path.resolve(process.env.CALENDAR_OUTPUT_DIR || path.join(root,'output'));
const evidence=path.resolve(process.env.EVIDENCE_DIR || path.join(directory,'artifacts'));
await fs.mkdir(evidence,{recursive:true});
const checks=[];const errors=[];let browser,server;
const temp=await fs.mkdtemp(path.join(os.tmpdir(),'lunar-consumer-'));
const python=process.env.PYTHON || 'python';
function check(label,value=true){assert(value,label);checks.push(label);}
function sha(raw){return createHash('sha256').update(raw).digest('hex');}
const docStyle=`*{box-sizing:border-box;cursor:none!important}body{margin:0;color:#1f2328;background:#f6f8fa;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}article{max-width:1060px;margin:26px auto;padding:32px 46px;background:white;border:1px solid #d1d9e0;border-radius:8px}h1,h2{line-height:1.3;border-bottom:1px solid #d8dee4;padding-bottom:10px}h1{font-size:30px}h2{font-size:23px;margin-top:26px}a{color:#0969da;text-decoration:none}p{margin:14px 0}pre{padding:16px;background:#f6f8fa;border-radius:6px;overflow:auto;font-size:13px;line-height:1.7}code{font-family:Consolas,monospace}summary{padding:9px 0;color:#34495e}blockquote{border-left:3px solid #d0d7de;margin-left:0;padding-left:16px;color:#59636e}table{border-collapse:collapse}td,th{border:1px solid #d1d9e0;padding:7px 12px}img{max-width:100%}p,a{overflow-wrap:anywhere}.label{font-size:11px;letter-spacing:1px;color:#6e7781;text-transform:uppercase;margin:0 0 22px}@media(max-width:600px){article{margin:0;border:0;padding:20px}h1{font-size:25px}h2{font-size:21px}body{font-size:14px}}`;
function buildCustom(color){
 const config=path.join(temp,'calendar.json');
 const args=[path.join(root,'main.py'),'--config',config,'--output-dir',temp];
 if(color)args.push('--holiday-color',color);
 const result=spawnSync(python,args,{encoding:'utf8',env:{...process.env,PYTHONUTF8:'1'}});
 assert.equal(result.status,0,result.stderr||result.stdout);
}
try{
 const inventory=JSON.parse(await fs.readFile(path.join(output,'index.json'),'utf8'));
 assert.equal(inventory.length,2);
 assert.deepEqual(new Set(inventory.map(e=>e.language)),new Set(['vi','en']));
 assert(inventory.every(e=>e.countries.length===1 && e.countries[0]==='VN'));
 let totalEvents=0;
 let englishEvents;
 for(const entry of inventory){
  const raw=await fs.readFile(path.join(output,entry.file));
  assert.equal(sha(raw),entry.sha256,entry.file);
  const parsed=readCalendar(raw.toString('utf8'));
  if(entry.language==='en')englishEvents=parsed.events;
  assert.equal(parsed.events.length,entry.events,entry.file);
  for(const event of parsed.events){assert(event.start>=`${entry.start_year}-01-01`&&event.start<=`${entry.end_year}-12-31`);}
  totalEvents+=parsed.events.length;
 }
 check(`Independent ICAL.js parse, checksums, UIDs and all-day boundaries: ${inventory.length} feeds / ${totalEvents} events`);
 const tet=englishEvents.find(event=>/Lunar New Year.*Day 1/.test(event.title));
 assert(tet,'The rolling feed must contain Vietnamese Lunar New Year');
 const tetDate=tet.start, displayMonth=tetDate.slice(0,7)+'-01';
 const firstYear=inventory[0].start_year, lastYear=inventory[0].end_year;
 await fs.writeFile(path.join(temp,'calendar.json'),JSON.stringify({country:'VN',content:'festivals',language:'vi',feed_name:'consumer-test',start_year:firstYear,end_year:lastYear}));
 buildCustom();
 server=http.createServer(async(req,res)=>{
  try{
   const url=new URL(req.url,'http://localhost');
   let file;
   if(url.pathname==='/viewer')file=path.join(directory,'viewer.html');
   else if(url.pathname==='/custom.ics')file=path.join(temp,'custom_consumer-test_latest.ics');
   else if(url.pathname.startsWith('/output/')){
    const name=decodeURIComponent(url.pathname.slice('/output/'.length));
    if(path.basename(name)!==name)throw new Error('Outside output');
    file=path.join(output,name);
   }
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
 async function show(feed,date){await page.goto(`${base}/viewer?feed=${encodeURIComponent(feed)}&date=${date}`);await page.waitForFunction(()=>window.ready===true);}
 for(const [guide,language] of [['README.md','vi'],['README.en.md','en']]){
  await page.goto(base+'/'+guide);
  check(language+' README has only Vietnamese/English feed URLs', (await page.locator('pre code').first().textContent()).trim().endsWith('viet_lunar_latest.ics'));
  check(language+' shared cover loads',await page.locator('img[src="assets/lunar-calendar-cover.png"]').evaluate(img=>img.complete && img.naturalWidth>0));
  await page.screenshot({path:path.join(evidence,'readme-'+language+'.png')});
  await page.setViewportSize({width:390,height:844});
  check(language+' README fits mobile',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.screenshot({path:path.join(evidence,'readme-'+language+'-mobile.png')});
  await page.setViewportSize({width:1440,height:1050});
 }
 for(const [language,file] of [['vi','viet_lunar_latest.ics'],['en','viet_lunar_en_latest.ics'],['vi','viet_lunar_minimal_latest.ics'],['en','viet_lunar_en_minimal_latest.ics']]){
  await show('/output/'+file,displayMonth);
  check(language+' Tet is one all-day event',await page.locator(`.fc-daygrid-day[data-date="${tetDate}"] .fc-event`).count()===1);
  const title=await page.locator(`.fc-daygrid-day[data-date="${tetDate}"] .fc-event`).textContent();
  check(language+' localized Tet title',title.includes(language==='vi'?'T\u1ebft':'Lunar New Year'));
  await page.screenshot({path:path.join(evidence,'calendar-'+language+'.png')});
 }
 await show('/custom.ics',displayMonth);
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
  await zonePage.goto(`${base}/viewer?feed=/output/viet_lunar_en_latest.ics&date=${displayMonth}`);await zonePage.waitForFunction(()=>window.ready);
  const value=await zonePage.evaluate(uid=>window.calendar.getEvents().find(e=>e.id===uid).startStr,tet.id);
  assert.equal(value,tetDate,zone);await zoneContext.close();
 }
 check('Four browser timezones preserve the source all-day date, in the English Vietnamese feed');
 assert.deepEqual(errors,[]);check('No browser JavaScript errors');
 await fs.writeFile(path.join(evidence,'results.json'),JSON.stringify({status:'passed',feeds:inventory.length,events:totalEvents,checks,screenshots:'Browser-native capture; no pointer overlay',scope:'Local actual ICS + ICAL.js + FullCalendar. Not Google/Apple/Outlook subscription certification.'},null,2)+'\n');
 console.log(JSON.stringify({status:'passed',feeds:inventory.length,events:totalEvents,checks:checks.length,evidence},null,2));
}finally{
 if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));
 const resolvedTemp=path.resolve(temp);
 if(path.dirname(resolvedTemp)!==path.resolve(os.tmpdir()) || !path.basename(resolvedTemp).startsWith('lunar-consumer-'))throw new Error('Unsafe temporary cleanup target');
 await fs.rm(resolvedTemp,{recursive:true,force:true});
}
