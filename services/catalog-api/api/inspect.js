import { ApiError, authorize, cached, integer, respondError, upstream } from '../lib/runtime.js';
import { analyzePng } from '../lib/palette.js';

export default async function handler(req, res) {
  if (!authorize(req, res)) return;
  try {
    const id=integer(req.body.assetId,1,Number.MAX_SAFE_INTEGER);
    const result=await cached(`inspect:5:${id}`,3600000,async deadline=>{
      const [color,economy]=await Promise.allSettled([
        (async()=>{
          const thumb=await upstream(`https://thumbnails.roblox.com/v1/assets?assetIds=${id}&size=150x150&format=Png&isCircular=false`,deadline);
          const item=thumb?.data?.[0];
          if(item?.state!=='Completed' || typeof item.imageUrl!=='string') throw new ApiError(503,'THUMBNAIL_PENDING',2);
          const image=await upstream(item.imageUrl,deadline,{image:true,bytes:1048576});
          return analyzePng(image);
        })(),
        upstream(`https://economy.roblox.com/v2/assets/${id}/details`,deadline)
      ]);
      if(color.status==='rejected' && economy.status==='rejected') throw color.reason;
      const e=economy.status==='fulfilled'?economy.value:null;
      return {assetId:id,warna:color.status==='fulfilled'?color.value:null,nama:e?.Name||null,harga:e?.PriceInRobux??null,
        creator:e?.Creator?.Name||null,isLimited:Boolean(e?.IsLimited||e?.IsLimitedUnique),
        partial:color.status==='rejected'||economy.status==='rejected',diperiksaPada:new Date().toISOString()};
    });
    return res.status(200).json(result);
  } catch(err) { return respondError(res,err); }
}
