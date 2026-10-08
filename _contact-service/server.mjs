// Tiny contact endpoint for oddlysunny.com. Sends one email through Resend. No dependencies.
import http from 'node:http';

const PORT = process.env.PORT || 8080;
const KEY = process.env.RESEND_API_KEY || '';
const TO = process.env.CONTACT_TO || 'hello@oddlysunny.com';
const FROM = process.env.CONTACT_FROM || 'Oddly Sunny <hello@oddlysunny.com>';
const DRY = process.env.DRY_RUN === '1';
const ORIGINS = new Set(['https://oddlysunny.com', 'https://www.oddlysunny.com', 'http://localhost:8000', 'http://127.0.0.1:8000']);
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const hits = new Map(); // ip -> [timestamps]

const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
function limited(ip) {
  const now = Date.now(), win = (hits.get(ip) || []).filter((t) => now - t < 3600e3);
  win.push(now); hits.set(ip, win);
  return win.length > 5;
}
function send(res, code, obj, origin) {
  const h = { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', Vary: 'Origin' };
  if (origin && ORIGINS.has(origin)) { h['Access-Control-Allow-Origin'] = origin; h['Access-Control-Allow-Methods'] = 'POST, OPTIONS'; h['Access-Control-Allow-Headers'] = 'Content-Type'; }
  res.writeHead(code, h); res.end(JSON.stringify(obj));
}

http.createServer(async (req, res) => {
  const origin = req.headers.origin || '';
  if (req.method === 'OPTIONS') return send(res, 204, {}, origin);
  if (req.url === '/healthz') return send(res, 200, { ok: true }, origin);
  if (req.method !== 'POST') return send(res, 405, { error: 'Method not allowed' }, origin);
  if (origin && !ORIGINS.has(origin)) return send(res, 403, { error: 'Forbidden' }, origin);
  try {
    let raw = '';
    for await (const chunk of req) { raw += chunk; if (raw.length > 20000) return send(res, 413, { error: 'Too large' }, origin); }
    const body = JSON.parse(raw || '{}');
    if (body.website) return send(res, 200, { ok: true }, origin); // honeypot
    const name = String(body.name || '').trim().slice(0, 120), email = String(body.email || '').trim().slice(0, 200), message = String(body.message || '').trim();
    if (!name || !EMAIL_RE.test(email) || !message) return send(res, 400, { error: 'Please add your name, a valid email and a message.' }, origin);
    if (message.length > 5000) return send(res, 400, { error: 'That message is a little long, please trim it.' }, origin);
    const ip = String(req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim();
    if (limited(ip)) return send(res, 429, { error: 'Too many messages. Please try again later.' }, origin);
    const mail = {
      from: FROM, to: [TO], reply_to: email, subject: `Contact form: ${name}`.slice(0, 150),
      text: `${message}\n\n--\n${name} <${email}>\nSent from oddlysunny.com contact form`,
      html: `<p style="white-space:pre-wrap;font:15px/1.6 system-ui">${esc(message)}</p><hr><p style="font:13px system-ui;color:#555">${esc(name)} &lt;${esc(email)}&gt;<br>Sent from the oddlysunny.com contact form</p>`,
    };
    if (DRY) { console.log('[dry-run]', JSON.stringify(mail)); return send(res, 200, { ok: true, dry: true }, origin); }
    if (!KEY) { console.error('RESEND_API_KEY missing'); return send(res, 500, { error: 'Something went wrong. Please email us directly.' }, origin); }
    const r = await fetch('https://api.resend.com/emails', { method: 'POST', headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' }, body: JSON.stringify(mail) });
    if (!r.ok) { console.error('resend', r.status, await r.text()); return send(res, 502, { error: 'Something went wrong. Please email us directly.' }, origin); }
    return send(res, 200, { ok: true }, origin);
  } catch (e) {
    console.error(e); return send(res, 500, { error: 'Something went wrong. Please email us directly.' }, origin);
  }
}).listen(PORT, () => console.log('contact service on', PORT));
