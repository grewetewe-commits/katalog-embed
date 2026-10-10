import { PNG } from 'pngjs';
import { ApiError } from './runtime.js';

const NAMES = [['merah', 0], ['oranye', 30], ['kuning', 55], ['hijau', 130], ['cyan', 185], ['biru', 235], ['ungu', 280], ['pink', 335]];
export function hsl(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r,g,b), min = Math.min(r,g,b), d = max - min, l = (max + min) / 2;
  if (!d) return [0, 0, l];
  const s = d / (1 - Math.abs(2*l - 1));
  let h = max === r ? ((g-b)/d)%6 : max === g ? (b-r)/d+2 : (r-g)/d+4;
  h *= 60; if (h < 0) h += 360;
  return [h,s,l];
}
export function analyzePng(buffer) {
  if (buffer.length < 24 || buffer.readUInt32BE(0) !== 0x89504e47 || buffer.readUInt32BE(4) !== 0x0d0a1a0a) throw new ApiError(502, 'PNG_FORMAT');
  const width = buffer.readUInt32BE(16), height = buffer.readUInt32BE(20);
  if (width < 1 || height < 1 || width > 512 || height > 512) throw new ApiError(502, 'PNG_DIMENSIONS');
  let png;
  try { png = PNG.sync.read(buffer); } catch { throw new ApiError(502, 'PNG_DECODE'); }
  const bins = Array.from({length:36},()=>({weight:0,n:0,r:0,g:0,b:0,s:0,l:0,sin:0,cos:0}));
  const neutral = Array.from({length:4},()=>({n:0,r:0,g:0,b:0}));
  let total=0, colored=0;
  const corners = [0, (width-1)*4, (height-1)*width*4, (width*height-1)*4].map(i=>[...png.data.subarray(i,i+4)]);
  const opaque = corners.every(p=>p[3]>=200);
  const bg = opaque && corners.every(p=>Math.hypot(p[0]-corners[0][0],p[1]-corners[0][1],p[2]-corners[0][2])<15) ? corners[0] : null;
  for(let i=0;i<png.data.length;i+=4) {
    const [r,g,b,a] = png.data.subarray(i,i+4);
    if(a<100 || (bg && Math.hypot(r-bg[0],g-bg[1],b-bg[2])<20)) continue;
    total++;
    const [h,s,l]=hsl(r,g,b);
    if(s<0.08 || l<0.12 || l>0.97) {
      const bin=neutral[l<0.14?0:l>0.90?1:l>0.65?2:3];
      bin.n++; bin.r+=r; bin.g+=g; bin.b+=b; continue;
    }
    colored++;
    const w=s*(1-Math.abs(2*l-1)), rad=h*Math.PI/180, bin=bins[Math.floor(h/10)%36];
    bin.n++; bin.weight+=w; bin.r+=r*w; bin.g+=g*w; bin.b+=b*w; bin.s+=s*w; bin.l+=l*w; bin.sin+=Math.sin(rad)*w; bin.cos+=Math.cos(rad)*w;
  }
  if(!total) throw new ApiError(502,'PNG_EMPTY');
  const clusters = bins.map((_,i)=>[(i+35)%36,i,(i+1)%36].reduce((a,k)=>{ const b=bins[k]; for(const key of Object.keys(a))a[key]+=b[key]; return a; },{weight:0,n:0,r:0,g:0,b:0,s:0,l:0,sin:0,cos:0})).sort((a,b)=>b.weight-a.weight);
  const top=clusters[0];
  let rgb, name, hue=null, saturation=0, light=0, limited=false;
  if(colored/total>=0.025 && top.weight>0 && top.n>=12) {
    hue=(Math.atan2(top.sin,top.cos)*180/Math.PI+360)%360;
    saturation=top.s/top.weight; light=top.l/top.weight;
    rgb=[top.r,top.g,top.b].map(v=>Math.round(v/top.weight));
    name=[...NAMES].sort((a,b)=>Math.min(Math.abs(a[1]-hue),360-Math.abs(a[1]-hue))-Math.min(Math.abs(b[1]-hue),360-Math.abs(b[1]-hue)))[0][0];
    // Pink terang dan redup tetap dekat hue merah; lightness membedakannya.
    if ((hue >= 320 || hue <= 12) && light >= 0.65 && saturation < 0.75) name='pink';
    limited=colored/total<0.12;
  } else {
    const topNeutral=neutral.map((b,i)=>({...b,i})).sort((a,b)=>b.n-a.n)[0];
    if(!topNeutral.n) throw new ApiError(502,'PNG_COLOR_UNCERTAIN');
    rgb=[topNeutral.r,topNeutral.g,topNeutral.b].map(v=>Math.round(v/topNeutral.n));
    name=['hitam','putih','abu-abu terang','abu-abu'][topNeutral.i]; light=hsl(...rgb)[2];
  }
  return {namaTerdekat:name,namaSekunder:null,hex:'#'+rgb.map(v=>v.toString(16).padStart(2,'0')).join(''),rgb,
    hueDerajat:hue==null?null:Math.round(hue),saturasi:Number(saturation.toFixed(3)),kecerahan:Number(light.toFixed(3)),
    porsiKromatik:Number((colored/total).toFixed(3)),polaVisual:'belum dinilai',versi:5,evidence:limited?'warna sedikit; perlu nama/render':'thumbnail'};
}
