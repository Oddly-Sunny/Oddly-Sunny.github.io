#!/usr/bin/env python3
"""Builds the oddlysunny.com static pages. Run from repo root: python3 _build/build.py
Writes index.html, work/index.html and work/<slug>/index.html. Edit copy here, not in the output."""
import os, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIL = "hello@oddlysunny.com"

APPLE = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.4 12.6c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9-.7 0-1.8-.8-3-.8-1.5 0-3 .9-3.800 2.300-1.600 2.800-.4 7 1.200 9.300.8 1.100 1.700 2.400 2.900 2.300 1.200 0 1.600-.7 3-.7s1.800.7 3 .7c1.300 0 2.100-1.100 2.800-2.200.9-1.300 1.300-2.500 1.300-2.600-.1 0-2.500-1-2.500-3.900zM14.200 5.800c.6-.8 1.100-1.800.9-2.800-.9 0-2 .6-2.700 1.400-.6.700-1.100 1.800-.9 2.700 1 .1 2-.5 2.700-1.300z"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.600 2.300c-.3.300-.5.800-.5 1.400v16.600c0 .6.200 1.100.5 1.400l.1.100 9.300-9.300v-.2L3.700 2.200l-.1.100zm12.400 12.500-3.100-3.100v-.2l3.100-3.100 3.700 2.100c1.100.6 1.100 1.600 0 2.200l-3.700 2.100zm-.1-.1L12.800 11.600 3.700 20.700c.4.400.9.400 1.600.1l10.600-6.100zm0-5.400L5.300 3.200c-.7-.4-1.200-.3-1.600.1l9.100 9.100 3.100-3.100z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'

