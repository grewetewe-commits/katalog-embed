import { timingSafeEqual } from 'node:crypto';

export class ApiError extends Error {
  constructor(status, code, retryAfter = 0) { super(code); this.status = status; this.code = code; this.retryAfter = retryAfter; }
}
const cache = new Map();
const inflight = new Map();
let requests = 0;
const MAX_CACHE = 256;
export function authorize(req, res) {
  res.setHeader('Cache-Control', 'private, no-store');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  const expected = process.env.API_SECRET;
  const actual = req.headers?.['x-api-secret'];
  if (typeof expected !== 'string' || expected.length < 16) { res.status(503).json({ error: 'CONFIGURATION' }); return false; }
  if (typeof actual !== 'string' || actual.length > 256) { res.status(401).json({ error: 'UNAUTHORIZED' }); return false; }
  const a = Buffer.from(actual), b = Buffer.from(expected);
  if (a.length !== b.length || !timingSafeEqual(a, b)) { res.status(401).json({ error: 'UNAUTHORIZED' }); return false; }
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); res.status(405).json({ error: 'METHOD' }); return false; }
  if (Number(req.headers?.['content-length'] || 0) > 8192) { res.status(413).json({ error: 'BODY_TOO_LARGE' }); return false; }
  if (!req.body || typeof req.body !== 'object' || Array.isArray(req.body)) { res.status(400).json({ error: 'JSON_BODY' }); return false; }
  return true;
}
export function respondError(res, err) {
  const status = err instanceof ApiError ? err.status : 502;
  const code = err instanceof ApiError ? err.code : 'UPSTREAM';
  const retry = err instanceof ApiError ? err.retryAfter : 2;
  if (retry > 0) res.setHeader('Retry-After', String(retry));
  return res.status(status).json({ error: code, retryAfter: retry || undefined });
}
export function integer(value, min, max) {
  const n = Number(value);
  if (!Number.isSafeInteger(n) || n < min || n > max) throw new ApiError(400, 'INTEGER');
  return n;
}
export function shortString(value, max = 80) {
  if (value == null) return '';
  if (typeof value !== 'string' || value.length > max || /[\u0000-\u001f]/.test(value)) throw new ApiError(400, 'STRING');
  return value.trim();
}
export async function cached(key, ttl, work) {
  const now = Date.now();
  const c = cache.get(key);
  if (c && c.expires > now) return c.value;
  if (inflight.has(key)) return inflight.get(key);
  if (requests >= 8) throw new ApiError(503, 'BUSY', 2);
  requests++;
  const promise = (async () => {
    try {
      const value = await Promise.resolve().then(() => work(Date.now() + 11000));
      for (const [k, row] of cache) if (row.expires <= Date.now()) cache.delete(k);
      if (cache.size >= MAX_CACHE) cache.delete(cache.keys().next().value);
      cache.set(key, { value, expires: Date.now() + ttl });
      return value;
    } finally { requests--; inflight.delete(key); }
  })();
  inflight.set(key, promise);
  return promise;
}
function allowed(url, image) {
  const u = new URL(url);
  const hosts = new Set(['catalog.roblox.com', 'thumbnails.roblox.com', 'economy.roblox.com']);
  const cdn = u.hostname === 'rbxcdn.com' || u.hostname.endsWith('.rbxcdn.com');
  if (u.protocol !== 'https:' || u.username || u.password || u.port || !(image ? cdn : hosts.has(u.hostname))) throw new ApiError(502, 'INVALID_UPSTREAM');
  return u.href;
}
export async function upstream(url, deadline, { image = false, method = 'GET', body, bytes = 2097152 } = {}) {
  url = allowed(url, image);
  for (let attempt = 0; attempt < 3; attempt++) {
    const left = deadline - Date.now();
    if (left < 200) throw new ApiError(504, 'UPSTREAM_TIMEOUT', 2);
    let response;
    try {
      response = await fetch(url, { method, body, headers: body ? { 'content-type': 'application/json' } : undefined,
        redirect: 'error', signal: AbortSignal.timeout(Math.min(left, 3500)) });
    } catch {
      if (attempt === 2) throw new ApiError(504, 'UPSTREAM_TIMEOUT', 2);
    }
    if (response?.ok) {
      if (Number(response.headers.get('content-length') || 0) > bytes) throw new ApiError(502, 'UPSTREAM_SIZE');
      const reader = response.body.getReader();
      const chunks = []; let size = 0;
      try {
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          size += value.length;
          if (size > bytes) throw new ApiError(502, 'UPSTREAM_SIZE');
          chunks.push(value);
        }
      } finally { await reader.cancel().catch(() => {}); }
      const raw = Buffer.concat(chunks);
      if (image) return raw;
      try { return JSON.parse(raw.toString('utf8')); } catch { throw new ApiError(502, 'UPSTREAM_JSON'); }
    }
    if (response && response.status !== 429 && response.status < 500) throw new ApiError(response.status === 404 ? 404 : 502, 'UPSTREAM_REJECTED');
    const seconds = Number(response?.headers.get('retry-after'));
    const wait = Number.isFinite(seconds) && seconds > 0 ? seconds * 1000 : 300 * 2 ** attempt + Math.random() * 150;
    if (attempt === 2 || Date.now() + wait + 200 >= deadline) throw new ApiError(response?.status === 429 ? 429 : 503, 'UPSTREAM_BUSY', Math.max(1, Math.min(60, Math.ceil(wait / 1000))));
    await new Promise(resolve => setTimeout(resolve, wait));
  }
  throw new ApiError(503, 'UPSTREAM_BUSY', 2);
}
