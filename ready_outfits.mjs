// Public Roblox data only. Look identifiers remain strings (some exceed 2^53).
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {createHash} from 'node:crypto';

const ACCESSORY = {8:1,41:2,42:3,43:4,44:5,45:6,46:7,47:8,64:9,65:10,66:11,67:12,68:13,69:14,70:15,71:16,72:17,76:18,77:19};
const BODY = {17:'Head',79:'Head',27:'Torso',28:'RightArm',29:'LeftArm',30:'LeftLeg',31:'RightLeg'};
const PARTS = ['Head','Torso','LeftArm','RightArm','LeftLeg','RightLeg'];
const SCALES = ['height','width','depth','head','proportion','bodyType'];
export const safeId = x => Number.isSafeInteger(x) && x > 0;
const lookId = x => typeof x === 'string' && /^[1-9]\d{0,19}$/.test(x);
const finite = x => typeof x === 'number' && Number.isFinite(x);
export function hashCanonical(text) {
  let a=5381,b=52711;
  for(const byte of Buffer.from(text,'utf8')) { a=(a*131+byte)%4294967291; b=(b*137+byte)%4294967279; }
  return a.toString(16).padStart(8,'0')+b.toString(16).padStart(8,'0');
}
function transform(meta) {
  const out={};
  if(Number.isInteger(meta?.order) && meta.order>=0 && meta.order<=100) out.Order=meta.order;
  if(finite(meta?.puffiness) && meta.puffiness>=0 && meta.puffiness<=1) out.Puffiness=meta.puffiness;
  for(const [key,source,lo,hi] of [['Pos','position',-1.5,1.5],['Rot','rotation',-180,180],['Scl','scale',0.4,2]]) {
    const v=meta?.[source];
    const xyz=Array.isArray(v)?v:[v?.x??v?.X,v?.y??v?.Y,v?.z??v?.Z];
    if(xyz.length===3 && xyz.every(x=>finite(x)&&x>=lo&&x<=hi)) out[key]=xyz;
  }
  return out;
}
export function fromOutfitModel(model, origin={kind:'public_saved_outfit'}) {
  if(!model || !Array.isArray(model.assets) || model.assets.length>80 || !['R6','R15'].includes(model.playerAvatarType)) throw Error('Invalid avatar definition');
  if(!SCALES.every((k,i)=>finite(model.scale?.[k]) && model.scale[k]>=0 && model.scale[k]<=2 && (i>=4||model.scale[k]>0))) throw Error('Incomplete avatar scales');
  const seed={S:origin.kind,R:model.playerAvatarType,A:[],AM:{},BP:Object.fromEntries(PARTS.map(k=>[k,0])),SC:SCALES.map(k=>model.scale[k]),BC:[],Origin:origin};
  const seen=new Set();
  for(const asset of model.assets) {
    const id=asset.id,type=asset.assetType?.id;
    if(!safeId(id)||!Number.isInteger(type)) throw Error('Invalid asset ID/type');
    if(seen.has(id)) continue;
    seen.add(id);
    if(BODY[type]) seed.BP[BODY[type]]=id;
    else if(type===11) seed.Sh=id;
    else if(type===12) seed.Pa=id;
    else if(type===2) seed.Gt=id;
    else if(type===18) seed.F=id;
    else if(ACCESSORY[type]) { seed.A.push([id,ACCESSORY[type]]); seed.AM[id]=transform(asset.meta); }
  }
  if(seed.A.length>20 || seed.A.length+Number(!!seed.Sh)+Number(!!seed.Pa)+Number(!!seed.Gt)<3) throw Error('Insufficient outfit composition');
  if(!seed.Sh&&!seed.Pa&&!seed.A.some(a=>a[1]>=9&&a[1]<=17)) throw Error('Avatar has no clothing');
  for(const part of PARTS) {
    const hex=model.bodyColors?.[part[0].toLowerCase()+part.slice(1)+'Color'];
    if(typeof hex!=='string'||!/^[a-fA-F0-9]{6}$/.test(hex)) throw Error('Incomplete body colors');
    seed.BC.push(hex.toUpperCase());
  }
  seed.A.sort((a,b)=>a[1]-b[1]||a[0]-b[0]);
  // Include face, exact original body and layering in dedup; matching items may have different fits.
  const canon=[seed.Sh||0,seed.Pa||0,seed.Gt||0,seed.F||0,...seed.A.map(a=>a.join(':')),JSON.stringify(seed.BP),seed.SC.join(','),seed.BC.join(','),seed.R,JSON.stringify(seed.AM)].join('|');
  seed.H=hashCanonical(canon);
  return seed;
}
export function fromLookRecord(record) {
  const look=record.look;
  if(!record.success||!record.avatarSuccess||!lookId(String(record.id))||look?.lookId!==String(record.id)||!safeId(look.outfitId)) throw Error('Unverified Look record');
  if(String(record.avatarDefinition?.outfitModel?.id)!==String(look.outfitId)||look.lookType!=='Avatar'||look.moderationStatus!=='Approved') throw Error('Look/avatar mismatch');
  const creatorHash=look.curator?.id?createHash('sha256').update('roblox-user:'+look.curator.id).digest('hex'):undefined;
  return fromOutfitModel(record.avatarDefinition.outfitModel,{kind:'marketplace_look',lookId:look.lookId,outfitId:String(look.outfitId),...(creatorHash?{creatorHash}:{})});
}
export async function atomicJson(filename,data) {
  await fs.mkdir(path.dirname(filename),{recursive:true});
  const tmp=filename+'.tmp';
  await fs.writeFile(tmp,JSON.stringify(data)+'\n');
  await fs.rename(tmp,filename);
}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
class PublicReader {
  constructor(maxRequests=90,deadlineMs=12*60*1000) { this.left=maxRequests;this.deadline=Date.now()+deadlineMs;this.next=0;this.failures=[]; }
  async get(url) {
    if(!/^https:\/\/(avatar\.roblox\.com|apis\.roblox\.com)\//.test(url)) throw Error('Unexpected API destination');
    for(let attempt=0;attempt<3;attempt++) {
      if(this.left<=0||Date.now()>=this.deadline) return {ok:false,deferred:true};
      await sleep(Math.max(0,this.next-Date.now()));
      this.left--;this.next=Date.now()+4000;
      try {
        const response=await fetch(url,{signal:AbortSignal.timeout(20000),headers:{'User-Agent':'KatalogPraktis-PublicOutfits/1.0'},redirect:'error'});
        if(response.ok) return {ok:true,data:await response.json()};
        this.failures.push({url,status:response.status});
        if([401,403,404].includes(response.status)) return {ok:false,status:response.status};
        const retry=Number(response.headers.get('retry-after'));
        const delay=response.status===429?Math.max(60000,Number.isFinite(retry)?Math.min(retry*1000,180000):0):Math.min(30000,2000*2**attempt);
        this.next=Math.max(this.next,Date.now()+delay);
      } catch(e) { this.failures.push({url,error:String(e.name)}); this.next=Math.max(this.next,Date.now()+4000*2**attempt); }
    }
    return {ok:false};
  }
}
async function readJson(filename,fallback) { try{return JSON.parse(await fs.readFile(filename,'utf8'));}catch(e){if(e.code==='ENOENT')return fallback;throw e;} }
export async function collect({root='.',maxRequests=90,deadlineMs=720000,reader:providedReader}={}) {
  const bankPath=path.join(root,'bank/ready_outfits.json'), statePath=path.join(root,'data/ready_outfit_cursor.json');
  const bank=await readJson(bankPath,{schema:1,version:0,seeds:[],meta:{}});
  const input=await readJson(path.join(root,'data/ready_outfit_sources.json'),{lookIds:[],creatorIds:[]});
  const state=await readJson(statePath,{creators:{},pending:[],looks:{}});
  if(bank.schema!==1||!Array.isArray(bank.seeds)||!Array.isArray(input.lookIds)||!Array.isArray(input.creatorIds)) throw Error('Invalid collection files');
  state.creators??={}; state.pending??=[]; state.looks??={};
  const reader=providedReader??new PublicReader(maxRequests,deadlineMs), seeds=new Map(bank.seeds.map(s=>[s.H,s]));
  let added=0;
  const checkpoint=async()=>{
    const out={...bank,schema:1,version:Math.floor(Date.now()/1000),seeds:[...seeds.values()].slice(-4000),fetchedAtUtc:new Date().toISOString()};
    await atomicJson(bankPath,out);await atomicJson(statePath,state);
  };
  // Resolve IDs only from actual supplied discovery records. Never enumerate guessed Look IDs.
  let refreshedLooks=0;
  for(const id of input.lookIds) {
    if(!lookId(id)) throw Error('Look IDs must be decimal strings');
    if(state.looks[id]&&Date.now()-state.looks[id]<86400000) continue;
    if(refreshedLooks>=Math.min(20,Math.floor(maxRequests/4))) break;
    refreshedLooks++;
    const r=await reader.get('https://apis.roblox.com/look-api/v2/looks/'+id);
    if(r.deferred) break;
    if(!r.ok) continue;
    const look=r.data.look;
    if(look?.lookId!==id||!safeId(look.outfitId)||look.lookType!=='Avatar'||look.moderationStatus!=='Approved') continue;
    if(!state.pending.some(x=>x.lookId===id)) state.pending.push({id:String(look.outfitId),lookId:id,kind:'marketplace_look'});
    for(const item of look.items||[]) if(item.itemType==='Asset'&&safeId(item.id)&&Number.isInteger(item.assetType)) bank.meta[item.id]={n:item.name,t:item.assetType,p:item.priceInRobux,s:item.isPurchasable===true?1:0,c:item.creator?.name||'',w:Math.floor(Date.now()/1000)};
    state.looks[id]=Date.now();
    await checkpoint();
  }
  // First consume pending detail work: continuing pagination must not lose previously discovered IDs.
  const consume=async()=>{
    let remaining=state.pending.length;
    while(state.pending.length && remaining-->0) {
      const item=state.pending[0];
      if(!/^\d{1,16}$/.test(item.id)||!safeId(Number(item.id))) {state.pending.shift();continue;}
      const r=await reader.get('https://avatar.roblox.com/v4/outfits/'+item.id+'/details');
      if(r.deferred) break;
      state.pending.shift();
      if(!r.ok) { if(![403,404].includes(r.status))state.pending.push(item);await checkpoint();continue; }
      try {
        if(String(r.data.outfitModel?.id)!==item.id) throw Error('Outfit ID mismatch');
        const seed=fromOutfitModel(r.data.outfitModel,{kind:item.kind,outfitId:item.id,...(item.lookId?{lookId:item.lookId}:{}),...(item.creatorHash?{creatorHash:item.creatorHash}:{})});
        if(!seeds.has(seed.H)){seeds.set(seed.H,seed);added++;}
      } catch(e) {reader.failures.push({outfitId:item.id,error:e.message});}
      await checkpoint();
    }
  };
  await consume();
  const creatorIds=input.creatorIds;
  const start=Number.isInteger(state.creatorIndex)?state.creatorIndex%Math.max(1,creatorIds.length):0;
  for(let offset=0;offset<creatorIds.length;offset++) {
    const index=(start+offset)%creatorIds.length,uid=creatorIds[index];
    if(typeof uid!=='string'||!/^\d{1,16}$/.test(uid)||!safeId(Number(uid))) throw Error('Invalid public creator ID');
    const cursor=state.creators[uid]||{token:'',completedAt:0};
    if(cursor.completedAt&&Date.now()-cursor.completedAt<7*86400000)continue;
    if(cursor.completedAt){cursor.token='';cursor.completedAt=0;}
    const url='https://avatar.roblox.com/v2/avatar/users/'+uid+'/outfits'+(cursor.token?'?paginationToken='+encodeURIComponent(cursor.token):'');
    const r=await reader.get(url);
    if(r.deferred) break;
    state.creatorIndex=(index+1)%Math.max(1,creatorIds.length);
    if(!r.ok||!Array.isArray(r.data.data)||typeof r.data.paginationToken!=='string'){await checkpoint();continue;}
    if(r.data.paginationToken&&r.data.paginationToken===cursor.token) {reader.failures.push({userId:uid,error:'Repeated pagination token'});continue;}
    for(const item of r.data.data) if(item.isEditable===true&&item.outfitType==='Avatar'&&safeId(item.id)&&state.pending.length<1000&&!state.pending.some(x=>x.id===String(item.id))) state.pending.push({id:String(item.id),kind:'public_saved_outfit',creatorHash:createHash('sha256').update('roblox-user:'+uid).digest('hex')});
    cursor.token=r.data.paginationToken;
    if(!cursor.token)cursor.completedAt=Date.now();
    state.creators[uid]=cursor;
    await checkpoint();
    await consume();
  }
  await checkpoint();
  const report={added,total:seeds.size,pending:state.pending.length,requests:maxRequests-reader.left,failures:reader.failures,scope:'observed public outfits; not the global Marketplace total'};
  await atomicJson(path.join(root,'data/ready_outfit_report.json'),report);
  console.log(JSON.stringify({...report,failures:report.failures.length}));
  return report;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) await collect();
