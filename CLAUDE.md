# oddlysunny.com

Static site on GitHub Pages (push `main` to deploy). Edtech-studio redesign (Oct 2026), Superside-reference layout; per-section data-scheme (green/purple/ember dark, cream/tan light).

- Pages are GENERATED: edit `_build/build.py` (copy, product data, templates), then `python3 _build/build.py`. Outputs `index.html`, `work/index.html`, `work/<slug>/index.html`.
- Shared `assets/site.css` and `assets/site.js` (includes GA4 + cookie consent; GA is skipped on localhost). Bump `?v=` in build.py when CSS/JS change.
- Banners in `assets/img/` (7 jpgs, 1800px).
- Preview: `python3 -m http.server 8000` from repo root.
- Rules: always "we", never "I"; no personal info (no names, home address); no em-dashes; brand mark 4 cells with yellow cell nudging.
- Do not touch `privacy/`, `cookie-settings/`, `*-terms/`, `dmv-iq-privacy/`.
- Store links come from the memory file portfolio-store-urls; Aviator IQ, Insurance Pass, Airwaves IQ, Mariner IQ have no apps yet (add to `apps` in build.py when they ship).
