#!/usr/bin/env python3
"""Builds the oddlysunny.com static pages. Run from repo root: python3 _build/build.py
Writes index.html, work/index.html and work/<slug>/index.html. Edit copy here, not in the output."""
import os, re, sys, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stories import STORIES
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
  apps=[("Aviator IQ",[("ios","https://apps.apple.com/us/app/aviator-iq-faa-test-prep/id6813969252"),("android","https://play.google.com/store/apps/details?id=com.oddlysunny.aviator_iq")])], appnote="",
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
  tag="DMV practice tests for every state.",
  short="Permit test practice for all 50 states and DC, with road-sign visuals and honest explanations.",
  title=("DMV ","IQ"),
  lede="DMV practice tests for every state. Real exam-style questions, road-sign visuals and explanations that make the rules stick.",
  what="Driving permit tests",
  over=[
   "Every state writes its own driving rules, and every state's test is a little different. DMV IQ is built around that, not in spite of it.",
   "You get <strong>7,500+ practice questions across all 50 states and DC</strong>, with the details that actually differ from state to state checked against each state's own material.",
   "Expect friendly visuals, road-sign drills, road test guides, and a readiness score that tells you when to stop studying and go get your permit.",
  ],
  facts=[("51","jurisdictions: 50 states and DC"),("7,500+","practice questions"),("Official","state handbooks")],
  feats=[("Your state, your rules","Questions and facts tuned to the state you're actually testing in."),
         ("Road signs, made easy","Visual drills so shapes, colors and meanings click fast."),
         ("Road test guides","Step-by-step guides for the behind-the-wheel test, for every state."),
         ("Readiness score","See how ready you are as a percentage, and what to review next."),
         ("Personalized study","Weak spots first, so your time goes where it matters."),
         ("Apps and web","iOS, Android and a fast website. Start on one, pick up on another.")],
  apps=[("DMV IQ",[("ios","https://apps.apple.com/us/app/dmv-iq-driving-practice-test/id6759559149"),("android","https://play.google.com/store/apps/details?id=com.oddlysunny.dmv_iq")])],
  appnote="",
  img="dmv-iq.jpg", alt="DMV IQ practice question on a tablet in an armchair"),

 dict(slug="drive-iq-canada", name="Drive IQ Canada", url="https://driveiqcanada.com", host="driveiqcanada.com",
  cat=["driving","apps"], catlabel="Driving", accent="#E5484D", tint="#2A0F13",
  tag="Canadian driving test practice, in English and French.",
  short="G1, SAAQ, ICBC, Class 7 and every province. Real exam-style questions in English and French.",
  title=("Drive IQ ","Canada"),
  lede="Canadian driving test practice for G1, SAAQ, ICBC, Class 7 and every province, in English or French.",
  what="Canadian driving tests",
  over=[
   "Canada doesn't have one driving test. It has a whole stack of them, each with its own handbook, its own rules and its own quirks.",
   "Drive IQ Canada is built <strong>province by province</strong>, so a question about speed zones in Quebec is checked against Quebec's own handbook and not someone else's. And yes, it's <strong>fully bilingual, English and French</strong>.",
   "Cars, motorcycles and commercial classes are all in there, with a Driving Index that ranks things honestly. If a province doesn't have enough data, we leave it unranked rather than fake it.",
  ],
  facts=[("13","provinces and territories"),("2","languages: English and French"),("Official","each province's handbook")],
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
  lede="Practice for the Technician, General, Extra, GROL, radar and GMDSS exams with the official question pools. Every answer explained.",
  what="FCC radio exams",
  over=[
   "Radio exams are a delight if you love electronics and a headache if you just want a licence. Airwaves IQ is for both people.",
   "It covers <strong>9 FCC exams</strong>: amateur (Technician, General, Extra) and commercial. You practice with the <strong>current official question pools</strong>, and every answer comes with a worked explanation and the regulation it comes from.",
   "Math gets walked through step by step, schematics show up where the real test shows them, and a readiness score tells you when to go find a volunteer exam session.",
  ],
  facts=[("9","FCC exams, ham and commercial"),("Official","current NCVEC and FCC pools"),("Pools","current FCC and NCVEC")],
  feats=[("The official pools","Practice with the same question pools the exam draws from."),
         ("Worked math","Derivations, step by step, so formulas stop feeling like magic."),
         ("Regulatory citations","Rules come with the section they live in, so you learn where to look."),
         ("Schematics and figures","The diagrams show up where the test shows them."),
         ("Study by category","Work through the syllabus topic by topic and tick them off."),
         ("Readiness score","See your readiness and aim for it before test day.")],
  apps=[], appnote="Web only for now. It works great on your phone's browser.",
  img="airwaves-iq.jpg", alt="Airwaves IQ on a laptop sitting on a green velvet pouf"),

 dict(slug="mariner-iq", name="Mariner IQ", url="https://mariner-iq.com", host="mariner-iq.com",
  cat=["careers","maritime"], catlabel="Maritime", accent="#D4A63C", tint="#0B1E3A",
  tag="Pass your Coast Guard captain's license exam.",
  short="Six-pack to 100-ton master, plus mariner credentials, with plain-English answers.",
  title=("Mariner ","IQ"),
  lede="Practice with questions from the Coast Guard's own sample exams, with a plain-English explanation on every answer.",
  what="Coast Guard exams",
  over=[
   "Getting a captain's licence is a serious goal, and the prep options mostly feel like a flea market. Mariner IQ is the clean, calm alternative.",
   "It's built from the <strong>Coast Guard's own sample exams</strong>, covering six-pack, 100-ton master, able seaman and other credentials, with a plain-English explanation on every single answer.",
   "There's even a night mode that turns the screen bridge-red for the wheelhouse.",
  ],
  facts=[("USCG","own sample exams"),("Bridge","red night mode built in")],
  feats=[("Straight from the source","Questions drawn from the Coast Guard's own sample exams."),
         ("Plain-English answers","Maritime jargon, translated, on every answer."),
         ("Many credentials","Six-pack, master, able seaman and more, in one place."),
         ("Route and rules practice","Charts, rules of the road and navigation, practiced the way you'll be tested."),
         ("Bridge night mode","A red-light theme that keeps your night vision intact.")],
  apps=[], appnote="Web only for now. Open it on your phone or laptop.",
  img="mariner-iq.jpg", alt="Mariner IQ on a phone on a deep blue velvet sofa"),
]
BY = {p["slug"]: p for p in PRODUCTS}
FEATURED_ORDER = ["aviator-iq","citizen-pass","dmv-iq","drive-iq-canada","insurance-pass","airwaves-iq","mariner-iq"]