# ------------------------------------------------------------------ products
# status "live" = site is up. apps: list of (label, url) with label "ios"/"android"
PRODUCTS = [
 dict(slug="aviator-iq", name="Aviator IQ", url="https://aviator-iq.com", host="aviator-iq.com",
  cat=["aviation"], catlabel="Aviation", accent="#E8B86A", tint="#241B12",
  tag="FAA knowledge test prep for every airman certificate.",
  short="Thirteen FAA exams, one calm place to study. Questions tied to the official handbooks, with the real testing figures.",
  title=("Aviator ", "IQ"),
  lede="FAA knowledge test prep for every airman certificate. Practice that points straight back to the handbooks, the ACS and the official testing figures, so you don't just pass, you actually get it.",
  what="FAA exams",
  over=[
   "Aviation exams have a reputation: huge handbooks, cryptic charts, and prep tools that look like they were built in 2004. We thought that was a very fixable problem.",
   "Aviator IQ covers <strong>13 FAA knowledge exams</strong>, from Private Pilot to ATP. Every question is mapped to the source it comes from, and the figures you'll see on test day (yes, the sectional charts) sit right next to the question.",
   "Then there's the part we're proudest of: an <strong>IQ Readiness Score</strong> that blends coverage, accuracy, recall and speed, so you know when you're ready instead of guessing.",
  ],
  facts=[("13","FAA exams covered"),("ACS","every question mapped to the standards"),("0-100","readiness score that tells you when to book")],
  feats=[("Official figures, in context","Charts and test figures load right alongside the question, the way they appear on exam day."),
         ("Handbook-linked answers","Explanations point back to the FAA handbook chapter, so one wrong answer turns into one solid lesson."),
         ("A readiness score you can trust","Mastery, not vibes. It moves when you learn, and it won't flatter you."),
         ("Study guides and tools","A growing library of study guides, a test code lookup, and a pass-rate index built from real FAA data."),
         ("Practice modes that fit your week","Quick sets, topic drills, full simulator runs. Ten minutes or two hours, you pick."),
         ("Built for the checkride path","Written for the student pilot, the CFI refreshing, and the airline hopeful alike.")],
  apps=[], appnote="Web today. The mobile app is in the works.",
  img="aviator-iq.jpg", alt="Aviator IQ on a laptop in a sunlit living room"),

 dict(slug="citizen-pass", name="Citizen Pass", url="https://citizen-pass.com", host="citizen-pass.com",
  cat=["citizenship","apps"], catlabel="Citizenship", accent="#F2724B", tint="#0E1A2C",
  tag="Walk in and know you are ready.",
  short="Citizenship test prep for the US, UK, Canada and Australia, with a Readiness Score that says when you're set.",
  title=("Citizen ","Pass"),
  lede="Practice for the citizenship test and know when you are ready. Official study material, turned into quizzes, full mock exams and one honest Readiness Score.",
  what="Citizenship tests",
  over=[
   "The citizenship test is one of the biggest moments in someone's life, and the prep material is mostly a PDF. We wanted to give people something better.",
   "Citizen Pass runs the official study material into <strong>quizzes, full mock exams and a Readiness Score</strong>, so you can stop guessing and start knowing. One pass, every country: <strong>the US, the UK, Canada and Australia</strong>.",
   "It speaks your language too. The study site comes in <strong>Spanish, French, Chinese, Korean and Vietnamese</strong> on top of English, because test prep shouldn't depend on how comfortable you are with English.",
  ],
  facts=[("4","countries, one pass"),("6","languages on the study site"),("iOS + Android","plus the web")],
  feats=[("Readiness Score","A model-driven score that reflects mastery, not just how many cards you flipped."),
         ("Mock exams that feel real","Timed, mixed, and built from the official material for your country."),
         ("Plain-language explanations","Every answer says why, in words that make sense the first time."),
         ("The Canada Journey","A stage-by-stage timeline and a library of common questions for the whole path to citizenship."),
         ("Data worth reading","Open data pages on processing times and trends, built from public sources."),
         ("Study anywhere","Native apps on iOS and Android, and a full study site on the web.")],
  apps=[("United States",[("ios","https://apps.apple.com/us/app/citizen-pass-us-civics-2026/id6759070713"),("android","https://play.google.com/store/apps/details?id=com.civicsready.civics_ready")]),
        ("Canada",[("ios","https://apps.apple.com/app/citizen-pass-canada-test-prep/id6759070931"),("android","https://play.google.com/store/apps/details?id=com.oddlysunny.citizen_pass_canada")]),
        ("Australia",[("ios","https://apps.apple.com/app/citizen-pass-australia/id6759070987"),("android","https://play.google.com/store/apps/details?id=com.oddlysunny.citizen_pass_australia")]),
        ("United Kingdom",[("android","https://play.google.com/store/apps/details?id=com.oddlysunny.citizen_pass_uk")])],
  appnote="",
  img="citizen-pass.jpg", alt="Citizen Pass website on a laptop with an airplane wing over clouds"),

 dict(slug="dmv-iq", name="DMV IQ", url="https://dmv-iq.com", host="dmv-iq.com",
  cat=["driving","apps"], catlabel="Driving", accent="#6AB58E", tint="#141B18",
  tag="Free DMV practice tests for every state.",
  short="Permit test practice for all 50 states and DC, with road-sign visuals and honest explanations.",
  title=("DMV ","IQ"),
  lede="Free DMV practice tests for every state. Real exam-style questions, road-sign visuals and explanations that make the rules stick.",
  what="Driving permit tests",
  over=[
   "Every state writes its own driving rules, and every state's test is a little different. DMV IQ is built around that, not in spite of it.",
   "You get <strong>7,500+ practice questions across all 50 states and DC</strong>, with the details that actually differ from state to state checked against each state's own material.",
   "Expect friendly visuals, road-sign drills, road test guides, and a readiness score that tells you when to stop studying and go get your permit.",
  ],
  facts=[("51","jurisdictions: 50 states and DC"),("7,500+","practice questions"),("Free","to start, no signup")],
  feats=[("Your state, your rules","Questions and facts tuned to the state you're actually testing in."),
         ("Road signs, made easy","Visual drills so shapes, colors and meanings click fast."),
         ("Road test guides","Step-by-step guides for the behind-the-wheel test, for every state."),
         ("Readiness score","See how ready you are as a percentage, and what to review next."),
         ("Personalized study","Weak spots first, so your time goes where it matters."),
         ("Apps and web","iOS, Android and a fast, free website. Start on one, pick up on another.")],
  apps=[("DMV IQ",[("ios","https://apps.apple.com/us/app/dmv-iq-driving-practice-test/id6759559149"),("android","https://play.google.com/store/apps/details?id=com.oddlysunny.dmv_iq")])],
  appnote="",
  img="dmv-iq.jpg", alt="DMV IQ practice question on a tablet in an armchair"),

 dict(slug="drive-iq-canada", name="Drive IQ Canada", url="https://driveiqcanada.com", host="driveiqcanada.com",
  cat=["driving","apps"], catlabel="Driving", accent="#E5484D", tint="#2A0F13",
  tag="Canadian driving test practice, in English and French.",
  short="G1, SAAQ, ICBC, Class 7 and every province. Real exam-style questions in English and French.",
  title=("Drive IQ ","Canada"),
  lede="Free Canadian driving test practice for G1, SAAQ, ICBC, Class 7 and every province. Start free, no signup, in English or French.",
  what="Canadian driving tests",
  over=[
   "Canada doesn't have one driving test. It has a whole stack of them, each with its own handbook, its own rules and its own quirks.",
   "Drive IQ Canada is built <strong>province by province</strong>, so a question about speed zones in Quebec is checked against Quebec's own handbook and not someone else's. And yes, it's <strong>fully bilingual, English and French</strong>.",
   "Cars, motorcycles and commercial classes are all in there, with a Driving Index that ranks things honestly. If a province doesn't have enough data, we leave it unranked rather than fake it.",
  ],
  facts=[("13","provinces and territories"),("2","languages: English and French"),("Free","to start, no signup")],
  feats=[("Every province, its own handbook","Answers verified against that province's official material."),
         ("Truly bilingual","Written for Quebec, not just translated for it."),
         ("Cars, motorcycles, commercial","Passenger, motorcycle and Class 1 prep in one place."),
         ("Driving Index","An honest, data-driven look at how provinces compare, with no made-up rankings."),
         ("Readiness score","Shown as a simple percentage, so you know when to book the test."),
         ("Apps and web","iOS, Android and the website, all in sync.")],
  apps=[("Drive IQ Canada",[("ios","https://apps.apple.com/app/drive-iq-canada-test-prep/id6762389061"),("android","https://play.google.com/store/apps/details?id=com.oddlysunny.drive_iq_canada")])],
  appnote="",
  img="driveiqcanada.jpg", alt="Drive IQ Canada question in French on a tablet on a red fuzzy sofa"),

 dict(slug="insurance-pass", name="Insurance Pass", url="https://www.insurance-pass.com", host="insurance-pass.com",
  cat=["careers"], catlabel="Careers and licences", accent="#E08A5F", tint="#2A1810",
  tag="Pass your insurance license exam with practice built on your state's law.",
  short="Life, health, property, casualty and adjuster exam prep, where every answer quotes the statute behind it.",
  title=("Insurance ","Pass"),
  lede="Practice for your state insurance license exam. Life and Health, Property and Casualty, Personal Lines and Adjuster, with every answer quoting the statute it comes from.",
  what="Insurance licensing",
  over=[
   "Insurance exams are state-by-state, and the rules really do change when you cross a border. Most prep tools wave at that. We went and read the law.",
   "Insurance Pass covers <strong>four lines of authority</strong> across the states and DC. Questions are built from state statutes and regulations, and each answer shows you the provision behind it.",
   "It's licence prep that treats you like a future professional: <strong>no trick questions, no hand-waving</strong>, just the rule and why it's the rule.",
  ],
  facts=[("4","lines of authority"),("51","states and DC"),("Statute","quoted on every answer")],
  feats=[("State-specific practice","Pick your state, pick your line, and practice what your exam actually covers."),
         ("Answers that cite the law","Each explanation quotes the statute or rule, so you learn the source."),
         ("Life and Health","The full life and health producer path, from basics to state overlays."),
         ("Property and Casualty","Commercial and personal property and liability, built around your state's rules."),
         ("Personal Lines and Adjuster","Focused prep for narrower licences and for adjuster exams."),
         ("Readiness you can read","A clear score, so you know when you're set for the proctor.")],
  apps=[], appnote="Web only for now. Open it on any device.",
  img="insurance-pass.jpg", alt="Insurance Pass on a tablet resting on a green velvet sofa"),

 dict(slug="airwaves-iq", name="Airwaves IQ", url="https://airwaves-iq.com", host="airwaves-iq.com",
  cat=["careers","radio"], catlabel="Radio", accent="#4FB39B", tint="#0B2420",
  tag="Ham and commercial radio practice tests.",
  short="Technician, General, Extra and FCC commercial exams with the official pools and a worked answer for each question.",
  title=("Airwaves ","IQ"),
  lede="Practice for the Technician, General, Extra, GROL, radar and GMDSS exams with the official question pools. Every answer explained. Free to start.",
  what="FCC radio exams",
  over=[
   "Radio exams are a delight if you love electronics and a headache if you just want a licence. Airwaves IQ is for both people.",
   "It covers <strong>10 live FCC exams</strong>: amateur (Technician, General, Extra) and commercial. You practice with the <strong>current official question pools</strong>, and every answer comes with a worked explanation and the regulation it comes from.",
   "Math gets walked through step by step, schematics show up where the real test shows them, and a readiness score tells you when to go find a volunteer exam session.",
  ],
  facts=[("10","FCC exams, ham and commercial"),("Official","current NCVEC and FCC pools"),("Free","to start, no card needed")],
  feats=[("The official pools","Practice with the same question pools the exam draws from."),
         ("Worked math","Derivations, step by step, so formulas stop feeling like magic."),
         ("Regulatory citations","Rules come with the section they live in, so you learn where to look."),
         ("Schematics and figures","The diagrams show up where the test shows them."),
         ("Study by category","Work through the syllabus topic by topic and tick them off."),
         ("Readiness score","See your readiness and aim for it before test day.")],
  apps=[], appnote="Web only for now. It works great on your phone's browser.",
  img="airwaves-iq.jpg", alt="Airwaves IQ on a laptop sitting on a green velvet pouf"),

 dict(slug="mariner-iq", name="Mariner IQ", url="https://mariner-iq.com", host="mariner-iq.com",
  cat=["careers","maritime"], catlabel="Maritime", accent="#F6C547", tint="#0B1E3A",
  tag="Pass your Coast Guard captain's license exam.",
  short="Six-pack to 100-ton master, plus mariner credentials, with plain-English answers. Pay once. No subscription.",
  title=("Mariner ","IQ"),
  lede="Practice with questions from the Coast Guard's own sample exams, with a plain-English explanation on every answer. Pay once, no subscription.",
  what="Coast Guard exams",
  over=[
   "Getting a captain's licence is a serious goal, and the prep options mostly feel like a flea market. Mariner IQ is the clean, calm alternative.",
   "It's built from the <strong>Coast Guard's own sample exams</strong>, covering six-pack, 100-ton master, able seaman and other credentials, with a plain-English explanation on every single answer.",
   "And because we like people, it's <strong>pay once, no subscription</strong>. There's even a night mode that turns the screen bridge-red for the wheelhouse.",
  ],
  facts=[("USCG","own sample exams"),("Once","pay once, no subscription"),("Bridge","red night mode built in")],
  feats=[("Straight from the source","Questions drawn from the Coast Guard's own sample exams."),
         ("Plain-English answers","Maritime jargon, translated, on every answer."),
         ("Many credentials","Six-pack, master, able seaman and more, in one place."),
         ("Route and rules practice","Charts, rules of the road and navigation, practiced the way you'll be tested."),
         ("Bridge night mode","A red-light theme that keeps your night vision intact."),
         ("Pay once","One price. No renewals, no surprises.")],
  apps=[], appnote="Web only for now. Open it on your phone or laptop.",
  img="mariner-iq.jpg", alt="Mariner IQ on a phone on a deep blue velvet sofa"),
]
BY = {p["slug"]: p for p in PRODUCTS}
FEATURED_ORDER = ["aviator-iq","citizen-pass","dmv-iq","drive-iq-canada","insurance-pass","airwaves-iq","mariner-iq"]

