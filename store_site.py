#!/usr/bin/env python3
"""Build the BYOK Store static site + catalog.json from Factory specs and the bespoke apps."""
import json, glob, os, colorsys, sys
sys.path.insert(0, "/root/claude/Factory")
OUT = "/root/claude/Store/site"
os.makedirs(f"{OUT}/icons", exist_ok=True)
exec(open("/root/claude/Factory/gen.py").read().split("def hx(")[0].split("GLYPHS = ")[0])  # noqa: imports only
GLYPHS = eval(open("/root/claude/Factory/gen.py").read().split("GLYPHS = ")[1].split("\ndef hx(")[0])

def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
def tone(h, l, s=None):
    hh, ll, ss = colorsys.rgb_to_hls(*hx(h)); r, g, b = colorsys.hls_to_rgb(hh, l, ss if s is None else s)
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c * 255))) for c in (r, g, b))

apps = []
for p in sorted(glob.glob("/root/claude/Factory/specs/*.json")):
    s = json.load(open(p)); pid = s["id"]
    apps.append({"id": pid, "name": s["name"], "tagline": s["tagline"], "category": s["category"], "about": s["about"],
        "colors": s["colors"], "icon": s.get("icon", "spark"), "package": f"com.mohithash.byok.{pid.replace('_','')}",
        "tools": [{"emoji": t["emoji"], "title": t["title"], "subtitle": t["subtitle"]} for t in s["tools"]],
        "apk": f"https://github.com/Mohithash/byok-factory/releases/download/{pid}-v1.0/{pid}-v1.0.apk",
        "aab": f"https://github.com/Mohithash/byok-factory/releases/download/{pid}-v1.0/{pid}-v1.0.aab",
        "source": "https://github.com/Mohithash/byok-factory", "listing": f"https://github.com/Mohithash/byok-factory/blob/main/listings/{pid}.md", "kind": "factory",
        "released": os.path.exists(f"/root/claude/Factory/dist/{pid}-v1.0.aab")})