CAPS = [
 ("quote","Direct Source Grounding","Every question carries a word-for-word quote from the official manual or regulation it came from. No source, no question."),
 ("blind","Independent Blind Check","A second model answers questions without seeing the key. When it disagrees, the question goes back for review."),
 ("blueprint","Official Exam Blueprint","Question counts, time limits and pass marks match the real exam, and topic coverage is checked against the published outline."),
 ("pattern","Giveaway Detection","We test banks for answer patterns, like the right answer sitting in one position or always being the longest, and fix them so scores reflect knowledge."),
]
ICONS = {
 "book":'<path d="M4 5.500A2.500 2.500 0 0 1 6.500 3H20v16H6.500A2.500 2.500 0 0 0 4 21.500z"/><path d="M4 19V5.500"/>',
 "check":'<path d="M12 3 4 6v6c0 4.500 3.200 8 8 9 4.800-1 8-4.500 8-9V6z"/><path d="m8.500 12 2.500 2.500 4.500-5"/>',
 "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.500 2.700 3.800 5.700 3.800 9S14.500 18.300 12 21c-2.500-2.700-3.800-5.700-3.800-9S9.500 5.700 12 3z"/>',
 "phone":'<rect x="7" y="2.500" width="10" height="19" rx="2.500"/><path d="M11 18.500h2"/>',
 "chart":'<path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/>',
 "route":'<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7.500a3.500 3.500 0 0 0 0-7h-7a3.500 3.500 0 0 1 0-7H16"/>',
 "chat":'<path d="M20 12.500a7.500 7.500 0 0 1-11 6.600L4 20.500l1.400-4.600A7.500 7.500 0 1 1 20 12.500z"/><path d="M9 12h.01M12.500 12h.01M16 12h.01"/>',
 "spark":'<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.500 2.500M15.500 15.500 18 18M18 6l-2.500 2.500M8.500 15.500 6 18"/>',
 # brand set (Oct 2026 pass): one forest stroke + one gold accent ("ac") per icon
 "plane":'<path d="M3 13.500 21 6l-6.500 15-2.800-6.200z"/><path class="ac" d="m11.700 14.800 3.300-3.300"/>',
 "anchor":'<circle cx="12" cy="5" r="2"/><path d="M12 7v13"/><path d="M5 13a7 7 0 0 0 14 0"/><path class="ac" d="M8.500 10.500h7"/>',
 "wheel":'<circle cx="12" cy="12" r="8.500"/><path d="M3.600 11h5.400M15 11h5.400M12 14v6.400"/><circle class="ac" cx="12" cy="12" r="2.200"/>',
 "scales":'<path d="M12 4v16M8 20h8M5 7h14"/><path d="M5 7 2.500 12.500a2.500 2.500 0 0 0 5 0z"/><path d="M19 7l-2.500 5.500a2.500 2.500 0 0 0 5 0z"/><circle class="ac" cx="12" cy="4" r="1.400"/>',
 "ingest":'<path d="M7 3h7l4 4v5"/><path d="M14 3v4h4"/><path d="M4 14v5a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/><path class="ac" d="M11 8v7m-3-3 3 3 3-3"/>',
 "adapt":'<circle cx="5" cy="18.500" r="2"/><path d="M7 18.500h5a4 4 0 0 0 0-8h-3a3 3 0 0 1 0-6h9"/><path class="ac" d="m16 2.500 2 2-2 2"/>',
 "verify":'<path d="M12 3 4.500 6v5.500c0 4.400 3.100 8 7.500 9.500 4.400-1.500 7.500-5.100 7.500-9.500V6z"/><path class="ac" d="m8.500 12 2.500 2.500 4.500-5"/>',
 "gauge":'<path d="M3.500 17a8.500 8.500 0 1 1 17 0"/><path d="M12 8.500V9.500M6.300 11.300l.7.7M17.700 11.300l-.7.7"/><path class="ac" d="m12 17 3.800-4.800"/><circle cx="12" cy="17" r="1.300"/>',
 "cells":'<rect x="3.500" y="3.500" width="7" height="7" rx="2"/><rect x="13.500" y="3.500" width="7" height="7" rx="2"/><rect x="13.500" y="13.500" width="7" height="7" rx="2"/><rect class="ac" x="4.600" y="14.600" width="4.800" height="4.800" rx="1.200" transform="rotate(45 7 17)"/>',
 "quote":'<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><path d="M9 9.500h4M9 17h5"/><path class="ac" d="M9 13.300h7"/>',
 "blind":'<path d="M2.500 12S6 5.500 12 5.500 21.500 12 21.500 12 18 18.500 12 18.500 2.500 12 2.500 12z"/><circle cx="12" cy="12" r="2.800"/><path class="ac" d="M4.500 19.500 19.500 4.500"/>',
 "blueprint":'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V2.800h6V4"/><path d="M8.500 9.500h7M8.500 13h7"/><path class="ac" d="M8.500 16.500h4"/>',
 "pattern":'<circle cx="10.500" cy="10.500" r="6.500"/><path d="m15.500 15.500 5 5"/><path class="ac" d="M8 8.500h.01M10.500 8.500h.01M13 8.500h.01M8 11h.01M8 13.500h.01M10.500 11h.01"/>',
}
ICON_ORDER = ["book","check","globe","phone","chart","spark"]
STEPS = [
 ("Find the gate","Every product starts with a test people have to pass. We dig into who takes it, what trips them up, and what the official sources say."),
 ("Source the truth","We build the question bank from official, public material, check every answer against it, and keep a paper trail."),
 ("Make it feel good","Then the fun part: design, animation, readiness scoring, explanations a human would write."),
 ("Keep it fresh","Rules change and handbooks get new editions. We watch the sources and update, so nobody studies yesterday's law."),
]
SCHEME = {"aviator-iq":"ember","citizen-pass":"purple","dmv-iq":"green","drive-iq-canada":"ember","insurance-pass":"ember","airwaves-iq":"green","mariner-iq":"purple"}

def platforms(p):
    kinds = {k for _, links in p["apps"] for k, _ in links}
    out = (["iOS"] if "ios" in kinds else []) + (["Android"] if "android" in kinds else []) + ["Web"]
    return ", ".join(out)

def esc(s): return html.escape(s, quote=True)
def icon(k): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

def mark(cls=""):
    return f'<div class="mark {cls}"><div class="cell c1"></div><div class="cell c2"></div><div class="cell c3"></div><div class="cell c4"></div></div>'

SITE = "https://oddlysunny.com"
SEO_TITLE = {
 "aviator-iq": "Aviator IQ: FAA Knowledge Test Prep | Oddly Sunny",
 "citizen-pass": "Citizen Pass: Citizenship Test Practice | Oddly Sunny",
 "dmv-iq": "DMV IQ: State DMV Practice Tests | Oddly Sunny",
 "drive-iq-canada": "Drive IQ Canada: Driving Test Practice | Oddly Sunny",
 "insurance-pass": "Insurance Pass: License Exam Prep | Oddly Sunny",
 "airwaves-iq": "Airwaves IQ: Ham and FCC Radio Tests | Oddly Sunny",
 "mariner-iq": "Mariner IQ: Coast Guard License Prep | Oddly Sunny",
}
def trim(t, n=155):
    if len(t) <= n: return t
    cut = t[:n].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "..."

def head_html(title, desc, path, og_img, ld=None):
    desc = trim(desc)
    img = f"{SITE}/assets/og/{og_img}"
    ld_tag = "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in (ld or []))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:site_name" content="Oddly Sunny">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#091A12">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{ld_tag}<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;500;600&family=Inter:wght@300;400;500;600&family=Newsreader:ital,wght@0,300;0,400;1,300;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=192">
</head>
"""

def live_mark():
    """Header logo as inline SVG so the gold cell can morph and the green cells can wink. Animated by assets/site.js."""
    return ('<svg class="live-mark" viewBox="0 0 100 100" aria-hidden="true">'
            '<rect class="c c1" x="2" y="2" width="46" height="46" rx="12"/>'
            '<rect class="c c2" x="52" y="2" width="46" height="46" rx="12"/>'
            '<rect class="c c4" x="52" y="52" width="46" height="46" rx="12"/>'
            '<g transform="translate(25 75)"><g class="gold">'
            '<g class="sh on" data-s="diamond"><rect x="-17" y="-17" width="34" height="34" rx="8" transform="rotate(45)"/></g>'
            '<g class="sh" data-s="triangle"><path class="f" d="M0 -20 L21 15 L-21 15 Z"/></g>'
            '<g class="sh" data-s="arrow"><path class="st" d="M0 19 V-17 M-15 -3 L0 -19 L15 -3"/></g>'
            '<g class="sh" data-s="circle"><circle r="19"/></g>'
            '<g class="sh" data-s="check"><path class="st" d="M-18 2 L-6 14 L18 -14"/></g>'
            '<g class="sh" data-s="plus"><path class="st" d="M0 -19 V19 M-19 0 H19"/></g>'
            '<g class="sh" data-s="heart"><path class="f" d="M0 20 C-26 2 -22 -19 -9 -18 C-3 -17.5 0 -13 0 -10 C0 -13 3 -17.5 9 -18 C22 -19 26 2 0 20 Z"/></g>'
            '</g></g></svg>')

def header():
    return f"""<body>
<header class="hdr hdr-ent" data-scheme="white" data-fixed>
  <div class="wrap">
    <a href="/" class="brand" aria-label="oddly sunny home">{live_mark()}<span>oddly <b>sunny</b></span></a>
    <nav class="nav" aria-label="Main">
      <a href="/#platform">Architecture<span class="nav-go">{ARROW_R}</span></a>
      <a href="/#verticals">Verticals<span class="nav-go">{ARROW_R}</span></a>
      <a href="/sunny/">Sunny AI<span class="nav-go">{ARROW_R}</span></a>
      <a class="btn" href="/contact/">Contact</a>
    </nav>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><i></i></button>
  </div>