CAPS = [
 ("check","Grounded in official sources","AI drafts every question from official public material only, and each one carries a verbatim quote from its source."),
 ("book","Built for real exam conditions","Blueprints, question counts, timing, pass marks and figures are modeled on the official exam, so practice feels like test day."),
 ("globe","Blind verification","Independent AI reviewers answer every question without seeing the key. If they disagree with it, it never ships."),
 ("spark","Bias-proofed answers","We measure answer position and answer length patterns, so nobody passes by spotting the pattern instead of knowing the material."),
 ("chart","Adaptive readiness","A model-driven score tracks coverage, accuracy, recall and speed, and points students at their weak spots first."),
 ("phone","Always current","Source monitors watch for new editions and rule changes, so the practice updates when the exam does."),
]
ICONS = {
 "book":'<path d="M4 5.500A2.500 2.500 0 0 1 6.500 3H20v16H6.500A2.500 2.500 0 0 0 4 21.500z"/><path d="M4 19V5.500"/>',
 "check":'<path d="M12 3 4 6v6c0 4.500 3.200 8 8 9 4.800-1 8-4.500 8-9V6z"/><path d="m8.500 12 2.500 2.500 4.500-5"/>',
 "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.500 2.700 3.800 5.700 3.800 9S14.500 18.300 12 21c-2.500-2.700-3.800-5.700-3.800-9S9.500 5.700 12 3z"/>',
 "phone":'<rect x="7" y="2.500" width="10" height="19" rx="2.500"/><path d="M11 18.500h2"/>',
 "chart":'<path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/>',
 "spark":'<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.500 2.500M15.500 15.500 18 18M18 6l-2.500 2.500M8.500 15.500 6 18"/>',
}
ICON_ORDER = ["book","check","globe","phone","chart","spark"]
STEPS = [
 ("Find the gate","Every product starts with a test people have to pass. We dig into who takes it, what trips them up, and what the official sources say."),
 ("Source the truth","We build the question bank from official, public material, check every answer against it, and keep a paper trail."),
 ("Make it feel good","Then the fun part: design, animation, readiness scoring, explanations a human would write."),
 ("Keep it fresh","Rules change and handbooks get new editions. We watch the sources and update, so nobody studies yesterday's law."),
]
SCHEME = {"aviator-iq":"ember","citizen-pass":"purple","dmv-iq":"green","drive-iq-canada":"ember","insurance-pass":"ember","airwaves-iq":"green","mariner-iq":"purple"}