BESPOKE = [
 ("CalorieBank", "Calorie Bank", "Weight to lose as a kcal balance you spend down daily", "Health & Fitness", ["#1B5E4A", "#8A5A00", "#00658E"], "coin", "Bank model with daily settlement, zero-date estimate, water tracker and photo/text calorie estimation.", "v1.2", "CalorieBank-v1.2-release.apk", "CalorieBank-v1.2-release.aab", "com.mohithash.caloriebank"),
 ("PantryChef", "Pantry Chef", "Cook from what you have", "Food & Drink", ["#D9481F", "#2E7D32", "#F9A825"], "leaf", "Fridge photo → pantry, recipes with have/need markers, cook mode, grocery list.", "v1.0", "PantryChef-v1.0.apk", "PantryChef-v1.0.aab", "com.mohithash.pantrychef"),
 ("Mindstream", "Mindstream", "A quiet place to think", "Lifestyle", ["#5B4BC4", "#E86A8A", "#2A9D8F"], "moon", "Journaling with mood, AI reflections, weekly insight and streaks.", "v1.0", "Mindstream-v1.0.apk", "Mindstream-v1.0.aab", "com.mohithash.mindstream"),
 ("LingoLoop", "Lingo Loop", "Speak from day one", "Education", ["#1565C0", "#FF7043", "#26A69A"], "chat", "Role-play language tutor with corrections and auto flashcards (SM-2).", "v1.0", "LingoLoop-v1.0.apk", "LingoLoop-v1.0.aab", "com.mohithash.lingoloop"),
 ("Ledgerly", "Ledgerly", "Know where it goes", "Finance", ["#00695C", "#F4B400", "#6A4CB0"], "coin", "Receipt photo → expense, budgets, donut/trend charts, monthly insight.", "v1.0", "Ledgerly-v1.0.apk", "Ledgerly-v1.0.aab", "com.mohithash.ledgerly"),
 ("RepCoach", "Rep Coach", "Train with a plan", "Health & Fitness", ["#C62828", "#FFB300", "#00838F"], "dumbbell", "Generated programme, set logging, post-session coach review, PRs.", "v1.0", "RepCoach-v1.0.apk", "RepCoach-v1.0.aab", "com.mohithash.repcoach"),
 ("Cram", "Cram", "Study smarter", "Education", ["#7B1FA2", "#FFC107", "#0097A7"], "book", "Notes or a textbook photo → summary, flashcards, quiz, grounded tutor.", "v1.0", "Cram-v1.0.apk", "Cram-v1.0.aab", "com.mohithash.cram"),
 ("TripWeaver", "Trip Weaver", "Trips, woven for you", "Travel & Local", ["#0277BD", "#FF8F00", "#2E7D32"], "plane", "Neighbourhood-grouped itineraries, redo-a-day, packing list, tips, phrases.", "v1.0", "TripWeaver-v1.0.apk", "TripWeaver-v1.0.aab", "com.mohithash.tripweaver"),
 ("Braindump", "Braindump", "Get it out of your head", "Productivity", ["#3949AB", "#FF6F00", "#00897B"], "brain", "Brain dump → prioritised tasks, time-blocked day plan, weekly review.", "v1.0", "Braindump-v1.0.apk", "Braindump-v1.0.aab", "com.mohithash.braindump"),
 ("Sprout", "Sprout", "Keep them alive", "House & Home", ["#2E7D32", "#FF8F00", "#0288D1"], "leaf", "Plant ID + care plan, watering countdowns, plant doctor, care log.", "v1.0", "Sprout-v1.0.apk", "Sprout-v1.0.aab", "com.mohithash.sprout"),
 ("Draftly", "Draftly", "Say it well", "Communication", ["#00838F", "#F4511E", "#5E35B1"], "chat", "Reply, rewrite, summarise, translate, expand, shorten — from text or screenshot.", "v1.0", "Draftly-v1.0.apk", "Draftly-v1.0.aab", "com.mohithash.draftly"),
 ("StoryNest", "Story Nest", "Bedtime, made easy", "Parenting", ["#6A1B9A", "#FFB300", "#00897B"], "star", "Personalised bedtime stories with read mode, sequels and a library.", "v1.0", "StoryNest-v1.0.apk", "StoryNest-v1.0.aab", "com.mohithash.storynest"),
]
for d, name, tag, cat, colors, icon, about, ver, apk, aab, pkg in BESPOKE:
    apps.insert(0, {"id": d.lower(), "name": name, "tagline": tag, "category": cat, "about": about, "colors": colors, "icon": icon, "package": pkg, "tools": [],
        "apk": f"https://github.com/Mohithash/{d}/releases/download/{ver}/{apk}", "aab": f"https://github.com/Mohithash/{d}/releases/download/{ver}/{aab}",
        "source": f"https://github.com/Mohithash/{d}", "listing": f"https://github.com/Mohithash/{d}#readme", "kind": "bespoke", "released": True})

for a in apps:
    g = GLYPHS.get(a["icon"], GLYPHS["spark"]); c0, c1 = a["colors"][0], (a["colors"][1] if len(a["colors"]) > 1 else a["colors"][0])
    open(f"{OUT}/icons/{a['id']}.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{tone(c0,.42)}"/><stop offset="1" stop-color="{tone(c0,.20)}"/></linearGradient></defs><rect width="108" height="108" rx="26" fill="url(#g)"/><g transform="translate(28.8 28.8) scale(2.1)"><path fill="{tone(c1,.85)}" d="{g}"/></g></svg>''')
    a["icon_url"] = f"icons/{a['id']}.svg"

cats = sorted(set(a["category"] for a in apps))
json.dump({"generated": "2026-09-19", "count": len(apps), "categories": cats, "apps": apps}, open(f"{OUT}/catalog.json", "w"), ensure_ascii=False, indent=0)

html = open("/root/claude/Store/template.html").read().replace("__COUNT__", str(len(apps))).replace("__CATS__", json.dumps(cats))
open(f"{OUT}/index.html", "w").write(html)
print(len(apps), "apps,", len(cats), "categories")