</header>
"""

def footer(scheme="ember"):
    return f"""<footer class="ftr s" data-scheme="{scheme}">
  <div class="wrap ftr-row">
    <div class="l">{mark("xs")}<span>&copy; 2026 Oddly Sunny LLC. All rights reserved. Proprietary Learning Infrastructure.</span></div>
    <div class="r"><a href="mailto:{MAIL}">{MAIL}</a><a href="/privacy/">Privacy</a><a href="/cookie-settings/">Cookies</a></div>
  </div>
</footer>
<script src="/assets/site.js?v=69"></script>
</body>
</html>
"""

def store_btn(kind, url):
    if kind == "ios":
        return f'<a class="store" href="{url}" target="_blank" rel="noopener">{APPLE}<span><small>Download on the</small><strong>App Store</strong></span></a>'
    return f'<a class="store" href="{url}" target="_blank" rel="noopener">{PLAY}<span><small>Get it on</small><strong>Google Play</strong></span></a>'

def item(p, wide=False):
    plat = platforms(p)
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

def hero_floats():
    # owner set (2026-10-19): five studio headshots rotate; slots f4 (right middle; top right on phones) and f6 (bottom left)
    # only ever hold product shots: two of the three are always on screen, never on the same row (they crossfade, see site.js)
    heads = ["hs-curls","hs-wink","hs-bangs","hs-laugh","hs-glasses"]
    products = ["pr-tablet-chair","pr-phone-progress","pr-tablet-course"]
    pools = {"p": [{"src": f"/assets/img/wall/{n}.jpg?v=5", "pos": "50%"} for n in heads],
             "l": [{"src": f"/assets/img/wall/{n}.jpg?v=4", "pos": "50%"} for n in products]}
    kinds = {1: "p", 2: "p", 3: "p", 4: "l", 5: "p", 6: "l"}
    wall = "".join(f'<div class="float f{i}" data-pool="{kinds[i]}"><img src="" alt=""></div>' for i in range(1, 7))
    return json.dumps(pools), wall

# ------------------------------------------------------------------ enterprise homepage blocks
# hero mesh: real sources feed the engine, which feeds four live brands.
# Coordinates are in a 520x400 box; the HTML nodes are placed at the same percentages so the SVG curves meet them.
MESH_SRC = [("Pilot rules and handbooks","FAA","plane"),("Mariner licensing rules","U.S. Coast Guard","anchor"),("State driver handbooks","DMVs","wheel"),("State insurance laws","Insurance regulators","scales")]
HUB_STEPS = ["Unify sources", "Cross-reference rules", "Verify every answer", "Watch for new editions"]
MESH_OUT = [("aviator-iq","Aviation"),("mariner-iq","Maritime"),("dmv-iq","Driving"),("insurance-pass","Insurance")]
MESH_Y = [62, 154, 246, 338]
def flow():
    """Platform figure (Oct 2026 brand pass): an editorial diagram on a forest plate. Sources are typeset (agency in
    small caps over a serif title), the engine carries the real brand mark and numbered steps, products sit as app
    icons with names. Hairline curves join them on desktop; phones read it top to bottom along one gold rail."""
    ys = [62, 167, 272, 377]                      # row centres in the 1000 x 440 stage
    din = lambda y: f"M303 {y} C 356 {y}, 346 220, 392 220"
    dout = lambda y: f"M608 220 C 654 220, 644 {y}, 697 {y}"
    curves = "".join(f'<path class="fl-c in" d="{din(y)}"/><path class="fl-c out" d="{dout(y)}"/>' for y in ys)
    # glints: a short bright dash that runs each curve, sources first, then out to the products
    curves += "".join(f'<path class="fl-g in" pathLength="100" style="--i:{i}" d="{din(y)}"/><path class="fl-g out" pathLength="100" style="--i:{i}" d="{dout(y)}"/>' for i, y in enumerate(ys))
    svg = f'<svg class="fl-svg" viewBox="0 0 1000 440" preserveAspectRatio="none" aria-hidden="true">{curves}</svg>'
    src = "".join(f'<li class="fl-src" style="--y:{y / 4.4}%;--i:{i}"><span class="fl-ag">{esc(a)}</span><b>{esc(s)}</b></li>' for i, ((s, a, _), y) in enumerate(zip(MESH_SRC, ys)))
    out = "".join(f'<li class="fl-out" style="--y:{y / 4.4}%;--i:{i}"><img src="/assets/img/apps/{slug}.png" alt="" width="30" height="30"><span><b>{BY[slug]["name"]}</b><span class="fl-ag">{esc(l)}</span></span></li>' for i, ((slug, l), y) in enumerate(zip(MESH_OUT, ys)))
    steps = "".join(f'<li style="--i:{i}"><em>0{i + 1}</em>{esc(s)}</li>' for i, s in enumerate(HUB_STEPS))
    return f"""<figure class="fl" aria-label="Official regulations and manuals flow into the Oddly Sunny Engine, which feeds Aviator IQ, Mariner IQ, DMV IQ and Insurance Pass">
  <div class="fl-stage">
    {svg}
    <div class="fl-cap fl-cap-l">Official sources</div><div class="fl-cap fl-cap-r">Live products</div>
    <ul class="fl-col fl-l">{src}<li class="fl-more"><em>+</em>USCIS, IRCC, FCC and provincial agencies</li></ul>
    <div class="fl-hub">{mark("fl-mark")}<span class="fl-kick">One engine</span><b>Oddly Sunny Engine</b><ol>{steps}</ol></div>
    <ul class="fl-col fl-r">{out}<li class="fl-more"><em>+</em>Citizen Pass, Drive IQ Canada, Airwaves IQ</li></ul>
  </div>
  <div class="fl-foot"><span>Blind-checked answer keys</span><span>Page-level citations</span><span>Edition monitoring</span></div>
</figure>"""

VERTICALS = [("Mobility &amp; Transit", ["dmv-iq","drive-iq-canada"]),
             ("Aviation &amp; Marine", ["aviator-iq","mariner-iq"]),
             ("Civic &amp; Financial", ["citizen-pass","insurance-pass","airwaves-iq"])]
def tile(slug):
    p = BY[slug]
    return f'''<a class="pt" href="/work/{slug}/"><img class="pimg" src="/assets/img/{p["img"]}?v=3" alt="{esc(p["alt"])}" loading="lazy">
  <div class="cap"><div class="hd"><div><h3>{p["name"]}</h3><span>{p["host"]}</span></div></div>
  <div class="more"><p>{esc(p["short"])}</p><div class="chips"><span>{esc(p["catlabel"])}</span><span>{platforms(p)}</span></div><span class="go">Explore {ARROW}</span></div></div></a>'''

def verticals():
    return "".join(f'<div class="vt-g reveal"><h3>{g}</h3><div class="vt-row n{len(slugs)}">{"".join(tile(s) for s in slugs)}</div></div>' for g, slugs in VERTICALS)

ENGAGE = [
 ("spark","Micro-Diagnostic Sprints","Short, timed active-recall rounds built from the official question bank."),
 ("route","Missed-Question Recycling","Questions a learner misses come back in later sessions until they're answered correctly."),
 ("chart","Full-Length Exam Simulation","Mock exams that match the official question count, time limit and pass mark."),
]
def engage_ui():
    # three equal cards, each with a small looping demo (site.js "engagement cards"). California facts are real (46 questions, pass at 38)
    misses = (7, 19, 30, 41)
    dots = "".join(f'<i{" class=x" if n in misses else ""}></i>' for n in range(46))
    queue = [("Emergency vehicles", 3), ("School bus stops", 2), ("Railroad crossings", 1), ("Work zones", 1)]
    q = "".join(f'<li style="--p:{i}"{" class=now" if i == 0 else ""}><span>{t}</span><em aria-label="missed {n} times">{"".join("<i></i>" for _ in range(n))}</em></li>' for i, (t, n) in enumerate(queue))
    vis = [
     f'''<div class="eg2-mock eg2-sprint"><div class="eg2-top"><small>Right of way &middot; 4 of 10</small><span class="eg2-clock"><svg viewBox="0 0 36 36" aria-hidden="true"><circle cx="18" cy="18" r="15"/><circle class="run" cx="18" cy="18" r="15"/></svg><b>0:45</b></span></div>
        <p>Two vehicles reach a four-way stop together. Who goes first?</p>
        <div class="eg2-opts"><span><b>A</b>The larger vehicle</span><span class="ok"><b>B</b>The vehicle on the right<i>+10 XP</i></span><span><b>C</b>The vehicle on the left</span></div></div>''',
     f'''<div class="eg2-mock eg2-queue"><div class="eg2-top"><small>Coming back next session</small></div><ol>{q}</ol></div>''',
     f'''<div class="eg2-mock eg2-sim"><div class="eg2-top"><small>California knowledge test</small><em>Passed</em></div>
        <div class="eg2-dots">{dots}</div><div class="eg2-bar"><i class="eg2-fill"></i><em style="left:82.6%"><span>Pass 38</span></em></div><div class="eg2-score"><span><b class="eg2-cnt">0</b><small>/ 46 correct</small></span></div></div>''',
    ]
    return '<div class="eg2" data-eg2>' + "".join(f'''<article class="eg2-card reveal" style="--d:{i * 110}ms"><div class="eg2-vis">{v}</div><span class="eg2-n">0{i + 1}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></article>''' for i, (v, (_, t, d)) in enumerate(zip(vis, ENGAGE))) + '</div>'

def home():
    imgs, wall = hero_floats()
    feats = "".join(f'<div class="feat reveal"><div class="ic">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in CAPS)
    body = f"""