def esc(s): return html.escape(s, quote=True)
def icon(k): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

def mark(cls=""):
    return f'<div class="mark {cls}"><div class="cell c1"></div><div class="cell c2"></div><div class="cell c3"></div><div class="cell c4"></div></div>'

def head_html(title, desc, path, og_img=None):
    og = f'<meta property="og:image" content="https://oddlysunny.com/assets/img/{og_img}">' if og_img else ''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://oddlysunny.com{path}">
{og}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#091A12">
<link rel="canonical" href="https://oddlysunny.com{path}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;500;600&family=Sora:wght@300;400;500&family=Newsreader:ital,wght@0,300;0,400;1,300;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=24">
</head>
"""

def header():
    items = "".join(f'<a href="/work/{p["slug"]}/">{p["name"]}<span>{esc(p["catlabel"])}</span></a>' for p in [BY[s] for s in FEATURED_ORDER])
    return f"""<body>
<header class="hdr" data-scheme="green">
  <div class="wrap">
    <a href="/" class="brand" aria-label="oddly sunny home">{mark("sm")}<span>oddly <b>sunny</b></span></a>
    <nav class="nav" aria-label="Main">
      <div class="dd"><button type="button" aria-haspopup="true">Our portfolio <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.6"><path d="m2 3.500 3 3 3-3"/></svg></button>
        <div class="dd-menu">{items}</div></div>
      <a href="/#expertise">Our method</a>
      <a class="btn" href="mailto:{MAIL}">Say hello</a>
    </nav>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><i></i></button>
  </div>
