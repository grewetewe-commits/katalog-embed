import test from 'node:test';
import assert from 'node:assert/strict';
import { PNG } from 'pngjs';
import { authorize, cached, upstream, ApiError } from '../lib/runtime.js';
import { analyzePng } from '../lib/palette.js';
import catalog from '../api/catalog.js';

const secret = 'test-only-key-abcdefghijklmnopqrstuvwxyz';
process.env.API_SECRET = secret;
const res = () => ({code:200,headers:{},status(n){this.code=n;return this},setHeader(k,v){this.headers[k]=v},json(v){this.body=v;return this}});
const req = body => ({method:'POST',headers:{'x-api-secret':secret},body});
test('secret wajib dan environment yang kosong fail closed',()=>{
  const r=res(); assert.equal(authorize({...req({}),headers:{}},r),false);assert.equal(r.code,401);
  const original=process.env.API_SECRET;delete process.env.API_SECRET;
  const closed=res();assert.equal(authorize(req({}),closed),false);assert.equal(closed.code,503);process.env.API_SECRET=original;
});
test('method dan bentuk body divalidasi',()=>{
  const r=res();assert.equal(authorize({...req({}),method:'GET'},r),false);assert.equal(r.code,405);
  const b=res();assert.equal(authorize(req([]),b),false);assert.equal(b.code,400);
});
test('single-flight dan cache tidak menduplikasi kerja',async()=>{
  let count=0;
  const work=async()=>{count++;await new Promise(r=>setTimeout(r,5));return {ok:true}};
  const [a,b]=await Promise.all([cached('test-flight',1000,work),cached('test-flight',1000,work)]);
  assert.deepEqual(a,b);assert.equal(count,1);await cached('test-flight',1000,work);assert.equal(count,1);
});
test('pekerjaan gagal dapat dicoba lagi',async()=>{
  await assert.rejects(cached('test-retry',1000,()=>{throw new ApiError(503,'TEMPORARY')}));
  const value=await cached('test-retry',1000,()=>({ok:true}));assert.equal(value.ok,true);
});
test('URL sembarang dan PNG berukuran besar ditolak',async()=>{
  await assert.rejects(upstream('https://example.com',Date.now()+1000),e=>e.code==='INVALID_UPSTREAM');
  const b=Buffer.alloc(24);b.writeUInt32BE(0x89504e47);b.writeUInt32BE(0x0d0a1a0a,4);b.writeUInt32BE(10000,16);b.writeUInt32BE(10000,20);
  assert.throws(()=>analyzePng(b),e=>e.code==='PNG_DIMENSIONS');
});
test('pink pastel pada manekin abu tidak hilang',()=>{
  const png=new PNG({width:150,height:150});
  for(let i=0;i<png.data.length;i+=4){const colored=i/4%150>60&&i/4%150<80;png.data[i]=colored?240:145;png.data[i+1]=colored?208:145;png.data[i+2]=colored?220:145;png.data[i+3]=255;}
  const c=analyzePng(PNG.sync.write(png));assert.equal(c.namaTerdekat,'pink');assert.ok(c.porsiKromatik>0);
});
test('pink redup pada thumbnail hoodie tidak dilabeli merah',()=>{
  const png=new PNG({width:150,height:150});
  for(let i=0;i<png.data.length;i+=4){const colored=i/4%150>50&&i/4%150<85;png.data[i]=colored?201:145;png.data[i+1]=colored?181:145;png.data[i+2]=colored?185:145;png.data[i+3]=255;}
  assert.equal(analyzePng(PNG.sync.write(png)).namaTerdekat,'pink');
});
test('catalog menerima cursor resmi dan menolak input buruk',async()=>{
  const original=globalThis.fetch;
  let url;
  globalThis.fetch=async u=>{url=u;return new Response(JSON.stringify({data:[{id:999,itemType:'Asset',assetType:67,name:'Result'}],nextPageCursor:'cursor-2'}),{status:200,headers:{'content-type':'application/json'}})};
  try {
    const r=res();await catalog(req({keyword:'pink hoodie',cursor:'opaque:page1',limit:30}),r);
    assert.equal(r.code,200);assert.equal(r.body.nextPageCursor,'cursor-2');assert.equal(new URL(url).searchParams.get('Cursor'),'opaque:page1');
    const bad=res();await catalog(req({keyword:'x',limit:99999}),bad);assert.equal(bad.code,400);
  }finally{globalThis.fetch=original}
});
test('429 memakai Retry-After dan tidak menunggu melewati deadline',async()=>{
  const original=globalThis.fetch;let count=0;
  globalThis.fetch=async()=>{count++;return new Response('{}',{status:429,headers:{'retry-after':'60'}})};
  try {await assert.rejects(upstream('https://catalog.roblox.com/v2/search/items/details?Keyword=rate-test',Date.now()+1000),e=>e.status===429&&e.retryAfter===60);assert.equal(count,1)}finally{globalThis.fetch=original}
});
test('JSON rusak dan body terlalu besar tidak dianggap berhasil',async()=>{
  const original=globalThis.fetch;
  try{
    globalThis.fetch=async()=>new Response('not json',{status:200});await assert.rejects(upstream('https://catalog.roblox.com/v2/search/items/details?Keyword=bad-json',Date.now()+1000),e=>e.code==='UPSTREAM_JSON');
    globalThis.fetch=async()=>new Response('0123456789',{status:200});await assert.rejects(upstream('https://catalog.roblox.com/v2/search/items/details?Keyword=big-body',Date.now()+1000,{bytes:4}),e=>e.code==='UPSTREAM_SIZE');
  }finally{globalThis.fetch=original}
});