<div class="hero-pin">
<section class="hero" data-scheme="green" data-imgs='{imgs}'>
  {wall}
  <div class="wrap"><div class="copy">
    <div class="mark hero-mark" id="heroMark"><div class="cell c1"></div><div class="cell c2"></div><div class="cell c3"></div><div class="cell c4"></div></div>
    <h1>Learning,<br><i>reimagined with AI.</i></h1>
    <p class="lede">We turn complex statutes and government manuals into adaptive study tools. Seven live products, every question traced to the page it came from.</p>
    <div class="cta-row"><a class="btn btn-down" href="#platform" data-smooth>Explore the engine <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14"/><path d="m5 12 7 7 7-7"/></svg></a></div>
  </div></div>
  <a class="scroll-cue" href="#platform" data-smooth aria-label="Scroll down"><svg viewBox="140 10 150 410" fill="none" stroke="currentColor" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M215 37V393"/><path d="M161.600 339.600 215 393l53.400-53.400"/></svg></a>
</section>
</div>

<section class="sec mx-sec" id="platform" data-scheme="soft"><div class="wrap">
  <div class="mx-grid mx-wide">
    <div class="mx-copy reveal">
      <div class="eyebrow rule">Architecture &amp; ingestion pipeline</div>
      <h2 class="h2">One engine turns regulation <i>into study products.</i></h2>
      <p class="sub">Our proprietary pipeline turns statutory codes and agency handbooks into question banks where every item traces back to its source page.</p>
    </div>
    <div class="fl-wrap reveal">{flow()}</div>
  </div>
</div></section>

<section class="sec" id="verticals" data-scheme="white"><div class="wrap">
  <div class="vt-head reveal">
    <div class="eyebrow rule">Proven enterprise horizontal expansion</div>
    <h2 class="h2">Same AI engine. <i>Live across markets.</i></h2>
    <p class="sub">The Oddly Sunny architecture decouples domain ingestion from pedagogical delivery, allowing fast expansion into high-barrier regulatory markets:</p>
  </div>
  <div class="vt-groups">{verticals()}</div>
</div></section>
<section class="sec ai-sec" id="ai-tools" data-scheme="soft"><div class="wrap">
  <div class="vs-head">
    <div class="reveal">
      <div class="eyebrow rule">Proprietary AI (Sunny)</div>
      <h2 class="h2">An AI agent <i>built for learners.</i> <span class="ai-spark">{SPARK}</span></h2>
    </div>
    <p class="sub reveal">Sunny uses real tools: it searches the official handbook, pulls practice questions, starts quizzes and checks progress, then answers with the page it used.</p>
  </div>
  <div class="ai-grid">{ai_cards()}</div>
  <a class="ai-more reveal" href="/sunny/">Inspect Sunny in production {ARROW_R}</a>
</div></section>
<section id="expertise" data-scheme="white"><div class="exp">
  <div class="l">
    <div class="eyebrow rule">Verification Pipeline</div>
    <h2 class="h2">Smart enough to teach, <i>disciplined enough to trust.</i></h2>
    <p class="sub">Generative models make study sessions interactive, but unconstrained LLMs cannot be trusted with regulatory certification. We pair adaptive practice with a four-part audit that checks each question's source, its answer key and its wrong answers before it reaches learners.</p>
    <div class="feats">{feats}</div>
  </div>
  <div class="r exp-vid"><video autoplay muted loop playsinline preload="metadata" poster="/assets/img/personal-loop.jpg" aria-label="A learner using her phone outdoors in soft sunlight"><source src="/assets/img/personal-loop.webm" type="video/webm"><source src="/assets/img/personal-loop.mp4" type="video/mp4"></video></div>
</div></section>
<section class="sec" id="engagement" data-scheme="soft"><div class="wrap">
  <div class="vs-head">
    <div class="reveal">
      <div class="eyebrow rule">Engagement architecture &amp; retention</div>
      <h2 class="h2">Built for <i>daily learner retention.</i></h2>
    </div>
    <p class="sub reveal">Certification prep suffers from learner drop-off. We build retrieval practice and short daily loops into our products so learners keep coming back.</p>
  </div>
  {engage_ui()}
</div></section>
<section class="sec vs-sec" id="architecture" data-scheme="white"><div class="wrap">
  <div class="vs-head">
    <div class="reveal">
      <div class="eyebrow rule">Platform Architecture</div>
      <h2 class="h2">Legacy test publishers vs. <i>the Oddly Sunny Engine.</i></h2>
    </div>
    <p class="sub reveal">Five capabilities separate a static question bank from regulatory learning infrastructure.</p>
  </div>
  <div class="vs-table">{compare_rows(None, "Legacy test publishers", "Oddly Sunny Engine")}</div>
</div></section>

<section class="closing e-close" data-scheme="green"><div class="wrap reveal">
  <div class="eyebrow">Oddly Sunny</div>
  <h2 class="h2" style="margin-top:16px">Modernizing how <i>the world learns.</i></h2>
  <p class="body">Oddly Sunny builds AI-powered learning that brings education up to date: personal, trustworthy, and designed for how people actually learn today.</p>
  <div class="cta-row"><a class="btn" href="/contact/">Contact us {ARROW_R}</a></div>
</div></section>
"""
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "Oddly Sunny", "legalName": "Oddly Sunny LLC", "url": SITE + "/", "logo": SITE + "/apple-touch-icon.png",
           "description": "Oddly Sunny operates a proprietary, AI-native learning infrastructure platform for high-stakes licensing and certification exams."}
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Oddly Sunny", "url": SITE + "/"}
    return head_html("Oddly Sunny | Learning, Reimagined with AI",
        "We turn complex statutes and government manuals into adaptive study tools. Seven live products, every question traced to the page it came from.",
        "/", "home.jpg", [org, site]) + header().replace('class="hdr hdr-ent"', 'class="hdr hdr-ent brand-hidden away" data-away') + body + footer("green")

FLOAT_ORDER = ["cp-smile","study-library","cp-dog","study-desk","cp-denim","study-woman","cp-hoodie","cp-blonde","airwaves-man"]
FLOAT_POS = {"cp-hoodie":"18%","cp-blonde":"82%","cp-smile":"40%"}
def floats(offset=0):
    order = FLOAT_ORDER[offset:] + FLOAT_ORDER[:offset]
    imgs = json.dumps([{"n": n, "p": FLOAT_POS.get(n, "50%")} for n in order])
    wall = "".join(f'<div class="float f{i}"><img src="" alt=""></div>' for i in range(1, 9))
    return imgs, wall

RELATED = {
 "aviator-iq": ["airwaves-iq", "mariner-iq", "dmv-iq"],
 "citizen-pass": ["dmv-iq", "drive-iq-canada", "insurance-pass"],
 "dmv-iq": ["drive-iq-canada", "citizen-pass", "aviator-iq"],
 "drive-iq-canada": ["dmv-iq", "citizen-pass", "mariner-iq"],
 "insurance-pass": ["airwaves-iq", "mariner-iq", "aviator-iq"],
 "airwaves-iq": ["aviator-iq", "mariner-iq", "insurance-pass"],
 "mariner-iq": ["aviator-iq", "airwaves-iq", "insurance-pass"],
}

def pt_tile(slug):
    p = BY[slug]
    return f'''<a class="pt" href="/work/{slug}/"><img class="pimg" src="/assets/img/{p["img"]}?v=3" alt="{esc(p["alt"])}" loading="lazy">
  <div class="cap"><div class="hd"><div><h3>{p["name"]}</h3><span>{p["host"]}</span></div></div>
  <div class="more"><p>{esc(p["short"])}</p><div class="chips"><span>{esc(p["catlabel"])}</span><span>{platforms(p)}</span></div><span class="go">Read the story {ARROW}</span></div></div></a>'''

STAGE_BG = {
 "aviator-iq": ("#E7D9BF", "#B98E5A"),
 "citizen-pass": ("#3A4C78", "#1A2640"),
 "dmv-iq": ("#6E9482", "#2F4E41"),
 "drive-iq-canada": ("#B8404A", "#5C1A22"),
 "insurance-pass": ("#E3A883", "#A55F3E"),
 "airwaves-iq": ("#3F8C7E", "#16443C"),
 "mariner-iq": ("#3F74B3", "#14305A"),
}

def stage(p):
    """Static browser window built from a real screenshot of the product's Pro screens (desktop only)."""
    from PIL import Image
    slug = p["slug"]
    dw, dh = Image.open(os.path.join(ROOT, f"assets/img/shots/{slug}-d.jpg")).size
    c1, c2 = STAGE_BG[slug]
    dpct = round(100 * (1 - (11 / 16) / (dh / dw)), 1)
    return f"""<div class="stage" role="img" aria-label="A screen from {p['name']}" style="--dd:-{dpct}%;--c1:{c1};--c2:{c2};--bgimg:url(/assets/img/bg/{slug}.jpg)">
  <div class="win"><div class="bar"><i></i><i></i><i></i><span>{p['host']}</span></div>
    <div class="vp"><img src="/assets/img/shots/{slug}-d.jpg?v=3" alt="" width="{dw}" height="{dh}"></div></div>
</div>"""