</header>
"""

def footer(scheme="ember"):
    return f"""<footer class="ftr s" data-scheme="{scheme}">
  <div class="wrap ftr-row">
    <div class="l">{mark("xs")}<span>oddly sunny llc</span></div>
    <div class="r"><a href="mailto:{MAIL}">{MAIL}</a><a href="/privacy/">Privacy</a><a href="/cookie-settings/">Cookies</a></div>
  </div>
</footer>
<script src="/assets/site.js?v=8"></script>
</body>
</html>
"""

def store_btn(kind, url):
    if kind == "ios":
        return f'<a class="store" href="{url}" target="_blank" rel="noopener">{APPLE}<span><small>Download on the</small><strong>App Store</strong></span></a>'
    return f'<a class="store" href="{url}" target="_blank" rel="noopener">{PLAY}<span><small>Get it on</small><strong>Google Play</strong></span></a>'

def item(p, wide=False):
    plat = "iOS, Android, Web" if p["apps"] else "Web"
    return f"""<a class="item {'w2' if wide else ''} reveal" data-cat="{' '.join(p['cat'])}" href="/work/{p['slug']}/">
  <div class="img"><img src="/assets/img/{p['img']}" alt="{esc(p['alt'])}" loading="lazy"></div>
  <h3>{p['name']}</h3><p>{esc(p['catlabel'])}, {plat}</p>
