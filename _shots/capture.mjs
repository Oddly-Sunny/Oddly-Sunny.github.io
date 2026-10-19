// Usage: node capture.mjs <config.json>
// config: { url, origin, out, localStorage: {k: v|object}, preUrls?: [..], waitMs?, height?: 2578, hideSelectors?: [..], scrollY?: 0 }
// Opens origin, seeds localStorage, visits preUrls (e.g. QA ?sunnysideup), then url; saves 1280-wide JPG cropped to `height`.
import puppeteer from "puppeteer-core";
import fs from "fs";

const cfg = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const browser = await puppeteer.launch({
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: "new",
  args: ["--hide-scrollbars"],
});
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 900, deviceScaleFactor: 1 });
const origin = cfg.origin || new URL(cfg.url).origin;
await page.goto(origin, { waitUntil: "networkidle2", timeout: 60000 });
for (const u of cfg.preUrls || []) await page.goto(u, { waitUntil: "networkidle2", timeout: 60000 });
await page.evaluate((ls) => {
  for (const [k, v] of Object.entries(ls || {})) localStorage.setItem(k, typeof v === "string" ? v : JSON.stringify(v));
}, cfg.localStorage);
await page.goto(cfg.url, { waitUntil: "networkidle2", timeout: 60000 });
await new Promise((r) => setTimeout(r, cfg.waitMs ?? 3000));
// trigger lazy/reveal animations, then return to top
await page.evaluate(async () => {
  for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); }
  window.scrollTo(0, 0);
});
await new Promise((r) => setTimeout(r, 1500));
if (cfg.hideSelectors?.length) await page.addStyleTag({ content: cfg.hideSelectors.join(",") + "{display:none!important}" });
if (cfg.css) await page.addStyleTag({ content: cfg.css });
await new Promise((r) => setTimeout(r, 500));
const h = cfg.height || 2578;
await page.setViewport({ width: 1280, height: h, deviceScaleFactor: 1 });
await new Promise((r) => setTimeout(r, 1500));
await page.screenshot({ path: cfg.out, type: "jpeg", quality: 82, clip: { x: 0, y: cfg.scrollY || 0, width: 1280, height: h } });
if (cfg.dumpLocalStorage) console.log(JSON.stringify(await page.evaluate(() => Object.fromEntries(Object.entries(localStorage))), null, 1).slice(0, 4000));
await browser.close();
console.log("saved", cfg.out);