GAMES = [
 ("sprint","Sign Sprint","Sort road signs by type before the timer runs out."),
 ("fact","Fact Check","Swipe statements from the {region}'s material true or false."),
 ("flash","Flash Cards","Scratch to reveal the answer, then say honestly if you knew it."),
 ("match","Sign Match","Flip cards to pair road signs from memory."),
 ("numbers","By the Numbers","Spin to the exact distance, fine or time limit from your {region}'s questions."),
]
# per product: clip folder under assets/img/, and the word for its jurisdiction
GAME_SETS = {"dmv-iq": ("games", "state"), "drive-iq-canada": ("games/drive-iq-canada", "province")}

PLAY_JSON = '{"fact": [{"q": "A red octagon always means stop.", "a": true}, {"q": "Green signs warn you about hazards ahead.", "a": false, "why": "Green signs give directions. Yellow ones warn."}, {"q": "An upside-down triangle means yield.", "a": true}, {"q": "Orange signs mark work zones.", "a": true}, {"q": "A round yellow sign means a roundabout is ahead.", "a": false, "why": "A round yellow sign means a railroad crossing is ahead."}, {"q": "A five-sided sign marks a school zone or crossing.", "a": true}], "flash": [{"tag": "Driving", "q": "A flashing red traffic light means…", "a": "Stop, then go when it\'s safe"}, {"tag": "Citizenship", "q": "How many U.S. Senators are there?", "a": "100"}, {"tag": "Aviation", "q": "Which wingtip carries the red position light?", "a": "Left"}, {"tag": "Boating", "q": "Facing forward on a boat, port is…", "a": "Left"}, {"tag": "Ham radio", "q": "On the air, “CQ” means…", "a": "Calling any station"}, {"tag": "Driving", "q": "A solid yellow line on your side of the road means…", "a": "No passing from your side"}], "match": [["R1-1", "Stop"], ["R1-2", "Yield"], ["W10-1", "Railroad crossing ahead"], ["S1-1", "School crossing"], ["R5-1", "Do not enter"], ["W20-1", "Road work ahead"]]}'

HEART = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.500-4.600-9.600-9.300C.900 8.300 3 4.500 6.700 4.500c2.200 0 3.700 1.300 5.300 3.200 1.600-1.900 3.100-3.200 5.300-3.200 3.700 0 5.800 3.800 4.300 7.200C19.500 16.400 12 21 12 21z"/></svg>'

def games_block(p):
    """Gamification showcase on a product page: the real Challenges screen plus each game's animated intro art.
    Renders nothing until the product's clips are in assets/img/<folder>/."""
    folder, region = GAME_SETS[p["slug"]]
    if not os.path.exists(os.path.join(ROOT, f"assets/img/{folder}/challenges.jpg")): return ""
    d = f"/assets/img/{folder}"
    tiles = "".join(f'''<figure class="gm-tile reveal"><video autoplay muted loop playsinline preload="metadata" poster="{d}/{k}.jpg" aria-hidden="true"><source src="{d}/{k}.webm" type="video/webm"><source src="{d}/{k}.mp4" type="video/mp4"></video><figcaption><b>{esc(t)}</b><span>{esc(x.format(region=region))}</span></figcaption></figure>''' for k, t, x in GAMES)
    return f'''<div class="gm">
  <figure class="gm-phone reveal"><img src="{d}/challenges.jpg" alt="The Challenges screen in the {p['name']} app: Exam Simulator, Quick Quiz, Practice Test and daily games" width="520" height="1129" loading="lazy"></figure>
  <div class="gm-grid">{tiles}</div>
</div>
'''

def product(p):
    i = FEATURED_ORDER.index(p["slug"])
    nxt = BY[FEATURED_ORDER[(i+1) % len(FEATURED_ORDER)]]
    st = STORIES[p["slug"]]
    nst = STORIES[nxt["slug"]]
    body_html = ""
    for kind, text in st["body"]:
        if kind == "p": body_html += f"<p>{esc(text)}</p>\n"
        elif kind == "h": body_html += f"<h2>{esc(text)}</h2>\n"
        elif kind == "games": body_html += games_block(p)
        else: body_html += f'<blockquote class="pull">{esc(text)}</blockquote>\n'
    rows = ""
    for label, links in p["apps"]:
        rows += f'<div class="get-row"><small>{esc(label)}</small>{"".join(store_btn(k, u) for k, u in links)}</div>'
    # unavailable apps are simply left out: no "coming soon" or "web only" notes
    web = f'<a class="btn" href="{p["url"]}" target="_blank" rel="noopener">Visit {p["host"]} {ARROW}</a>'
    body = f"""
<section class="story" data-scheme="paper">
  <article>
    <header class="s-head">
      <div class="s-label">{p['name']}</div>
      <h1 class="s-title">{esc(st['headline'])}</h1>
      <p class="s-dek">{esc(st['dek'])}</p>
      <div class="s-by">By Oddly Sunny</div>
    </header>
    <figure class="s-fig"><div class="s-frame">{stage(p)}</div><figcaption>A look inside {p['name']}.</figcaption></figure>
    <div class="s-layout">
      <aside class="s-side" id="get" aria-label="Where to find {p['name']}">
        <div class="s-side-title">Find {p['name']}</div>
        <a class="btn" href="{p["url"]}" target="_blank" rel="noopener">Visit {p["host"]} {ARROW}</a>
        <div class="get-links">{rows}</div>
      </aside>
      <div class="s-col">
        <div class="s-body">
{body_html}        </div>
      </div>
    </div>
  </article>
</section>
<section class="s-more" data-scheme="paper"><div class="wrap">
  <div class="eyebrow">Keep exploring</div>
  <h2 class="h2">More from Oddly Sunny</h2>
  <div class="more-grid">{"".join(pt_tile(x) for x in RELATED[p["slug"]])}</div>
</div></section>
"""
    app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": p["name"], "applicationCategory": "EducationalApplication", "operatingSystem": platforms(p),
           "url": p["url"], "description": p["lede"], "publisher": {"@type": "Organization", "name": "Oddly Sunny", "url": SITE + "/"}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Oddly Sunny", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": p["name"], "item": f"{SITE}/work/{p['slug']}/"}]}
    return head_html(SEO_TITLE[p["slug"]], f"{p['name']}: {p['lede']}", f"/work/{p['slug']}/", p["slug"] + ".jpg", [app, crumbs]) + header() + body + footer("paper")


CONTACT_ENDPOINT = "https://oddlysunny-contact-496288753459.us-central1.run.app"  # set to a form service URL (for example a Formspree endpoint) to send messages without the visitor's email app