</a>"""

def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(content)

def closing(scheme="ember"):
    return f"""<section class="closing" data-scheme="{scheme}"><div class="wrap reveal">
  <div class="eyebrow">Let's talk</div>
  <h2 class="h2" style="margin-top:16px">Got a test people dread? <i>Let's make it oddly pleasant.</i></h2>
  <p class="body">Building something in learning, training or certification? We'd love to compare notes.</p>
  <div class="cta-row"><a class="btn" href="mailto:{MAIL}">Say hello {ARROW}</a></div>
</div></section>
"""

def home():
    F = [BY[s] for s in FEATURED_ORDER]
    import json
    pos = {"cp-hoodie":"18%","cp-blonde":"82%","mariner-woman":"42%","cp-smile":"40%"}
    order = ["cp-smile","study-library","cp-dog","study-desk","cp-denim","study-woman","cp-hoodie","cp-glasses","mariner-woman","cp-blonde","airwaves-man"]
    imgs = json.dumps([{"n": n, "p": pos.get(n, "50%")} for n in order])
    wall = "".join(f'<div class="float f{i}"><img src="" alt=""></div>' for i in range(1, 9))
    feats = "".join(f'<div class="feat reveal"><div class="ic">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in CAPS)
    steps = "".join(f'<div class="step reveal"><div><h3>{t}</h3><p>{d}</p></div><b>0{i+1}</b></div>' for i, (t, d) in enumerate(STEPS))
    words = '<span class="word">everything</span> <span class="word">worth</span> <span class="word">building</span> <br> <span class="word accent">was</span> <span class="word accent">once</span> <span class="word accent">an</span> <span class="word odd">odd</span> <span class="word accent">idea</span> <span class="word accent">in</span> <span class="word accent">good</span> <span class="word accent">light.</span>'
    def pt(slug):
        p = BY[slug]
        plat = "iOS, Android, Web" if p["apps"] else "Web"
        return f'''<a class="pt" href="/work/{slug}/"><img class="pimg" src="/assets/img/{p["img"]}" alt="{esc(p["alt"])}" loading="lazy">
  <div class="cap"><div class="hd"><div><h3>{p["name"]}</h3><span>{p["host"]}</span></div></div>
  <div class="more"><p>{esc(p["short"])}</p><div class="chips"><span>{esc(p["catlabel"])}</span><span>{plat}</span></div><span class="go">Explore {ARROW}</span></div></div></a>'''
    bento = (f'<div class="brow">{pt("aviator-iq")}<div class="stack">{pt("citizen-pass")}{pt("dmv-iq")}</div></div>'
             f'<div class="brow rev"><div class="stack">{pt("drive-iq-canada")}{pt("insurance-pass")}</div>{pt("airwaves-iq")}</div>'
             f'<div class="brow">{pt("mariner-iq")}<a class="pt all" href="/#expertise"><div><span class="eyebrow">The Oddly Sunny Method</span><h3>One method, <i>every brand</i></h3><span class="go">See our method {ARROW}</span></div></a></div>')
    body = f"""
