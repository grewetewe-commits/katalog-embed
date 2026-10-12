import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {fromOutfitModel,fromLookRecord,safeId,collect,atomicJson} from './ready_outfits.mjs';
const avatar=()=>({id:'1234',playerAvatarType:'R15',scale:{height:1,width:1,depth:1,head:1,proportion:0,bodyType:0},bodyColors:Object.fromEntries(['head','torso','leftArm','rightArm','leftLeg','rightLeg'].map(k=>[k+'Color','ABC123'])),assets:[{id:10,assetType:{id:11}},{id:20,assetType:{id:12}},{id:30,assetType:{id:41}},{id:40,assetType:{id:67},meta:{order:3,puffiness:.25}},{id:50,assetType:{id:27}}]});
test('preserves full body, layering, colors and origin',()=>{
 const s=fromOutfitModel(avatar(),{kind:'marketplace_look',lookId:'8583456989219258653',outfitId:'1234'});
 assert.equal(s.BP.Torso,50);assert.equal(s.BP.LeftLeg,0);assert.deepEqual(s.SC,[1,1,1,1,0,0]);assert.equal(s.AM[40].Order,3);assert.equal(s.AM[40].Puffiness,.25);assert.equal(s.Origin.lookId,'8583456989219258653');assert.equal(s.BC[0],'ABC123');
});
test('dedup distinguishes body, color and layering',()=>{
 const a=avatar(),base=fromOutfitModel(a).H;a.assets.at(-1).id=51;assert.notEqual(fromOutfitModel(a).H,base);
 a.assets.at(-1).id=50;a.bodyColors.headColor='FFFFFF';assert.notEqual(fromOutfitModel(a).H,base);
 a.bodyColors.headColor='ABC123';a.assets[3].meta.order=4;assert.notEqual(fromOutfitModel(a).H,base);
});
test('unsafe IDs, missing scales/colors, malformed and incomplete avatars are rejected',()=>{
 assert.equal(safeId(9007199254740992),false);
 for(const alter of [a=>a.assets[0].id=9007199254740992,a=>delete a.scale.width,a=>a.scale.width=true,a=>delete a.bodyColors.headColor,a=>a.assets=[],a=>a.playerAvatarType='Unknown']){const a=avatar();alter(a);assert.throws(()=>fromOutfitModel(a));}
});
test('invalid transforms are discarded and large Look IDs remain exact strings',()=>{
 const a=avatar();a.assets[3].meta={order:101,puffiness:Infinity,position:[0,99,0]};assert.deepEqual(fromOutfitModel(a).AM[40],{});
 const id='8583456989219258653';const record={id,success:true,avatarSuccess:true,look:{lookId:id,outfitId:1234,lookType:'Avatar',moderationStatus:'Approved'},avatarDefinition:{outfitModel:a}};
 assert.equal(fromLookRecord(record).Origin.lookId,id);record.look.outfitId=4321;assert.throws(()=>fromLookRecord(record));
});
test('failed detail work remains durably queued; next creator page is resumed',async()=>{
 const root=await fs.mkdtemp(path.join(os.tmpdir(),'kp-ready-'));
 try{
  await atomicJson(path.join(root,'data/ready_outfit_sources.json'),{lookIds:[],creatorIds:['99']});
  await atomicJson(path.join(root,'data/ready_outfit_cursor.json'),{looks:{},creators:{'99':{token:'page2',completedAt:0}},pending:[{id:'1234',kind:'public_saved_outfit'}]});
  const calls=[];const reader={left:7,failures:[],async get(url){calls.push(url);this.left--;if(url.includes('/users/'))return {ok:true,data:{data:[{id:9999,isEditable:false,outfitType:'Avatar'}],paginationToken:'page3'}};return {ok:false,status:429};}};
  await collect({root,reader,maxRequests:7});
  const state=JSON.parse(await fs.readFile(path.join(root,'data/ready_outfit_cursor.json'),'utf8'));
  assert.deepEqual(state.pending,[{id:'1234',kind:'public_saved_outfit'}]);assert.equal(state.creators['99'].token,'page3');assert.ok(calls.some(u=>u.includes('paginationToken=page2')));
 }finally{await fs.rm(root,{recursive:true,force:true});}
});
test('successful public detail is imported once, expired IDs are retired',async()=>{
 const root=await fs.mkdtemp(path.join(os.tmpdir(),'kp-ready-'));
 try{
  await atomicJson(path.join(root,'data/ready_outfit_sources.json'),{lookIds:[],creatorIds:[]});
  await atomicJson(path.join(root,'data/ready_outfit_cursor.json'),{looks:{},creators:{},pending:[{id:'1234',kind:'public_saved_outfit'},{id:'1234',kind:'public_saved_outfit'},{id:'4321',kind:'public_saved_outfit'}]});
  const reader={left:7,failures:[],async get(url){this.left--;return url.includes('/4321/')?{ok:false,status:404}:{ok:true,data:{outfitModel:avatar()}};}};
  const r=await collect({root,reader,maxRequests:7});assert.equal(r.added,1);assert.equal(r.pending,0);assert.equal(r.total,1);
 }finally{await fs.rm(root,{recursive:true,force:true});}
});