def contact_page():
    body = f"""
<section class="story contact" data-scheme="paper">
  <div class="c-wrap">
    <div class="s-label">Contact</div>
    <h1 class="s-title">Get in touch.</h1>
    <p class="s-dek">Send us a message and our team will get back to you.</p>
    <div class="c-grid">
      <form class="c-form" id="contactForm" novalidate data-endpoint="{CONTACT_ENDPOINT}" data-mail="{MAIL}">
        <label>Name<input name="name" type="text" autocomplete="name" required></label>
        <label>Email<input name="email" type="email" autocomplete="email" required></label>
        <label>Message<textarea name="message" rows="7" required></textarea></label>
        <input class="hp" name="website" type="text" tabindex="-1" autocomplete="off" aria-hidden="true">
        <button class="btn" type="submit">Send message {ARROW}</button>
        <p class="c-note" id="contactNote" role="status"></p>
      </form>
      <aside class="c-side">
        <div class="s-side-title">We can help with</div>
        <ul>
          <li>Partnerships and licensing</li>
          <li>Press and media</li>
          <li>Research and speaking requests</li>
          <li>Product support</li>
        </ul>
        <div class="s-side-title" style="margin-top:28px">Prefer email?</div>
        <p>Write to us at <a href="mailto:{MAIL}">{MAIL}</a>. We usually reply within a day or two.</p>
      </aside>
    </div>
  </div>
</section>
"""
    return head_html("Contact | Oddly Sunny", "Get in touch with the Oddly Sunny team.", "/contact/", "home.jpg") + header() + body + footer("paper")


SUNNY_EXAMPLES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunny_examples.json"), encoding="utf-8"))

# Cases that show the cards Sunny puts in the chat (quiz, course, progress). Merged after each industry's first transcript.
SUNNY_WIDGET_CASES = {
 "driving": [
  {"label": "Quiz me", "ctx": "Car permit test, after a lesson on right of way", "q": "Quiz me on right of way",
   "a": "Here is a quick round on right of way, starting with the kind of question you missed last time.",
   "cites": [], "choices": ["Another round", "Explain the four-way stop", "What's next?"],
   "ui": {"type": "quiz", "title": "Right of way", "items": [
     {"q": "Two cars reach a four-way stop at the same time. Who goes first?", "o": ["The car on the left", "The car on the right", "The bigger vehicle"], "a": 1},
     {"q": "An ambulance with its siren on comes up behind you. What do you do?", "o": ["Speed up to clear the lane", "Pull to the right and stop", "Stop where you are"], "a": 1},
     {"q": "A traffic light is flashing yellow. You should…", "o": ["Stop and wait for green", "Slow down and go with care", "Speed up to get through"], "a": 1}]}},
  {"label": "What's next?", "ctx": "Car permit test, a returning learner", "q": "What should I learn next?",
   "a": "You've finished **4 of 9** topics in your course. Next up is **Speed limits**. Want the short lesson first, or a quick quiz to see what you already know?",
   "cites": [], "choices": ["Start the lesson", "Quiz me first", "How ready am I?"],
   "ui": {"type": "path", "title": "Your course", "sub": "Car permit test", "now": 4, "steps": ["Getting your permit", "Road signs", "Signals and markings", "Right of way", "Speed limits", "Sharing the road", "Night and bad weather", "Alcohol and drugs", "Emergencies"]}},
  {"label": "Am I ready?", "ctx": "Car permit test, a week before the test", "q": "Am I ready for my test?",
   "a": "You're **72% ready**. Road signs and right of way are strong. Speed limits and the alcohol rules are pulling your score down, so that is where 15 minutes today would help most.",
   "cites": [], "choices": ["Quiz me on speed limits", "Make me a plan", "Show my weak spots"],
   "ui": {"type": "progress", "ready": 72, "topics": [["Road signs", 94], ["Right of way", 86], ["Signals and markings", 78], ["Speed limits", 52], ["Alcohol and drugs", 48]]}},
 ],
 "aviation": [
  {"label": "Learning path", "ctx": "Private Pilot knowledge test, studying the handbook in order", "q": "Teach me the handbook from the start. Where am I?",
   "a": "You're on **chapter 5, Aerodynamics of Flight**, with the first four chapters done. Let's pick up with the four forces: lift, weight, thrust and drag.",
   "cites": [{"title": "Pilot's Handbook of Aeronautical Knowledge", "locator": "Chapter 5"}], "choices": ["Start chapter 5", "Recap chapter 4", "Quiz me on chapter 4"],
   "ui": {"type": "path", "title": "Your course", "sub": "Pilot's Handbook of Aeronautical Knowledge", "now": 4, "steps": ["Introduction to Flying", "Aeronautical Decision-Making", "Aircraft Construction", "Principles of Flight", "Aerodynamics of Flight", "Flight Controls", "Aircraft Systems", "Flight Instruments", "Flight Manuals and Other Documents"]}},
 ],
}
for _ind in SUNNY_EXAMPLES:
    _ind["cases"] = _ind["cases"][:1] + SUNNY_WIDGET_CASES.get(_ind["key"], []) + _ind["cases"][1:]

def sunny_widget(u):
    """The cards Sunny shows inside a reply: a quiz, a course with the learner's place in it, or a progress read."""
    if not u:
        return ""
    if u["type"] == "quiz":
        qs = "".join(f'<div class="sw-qq{" on" if i == 0 else ""}" data-a="{it["a"]}"><p>{esc(it["q"])}</p><div class="sw-qo">' + "".join(f'<button type="button">{esc(o)}</button>' for o in it["o"]) + '</div></div>' for i, it in enumerate(u["items"]))
        dots = "<i></i>" * len(u["items"])
        return f'<div class="sw sw-quiz" data-quiz><div class="sw-top"><b>{esc(u["title"])}</b><span class="sw-dots">{dots}</span></div>{qs}<div class="sw-done"><span class="sw-score"></span><small>Missed ones go back into your study plan.</small></div></div>'
    if u["type"] == "path":
        n, steps = u["now"], u["steps"]
        li = "".join(f'<li class="{"done" if i < n else "now" if i == n else ""}" style="--i:{i}"><i></i><span>{esc(t)}</span>' + ('<em>You are here</em>' if i == n else "") + '</li>' for i, t in enumerate(steps))
        return f'<div class="sw sw-path"><div class="sw-top"><b>{esc(u["title"])}</b><small>{esc(u["sub"])}</small></div><div class="sw-bar"><i style="--w:{n / len(steps):.3f}"></i></div><small class="sw-meta">{n} of {len(steps)} topics done</small><ol>{li}</ol></div>'
    if u["type"] == "progress":
        r = u["ready"]; low = min(u["topics"], key=lambda t: t[1])[0]
        bars = "".join(f'<li class="{"low" if v < 60 else ""}" style="--i:{i}"><span>{esc(t)}</span><b>{v}%</b><i style="--w:{v / 100:.2f}"></i></li>' for i, (t, v) in enumerate(u["topics"]))
        return f'<div class="sw sw-prog"><div class="sw-ring" style="--r:{r / 100:.2f}"><svg viewBox="0 0 80 80" aria-hidden="true"><circle cx="40" cy="40" r="34"/><circle class="v" cx="40" cy="40" r="34"/></svg><span><b>{r}%</b><small>ready</small></span></div><ul>{bars}</ul><small class="sw-meta">From your study record. Weakest topic: {esc(low)}.</small></div>'
    return ""


def sunny_mascot(size, cls=""):
    """Sunny's face is drawn over the plain cloud image, the same way as on dmv-iq.com."""
    return (f'<span class="sn-mascot {cls}" style="width:{size}px;height:{size}px" aria-hidden="true"><span class="cm-body">'
            f'<img src="/assets/img/sunny/sunny-256.webp" alt="" width="{size}" height="{size}" draggable="false">'
            '<span class="cm-face"><span class="cm-blush cm-l"></span><span class="cm-blush cm-r"></span><span class="cm-eyes">'
            '<span class="cm-socket cm-l"></span><span class="cm-socket cm-r"></span><span class="cm-eye cm-l"></span><span class="cm-eye cm-r"></span>'
            '</span></span></span></span>')

