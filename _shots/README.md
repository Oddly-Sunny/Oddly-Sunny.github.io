# Product page screenshots

Sources for `assets/img/shots/*-d.jpg` (the browser window on each /work/ page). Each config opens the live site in headless Chrome, turns on Pro with the site's `?sunnysideup` QA flag, seeds localStorage with a learner about two-thirds through (real question IDs; the site computes every number itself), and saves a 1280 x 2578 JPG.

    npm install
    node capture.mjs dmv-iq.json

Answer timestamps are fixed, so "days left" and streaks drift as time passes; regenerate the seed data before a recapture if that matters. Bump `?v=` on the shot URL in `stage()` in build.py after replacing images.
