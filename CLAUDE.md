# oddlysunny.com

Static site on GitHub Pages (push `main` to deploy). Edtech-studio redesign (Oct 2026), Superside-reference layout; per-section data-scheme (green/purple/ember dark, cream/tan light).

- Pages are GENERATED: edit `_build/build.py` (copy, product data, templates), then `python3 _build/build.py`. Outputs `index.html`, `work/index.html`, `work/<slug>/index.html`.
- Shared `assets/site.css` and `assets/site.js` (includes GA4 + cookie consent; GA is skipped on localhost). Bump `?v=` in build.py when CSS/JS change.
- Banners in `assets/img/` (7 jpgs, 1800px).
- Preview: `python3 -m http.server 8000` from repo root.
- Rules: always "we", never "I"; no personal info (no names, home address); no em-dashes; brand mark 4 cells with yellow cell nudging.
- Do not touch `privacy/`, `cookie-settings/`, `*-terms/`, `dmv-iq-privacy/`.
- Store links come from the memory file portfolio-store-urls; Insurance Pass has no app yet (Aviator IQ is live on iOS + Android; Airwaves IQ and Mariner IQ are live on Android, Mariner on Google Play since 2026-10-28) (add to `apps` in build.py when they ship).
- Preview note: plain `python3 -m http.server` does not support HTTP Range requests, so the looping video in the personal section will not load; use a range-capable server (or just test on GitHub Pages).
- Product page story copy lives in `_build/stories.py` (one entry per product: headline, dek, caption, body of paragraphs / subheads / pull quotes). Product pages use the light "paper" scheme and a scroll-scaling hero image (see end of `assets/site.js`).
- Contact form posts to the Cloud Run service `oddlysunny-contact` (project dmv-iq, us-central1; source in `_contact-service/`, key in Secret Manager `oddlysunny-resend-key`). Redeploy: `cd _contact-service && gcloud run deploy oddlysunny-contact --project dmv-iq --region us-central1 --source .` (set CLOUDSDK_PYTHON=/opt/homebrew/bin/python3.12).
- Homepage games (Play section) run from `assets/site.js` (search "playable mini games"); their data is `PLAY_JSON` in build.py, sign art in `assets/img/signs/` (real MUTCD SVGs from dmviq-website). Only use facts true in every state.
- /sunny demo cards: `SUNNY_WIDGET_CASES` + `sunny_widget()` in build.py are written examples of Sunny's real card types (quiz, course, progress); `sunny_examples.json` holds the real transcripts.
- Product page screenshots: recapture with `_shots/` (see its README); Pro + seeded progress on the live sites. Configs can `clicks` buttons by text (Drive IQ CA opens Sunny and asks a starter question: the reply is live output, so it changes per run).
- Product page games section: `games_block(p)` + `GAME_SETS` in build.py; clips per product in `assets/img/games/` (DMV IQ) or `assets/img/games/<slug>/`.
- Header menu is "Stories" (story headlines from stories.py, app icons in `assets/img/apps/`). Keep the dropdown light.
- Git gotcha: a sync tool once created `.git/refs/heads/main (1)` and broke `git fetch`; move such files out of `.git`.