def md_lite(t):
    """Sunny's replies use bold and short lists only."""
    out, lst = [], []
    def flush():
        if lst:
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in lst) + "</ul>"); lst.clear()
    for line in t.split("\n"):
        line = line.strip()
        if not line:
            flush(); continue
        h = esc(line)
        h = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", h)
        if line.startswith(("- ", "• ")):
            lst.append(h[2:])
        else:
            flush(); out.append(f"<p>{h}</p>")
    flush()
    return "".join(out)

COMPARE = [
 ("ingest","Curriculum Ingestion","Built directly from official handbooks and regulations, with edition monitoring that flags new versions for fast updates.","Manual editorial cycles per jurisdiction."),
 ("adapt","Pedagogical Adaptation","Weak topics surface first, and missed questions come back until they're mastered.","Static multiple-choice banks and linear, one-size-fits-all pathways."),
 ("verify","Factual Integrity","Every question traced to its source page and checked against the official text.","Unvetted AI answers or outdated printed answer keys."),
 ("gauge","Predictive Readiness","A readiness score that blends coverage, accuracy, recall and speed, measured against the official pass mark.","Flat completion percentages and uncalibrated scores."),
 ("cells","Horizontal Scalability","Reusable modular ingestion architecture deployable to new state, federal, or international domains in weeks.","Prohibitive cost and editorial overhead to expand across regional jurisdictions."),
]

SPARK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M10 2.500c.5 4.300 2.700 6.500 7 7-4.300.5-6.500 2.700-7 7-.5-4.300-2.700-6.500-7-7 4.300-.5 6.500-2.700 7-7zm8 10c.3 2.300 1.300 3.300 3.500 3.500-2.200.3-3.200 1.300-3.500 3.500-.3-2.200-1.300-3.200-3.500-3.500 2.200-.2 3.200-1.200 3.500-3.500z"/></svg>'

def ai_cards():
    btn = lambda t: f'<span class="ai-btn">{SPARK}{t}</span>'
    tick = '<i class="ai-tick"></i>'
    mocks = [
     ("ask", "Ask Sunny", f'''<div class="ai-mock"><b class="ai-mt">Ask Sunny</b>
        <div class="ai-q">Why is B wrong?</div>
        <div class="ai-dots" aria-hidden="true"><i></i><i></i><i></i></div>
        <div class="ai-a">Stop first, then pass at no more than 15 mph.</div>
        <span class="ai-cite">{icon("book")}p. 80 · Driver Manual</span></div>''', "Answers learners can verify",
      "Learners ask in plain language. Sunny answers only from the official manual, returns the page it used and checks every number before it is displayed."),
     ("quiz", "Generate quiz", f'''<div class="ai-mock"><b class="ai-mt">Quiz generator</b>
        <div class="ai-sel">Right of way<span>▾</span></div>
        <div class="ai-list"><small>Detected weak spots</small><span>{tick}Intersections</span><span>{tick}Pedestrians</span><span>{tick}Emergency vehicles</span></div></div>''', "Quizzes generated on demand",
      "Any topic becomes a fresh quiz in seconds, or Sunny targets the topics a learner keeps missing. Every question traces to the official source."),
     ("plan", "Build my plan", f'''<div class="ai-mock"><b class="ai-mt">Study plan</b>
        <div class="ai-row"><small>Test date</small><span>Nov 14</span></div>
        <div class="ai-row"><small>Time per day</small><span>20 min</span></div>
        <div class="ai-bar"><i style="width:62%"></i></div><small class="ai-note">62% ready · on track</small></div>''', "Plans paced to the exam date",
      "Candidates set a test date. Sunny builds a plan around it, adjusts as performance improves and reports readiness against the real pass mark."),
    ]
    # studio-backdrop colours taken from the hero headshots (teal, coral, olive): no people, just the set
    tones = {"ask": ("#6FB2B8", "#2E7680", "#52603F"), "quiz": ("#E39B92", "#B4605B", "#7A3E52"), "plan": ("#93A06C", "#56603E", "#B08A38")}
    return "".join(f'''<article class="ai-card reveal" style="--d:{i * 110}ms">
      <div class="ai-vis ai-studio" style="--s1:{tones[img][0]};--s2:{tones[img][1]};--s3:{tones[img][2]}">{mock}{btn(b)}</div>
      <h3>{esc(t)}</h3><p>{esc(d)}</p>
    </article>''' for i, (img, b, mock, t, d) in enumerate(mocks))

SUNNY_VS = [
 ("book","Where answers come from","A closed library of the official manuals for that exam","Its memory of everything it has read, accurate or not"),
 ("globe","Whose rules","Only your state's handbook, never another state's","Can blend one state's rule with another's"),
 ("chart","Numbers","Every number checked against the source before you see it","Stated with confidence, with nothing to check them against"),
 ("chat","When it doesn't know","Cites the page, or says the manual is silent","Fills the gap with something that sounds right"),
]

def compare_rows(rows=None, old="The old way", new="With Oddly Sunny"):
    rows = rows or COMPARE
    head = f'<div class="vs-row vs-hd" aria-hidden="true"><span></span><span class="vs-old">{esc(old)}</span><span class="vs-new"><b class="vs-brand">{esc(new)}</b></span></div>'
    return head + "".join(f'''<div class="vs-row reveal" style="--d:{i * 60}ms">
      <h3 class="vs-k"><span class="vs-icon">{icon(ic)}</span>{esc(k)}</h3>
      <p class="vs-old"><span class="sr-only vs-ml">{esc(old)} </span>{esc(t)}</p>
      <p class="vs-new"><span class="sr-only vs-ml">{esc(new)} </span>{esc(u)}</p>
    </div>''' for i, (ic, k, u, t) in enumerate(rows))

SUNNY_HOW = [
 ("phone","Conversational by design","Learners talk to Sunny the way they would talk to a tutor: in their own words, in the middle of a question or the night before the test. Sunny turns each message into the next useful step: an explanation, a lesson, a quiz or a plan."),
 ("book","Keeps the context","Sunny holds the thread of every conversation and sees the question on the learner's screen, so a follow-up like \"why not B?\" or \"give me another one\" just works, without repeating anything."),
 ("chart","Learns the learner","Every answer a learner gives updates what Sunny knows about them: their test, their date, the topics they have mastered and the ones they keep missing. Each session starts from that picture, never from zero."),
 ("spark","Adapts as they study","Sunny paces the plan to the test date, quizzes on weak spots and moves on once a topic is solid. Readiness comes from our own scoring model, so the guidance is measured, not guessed."),
 ("check","Grounded in the official source","Each brand connects Sunny to a closed library of the official material behind its exam, from state handbooks to federal regulations. Every answer comes from that text, with the page or rule to prove it."),
 ("globe","One engine, every exam, localized","A single domain-neutral engine powers every brand. Each one plugs in its own sources, exam rules and question bank, and Sunny meets learners in their own language."),
]

SUNNY_RESPONSIBLE = [
 ("Grounded answers, no guesswork","Sunny answers from the official text it retrieves for each question, not from general knowledge, which removes the usual source of AI hallucinations."),
 ("Every number checked first","Each number in an answer, from a speed limit to a fee, is checked against the source before the learner sees it. An answer that fails the check is corrected before it is ever shown."),
 ("Honest about what it doesn't know","When the official source is silent, Sunny says so and points to where to check. A missing fact is always better than an invented one."),
 ("Authority stays with the source","Sunny cites the page or rule behind each answer. Where our own explanation and the official source ever disagree, the source wins and Sunny says so."),
 ("Empathic, not just accurate","Sunny is warm, calm and patient. It notices when a learner is anxious and keeps the next step small and doable, because confidence is part of passing."),
]