<section class="hero" data-scheme="green" data-imgs='{imgs}'>
  {wall}
  <div class="wrap"><div class="copy">
    <div class="mark hero-mark" id="heroMark"><div class="cell c1"></div><div class="cell c2"></div><div class="cell c3"></div><div class="cell c4"></div></div>
    <h1>Modern education for<br>the tests <i>that never got one.</i></h1>
    <p class="lede">Driver's licences. Citizenship. Pilot, radio, maritime and insurance exams. Oddly Sunny brings modern, AI-powered education to the high-stakes tests that still run on dusty PDFs and guesswork, built from official sources and engineered to match the real exam.</p>
    <div class="cta-row"><a class="btn" href="#work">See our work {ARROW}</a></div>
  </div></div>
</section>

<section class="sec" data-scheme="cream"><div class="wrap split">
  <div class="reveal">
    <div class="eyebrow rule">Who we are</div>
    <h2 class="h2">We built the AI <i>that builds the prep</i></h2>
    <p class="sub">Most test prep is written once and left to age. Ours is generated, verified and refreshed by a proprietary AI method we built in-house.</p>
    <p class="body">Oddly Sunny is the company behind a family of learning brands. Each one starts from official sources and runs through the same method: questions grounded in source text, independently verified, and modeled on real exam conditions. One method, many exams.</p>
    <div class="cta-row"><a class="btn" href="#work">Explore our work {ARROW}</a></div>
  </div>
  <div class="pic reveal"><img src="/assets/img/who-we-are.jpg" alt="A learner studying at a laptop in warm evening light" loading="lazy"></div>
</div></section>

<section class="sec" id="work" data-scheme="purple"><div class="wrap center">
  <div class="eyebrow reveal">Our portfolio</div>
  <h2 class="h2 reveal">Learning brands, <i>all oddly good</i></h2>
  <div class="bento reveal">{bento}</div>
  </div></section>

<section id="expertise" data-scheme="tan"><div class="exp">
  <div class="l">
    <div class="eyebrow rule">The Oddly Sunny Method</div>
    <h2 class="h2">Engineered to match <i>the real exam</i></h2>
    <p class="sub">Our proprietary, AI-powered method turns official exam sources into practice that mirrors test day and teaches what students actually need to know.</p>
    <div class="feats">{feats}</div>
  </div>
  <div class="r"><img src="/assets/img/dmv-iq.jpg" alt="DMV IQ practice question on a tablet" loading="lazy"></div>
</div></section>

"""
    return head_html("oddly sunny | Modern, AI-powered education for the tests that matter",
        "Oddly Sunny builds and operates AI-powered learning brands for licences, citizenship and careers: Aviator IQ, Citizen Pass, DMV IQ, Drive IQ Canada, Insurance Pass, Airwaves IQ and Mariner IQ.",
        "/", "aviator-iq.jpg") + header().replace('class="hdr"', 'class="hdr brand-hidden away" data-away') + body + footer()

FLOAT_ORDER = ["cp-smile","study-library","cp-dog","study-desk","cp-denim","study-woman","cp-hoodie","cp-glasses","mariner-woman","cp-blonde","airwaves-man"]
FLOAT_POS = {"cp-hoodie":"18%","cp-blonde":"82%","cp-smile":"40%","mariner-woman":"42%"}
def floats(offset=0):
    order = FLOAT_ORDER[offset:] + FLOAT_ORDER[:offset]
    imgs = json.dumps([{"n": n, "p": FLOAT_POS.get(n, "50%")} for n in order])
    wall = "".join(f'<div class="float f{i}"><img src="" alt=""></div>' for i in range(1, 9))
    return imgs, wall

def product(p):
    i = FEATURED_ORDER.index(p["slug"])
    prev = BY[FEATURED_ORDER[(i-1) % len(FEATURED_ORDER)]]
    nxt = BY[FEATURED_ORDER[(i+1) % len(FEATURED_ORDER)]]
    sc = SCHEME[p["slug"]]
    a, b = p["title"]
    over = "".join(f"<p>{t}</p>" for t in p["over"])
    nums = "".join(f'<div class="num reveal"><p>{esc(l)}</p><b class="{"sm" if len(n) > 6 else ""}">{n}</b></div>' for n, l in p["facts"])
    feats = "".join(f'<div class="feat reveal"><div class="ic">{icon(ICON_ORDER[k % 6])}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for k, (t, d) in enumerate(p["feats"]))
    rows = ""
    for label, links in p["apps"]:
        rows += f'<div class="get-row"><small>{esc(label)}</small>{"".join(store_btn(k, u) for k, u in links)}</div>'
    if not p["apps"]:
        rows = f'<div class="get-row"><span class="web-only">{esc(p["appnote"])}</span></div>'
    web = f'<a class="btn" href="{p["url"]}" target="_blank" rel="noopener">Visit {p["host"]} {ARROW}</a>'
    get_title = "Get the app, <i>or go straight to the web</i>" if p["apps"] else "Jump in <i>on the web</i>"
    get_desc = f"{p['name']} is live right now. Start practicing in your browser or grab it on your phone." if p["apps"] else f"{p['name']} is live right now. No download needed: open it, pick your exam and start practicing."
    fimgs, fwall = floats(i % len(FLOAT_ORDER))
    body = f"""
