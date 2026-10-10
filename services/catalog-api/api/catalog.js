import { ApiError, authorize, cached, integer, respondError, shortString, upstream } from '../lib/runtime.js';

export default async function handler(req, res) {
  if (!authorize(req, res)) return;
  try {
    const b = req.body;
    const action = shortString(b.action || 'search', 20);
    if (action === 'asset') {
      const id = integer(b.assetId, 1, Number.MAX_SAFE_INTEGER);
      const value = await cached(`asset:${id}`, 60000, deadline => upstream(`https://economy.roblox.com/v2/assets/${id}/details`, deadline));
      return res.status(200).json(value);
    }
    if (action === 'assetBundles') {
      const id = integer(b.assetId, 1, Number.MAX_SAFE_INTEGER);
      const cursor = b.cursor == null ? null : integer(b.cursor, 1, Number.MAX_SAFE_INTEGER);
      const url = new URL(`https://catalog.roblox.com/v1/assets/${id}/bundles`);
      if (cursor) url.searchParams.set('cursor', String(cursor));
      const value = await cached(url.href, 300000, deadline => upstream(url.href, deadline));
      return res.status(200).json(value);
    }
    if (action === 'bundle') {
      const id = integer(b.bundleId, 1, Number.MAX_SAFE_INTEGER);
      const value = await cached(`bundle:${id}`, 300000, deadline => upstream(`https://catalog.roblox.com/v1/bundles/${id}/details`, deadline));
      return res.status(200).json(value);
    }
    if (action !== 'search') throw new ApiError(400, 'ACTION');
    const q = shortString(b.keyword);
    const cursor = shortString(b.cursor, 2048);
    const limit = b.limit == null ? 30 : integer(b.limit, 10, 120);
    if (![10, 28, 30, 60, 120].includes(limit)) throw new ApiError(400, 'LIMIT');
    const url = new URL('https://catalog.roblox.com/v2/search/items/details');
    url.searchParams.set('Keyword', q); url.searchParams.set('Limit', String(limit));
    if (cursor) url.searchParams.set('Cursor', cursor);
    if (b.category != null) url.searchParams.set('Category', String(integer(b.category, 1, 17)));
    if (b.sortType != null) url.searchParams.set('SortType', String(integer(b.sortType, 0, 7)));
    if (b.minPrice != null) url.searchParams.set('MinPrice', String(integer(b.minPrice, 0, 2147483647)));
    if (b.maxPrice != null) url.searchParams.set('MaxPrice', String(integer(b.maxPrice, 0, 2147483647)));
    if (b.minPrice != null && b.maxPrice != null && Number(b.minPrice) > Number(b.maxPrice)) throw new ApiError(400, 'PRICE_RANGE');
    const value = await cached(url.href, 30000, deadline => upstream(url.href, deadline));
    if (!Array.isArray(value.data)) throw new ApiError(502, 'CATALOG_SCHEMA');
    return res.status(200).json({ data: value.data, nextPageCursor: value.nextPageCursor || null, previousPageCursor: value.previousPageCursor || null, source: 'ROBLOX', fetchedAt: Date.now() });
  } catch (err) { return respondError(res, err); }
}