def sunny_page():
    BOOK = icon("book")
    tabs, panels = "", ""
    for i, ind in enumerate(SUNNY_EXAMPLES):
        on = " on" if i == 0 else ""
        tabs += f'<button type="button" class="sd-tab{on}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-ind="{ind["key"]}" style="--hue:{ind["hue"]}"><i></i>{esc(ind["label"])}</button>'
        cases = "".join(f'<button type="button" class="sd-case{" on" if j == 0 else ""}" data-case="{j}">{esc(c["label"])}</button>' for j, c in enumerate(ind["cases"]))
        convs = ""
        for j, c in enumerate(ind["cases"]):
            cites = "".join(f'<span class="sd-src">{BOOK}<span><b>{esc(x["locator"] or x["title"])}</b>{("<small>" + esc(x["title"]) + "</small>") if x["locator"] else ""}</span></span>' for x in c["cites"])
            chips = "".join(f'<span class="sd-chip">{esc(o)}</span>' for o in c["choices"])
            convs += f"""<div class="sd-conv{" on" if j == 0 else ""}" data-case="{j}">
  <div class="sd-ctx">{esc(c["ctx"])}</div>
  <div class="sd-q">{esc(c["q"])}</div>
  <div class="sd-typing" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="sd-a">{md_lite(c["a"])}{sunny_widget(c.get("ui"))}{('<div class="sd-srcs">' + cites + '</div>') if cites else ""}{('<div class="sd-chips">' + chips + '</div>') if chips else ""}</div>
</div>"""
        panels += f'<div class="sd-panel{on}" role="tabpanel" data-ind="{ind["key"]}" style="--hue:{ind["hue"]}"><div class="sd-cases">{cases}</div><div class="sd-win"><div class="sd-head">{sunny_mascot(34, "sm tint")}<div><b>Sunny</b><small>{esc(ind["label"])} coach</small></div></div><div class="sd-body">{convs}</div></div></div>'
    demo = f'''<div class="sd" data-sd>
      <div class="sd-tabs" role="tablist" aria-label="Industries">{tabs}</div>
      {panels}
    </div>'''
    how = "".join(f'<div class="feat reveal"><div class="ic">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in SUNNY_HOW)
    resp = "".join(f'<div class="sn-r reveal"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in SUNNY_RESPONSIBLE)
    body = f"""
<section class="story sn" data-scheme="paper">
  <header class="s-head sn-head">
    <div class="sn-hero-mascot">{sunny_mascot(120)}</div>
    <div class="s-label">Sunny</div>
    <h1 class="s-title">The AI study coach that looks it up, instead of making it up.</h1>
    <p class="s-dek">Sunny is our proprietary, conversational AI coach, built for education from the ground up. It answers only from the official manual behind each exam, shows the page it used and checks the facts before it speaks, so learners get the warmth of a great tutor without the guesswork of a chatbot.</p>
  </header>

  <div class="sn-wrap">
    <h2 class="sn-h2">The antidote to AI hallucinations</h2>
    <p class="sn-sub">General-purpose chatbots learn from a blend of the whole internet. Ask one about a driving rule and it may sound certain while quoting the wrong speed limit, inventing a fee or mixing up California's right-of-way rule with New York's. On a test, a confident wrong answer is worse than no answer. Sunny was designed around that problem from day one.</p>
    <div class="vs-table sn-vt">{compare_rows(SUNNY_VS, "A general chatbot", "Sunny")}</div>
  </div>

  <div class="sn-wrap">
    <div class="sd-intro">
      <h2 class="sn-h2">One coach, every kind of exam</h2>
      <p class="sn-sub">Pick an industry and a use case to see how Sunny answers: from the official source, with the quizzes, study plans and progress cards it puts right in the chat.</p>
    </div>
    {demo}
  </div>

  <div class="sn-wrap">
    <h2 class="sn-h2">How it works</h2>
    <p class="sn-sub">Sunny is a conversational AI built for education from the ground up. It does more than answer questions: it gets to know each learner and coaches them all the way to test day.</p>
    <div class="feats sn-feats">{how}</div>
  </div>

  <div class="sn-wrap">
    <h2 class="sn-h2">Responsible AI, by design</h2>
    <p class="sn-sub">In education, safety means not teaching people the wrong thing. Accuracy, authority and empathy are built into how Sunny works, not added afterward. These are the methods we use to keep it valid and trustworthy.</p>
    <div class="sn-resp">{resp}</div>
  </div>
</section>
<script>
(function(){{
  var root=document.querySelector('[data-sd]'); if(!root) return;
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var timer=0;
  function play(conv){{
    if(!conv) return; clearTimeout(timer);
    conv.classList.remove('typed','asked'); conv.classList.add('pre');
    void conv.offsetWidth;
    requestAnimationFrame(function(){{
      conv.classList.remove('pre'); conv.classList.add('asked');
      timer=setTimeout(function(){{conv.classList.add('typed');}}, still?0:900);
    }});
  }}
  function show(panel, j){{
    panel.querySelectorAll('.sd-case').forEach(function(b){{b.classList.toggle('on', b.dataset.case==j);}});
    panel.querySelectorAll('.sd-conv').forEach(function(c){{var on=c.dataset.case==j; if(on){{c.classList.remove('typed','asked'); c.classList.add('pre');}} c.classList.toggle('on',on); if(on){{panel.querySelector('.sd-body').scrollTop=0; play(c);}}}});
  }}
  root.querySelectorAll('.sd-tab').forEach(function(t){{
    t.addEventListener('click',function(){{
      root.querySelectorAll('.sd-tab').forEach(function(x){{var on=x===t; x.classList.toggle('on',on); x.setAttribute('aria-selected',on);}});
      root.querySelectorAll('.sd-panel').forEach(function(p){{var on=p.dataset.ind===t.dataset.ind; p.classList.toggle('on',on); if(on) show(p,'0');}});
    }});
  }});
  root.querySelectorAll('[data-quiz]').forEach(function(w){{
    var qs=w.querySelectorAll('.sw-qq'), dots=w.querySelectorAll('.sw-dots i'), i=0, score=0;
    qs.forEach(function(q,qi){{
      q.querySelectorAll('button').forEach(function(b,bi){{
        b.addEventListener('click',function(){{
          if(q.classList.contains('answered')) return; q.classList.add('answered');
          var ok=bi==q.dataset.a; if(ok) score++;
          b.classList.add(ok?'right':'wrong'); q.querySelectorAll('button')[q.dataset.a].classList.add('right');
          dots[qi].classList.add(ok?'right':'wrong');
          setTimeout(function(){{
            q.classList.remove('on'); i++;
            if(i<qs.length) qs[i].classList.add('on');
            else {{ w.querySelector('.sw-score').textContent=score+' of '+qs.length+' right'+(score===qs.length?'. Perfect.':''); w.classList.add('fin'); }}
          }},900);
        }});
      }});
    }});
  }});
  root.querySelectorAll('.sd-panel').forEach(function(p){{
    p.querySelectorAll('.sd-case').forEach(function(b){{b.addEventListener('click',function(){{show(p,b.dataset.case);}});}});
  }});
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{play(root.querySelector('.sd-panel.on .sd-conv.on'));io.disconnect();}}}});}},{{threshold:.3}});
  io.observe(root);
}})();
</script>
"""
    return head_html("Sunny, our AI study coach | Oddly Sunny",
        "Sunny is Oddly Sunny's AI study coach built to avoid hallucinations: it answers only from official manuals, cites the page and checks every number before it replies.",
        "/sunny/", "home.jpg") + header() + body + footer("paper")

def not_found_page():
    """GitHub Pages serves /404.html for any missing path, so every link and asset here is absolute."""
    tiles = "".join(f'<a href="/work/{p["slug"]}/">{p["name"]}<span>{esc(p["catlabel"])}</span></a>' for p in [BY[s] for s in FEATURED_ORDER])
    body = f"""
<section class="story contact nf" data-scheme="paper">
  <div class="c-wrap">
    <div class="s-label">404</div>
    <h1 class="s-title">This page took a wrong turn.</h1>
    <p class="s-dek">The page you were looking for isn't here. It may have moved, or the link may be out of date.</p>
    <div class="nf-actions">
      <a class="btn" href="/">Back to home {ARROW_R}</a>
      <a class="nf-link" href="/contact/">Tell us about a broken link</a>
    </div>
    <div class="nf-list"><div class="s-side-title">Or visit one of our learning brands</div><div class="nf-grid">{tiles}</div></div>
  </div>
</section>
"""
    head = head_html("Page not found | Oddly Sunny", "The page you were looking for isn't here. Head back to Oddly Sunny or visit one of our learning brands.", "/404.html", "home.jpg")
    head = head.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="noindex">', 1)
    return head + header() + body + footer("paper")

if __name__ == "__main__":
    write("index.html", home())
    write("404.html", not_found_page())
    write("sunny/index.html", sunny_page())
    write("contact/index.html", contact_page())
    for p in PRODUCTS:
        write(f"work/{p['slug']}/index.html", product(p))
    urls = ["/", "/sunny/", "/contact/"] + [f"/work/{p['slug']}/" for p in PRODUCTS] + ["/privacy/"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", 2 + len(PRODUCTS), "pages")