<section class="hero phero" data-scheme="{sc}" data-imgs='{fimgs}'>
  {fwall}
  <div class="wrap"><div class="copy">
    <div class="mark hero-mark" id="heroMark"><div class="cell c1"></div><div class="cell c2"></div><div class="cell c3"></div><div class="cell c4"></div></div>
    <div class="crumb"><a href="/">oddly sunny</a><span>/</span><a href="/#work">Our portfolio</a></div>
    <h1>{a}<i>{b}</i></h1>
    <p class="lede">{esc(p['lede'])}</p>
    <div class="cta-row">{web}<a class="btn ghost" href="#get">{'Get the apps' if p['apps'] else 'How to get it'}</a></div>
    <div class="p-meta">
      <div><small>Exams</small><span>{esc(p['what'])}</span></div>
      <div><small>Platforms</small><span>{"iOS, Android and web" if p["apps"] else "Web"}</span></div>
      <div><small>Status</small><span>Live</span></div>
    </div>
  </div></div>
</section>
<section class="shot" data-scheme="{sc}"><div class="wrap"><img src="/assets/img/{p['img']}" alt="{esc(p['alt'])}"></div></section>

<section class="sec" data-scheme="cream"><div class="wrap o-split">
  <div class="reveal"><div class="eyebrow rule">About {p['name']}</div><h2 class="h2">{esc(p['tag'])}</h2></div>
  <div class="prose reveal">{over}</div>
</div></section>

<section class="sec" data-scheme="{sc}"><div class="wrap">
  <div class="center reveal"><div class="eyebrow">At a glance</div><h2 class="h2">{p['name']}, <i>in short</i></h2></div>
  <div class="nums">{nums}</div>
</div></section>

<section class="sec" data-scheme="tan"><div class="wrap">
  <div class="reveal"><div class="eyebrow rule">What's inside</div><h2 class="h2">The good <i>stuff</i></h2></div>
  <div class="fgrid">{feats}</div>
</div></section>

<section class="sec" id="get" data-scheme="cream"><div class="wrap get">
  <div class="reveal"><div class="eyebrow rule">Get {p['name']}</div><h2 class="h2">{get_title}</h2><p class="body">{esc(get_desc)}</p><div class="cta-row">{web}</div></div>
  <div class="get-links reveal">{rows}</div>
</div></section>

<section data-scheme="{sc}" style="padding:50px 0 90px"><div class="wrap"><div class="pn">
  <a href="/work/{prev['slug']}/"><small>Previous</small><strong>{prev['name']}</strong></a>
  <a href="/work/{nxt['slug']}/"><small>Next</small><strong>{nxt['name']}</strong></a>
</div></div></section>
"""
    return head_html(f"{p['name']} | oddly sunny", f"{p['name']}: {p['lede']}", f"/work/{p['slug']}/", p["img"]) + header().replace('class="hdr"', 'class="hdr brand-hidden away" data-away') + body + footer(sc)

if __name__ == "__main__":
    write("index.html", home())
    for p in PRODUCTS:
        write(f"work/{p['slug']}/index.html", product(p))
    print("built", 1 + len(PRODUCTS), "pages")
