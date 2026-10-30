import os, json, html, re, datetime
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
exec(open("data3.py").read())
exec(open("intros.py").read())
U = json.load(open("urlcheck.json"))

# Single contact address for sponsor, contact, and Organization schema.
CONTACT_EMAIL = "hello@tipslice.com"
# $99/month Stripe Payment Link for each directory. A sponsor page uses only its own.
CHECKOUT_LINKS = {
    "contractoraitools": "https://buy.stripe.com/bJe00ibkqfwR7w20UY3ZK01",
    "moneytoolsdir": "https://buy.stripe.com/14A5kC4W2gAV03AdHK3ZK02",
    "agentusecasesdir": "https://buy.stripe.com/6oU4gy74a84p8A6avy3ZK03",
}
HOST = "https://totty911.github.io"
INDEXNOW_KEY = "6de77d11846e4d2eaf81163942182a19"
TODAY = "2026-10-19"
TODAYL = "October 19, 2026"
# Sitemap lastmod for this update. TODAY stays the link-check date.
SITEMAP_LASTMOD = "2026-10-30"
GA_ID = "G-Q2V68HNZV9"
# Standard GA4 gtag.js snippet, pasted once into <head>.
GA_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Q2V68HNZV9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-Q2V68HNZV9');
</script>"""
ROOT = os.path.abspath(os.path.join(HERE, ".."))

# urlcheck.json is keyed by the pre-move URLs. Listings now use the curl final URL.
OLD_OF = {
    "https://www.buildxact.com/us/": "https://www.buildxact.com",
    "https://www.getjobber.com/": "https://getjobber.com",
    "https://pro.houzz.com/pro": "https://pro.houzz.com",
    "https://contractorforeman.com/": "https://www.contractorforeman.com",
    "https://magicplan.app/": "https://www.magicplan.app",
    "https://www.hammertech.com/en-us/": "https://www.hammertech.com",
    "https://www.handoff.ai/": "https://handoff.ai",
    "https://www.omnicalculator.com/other/tip": "https://www.omnicalculator.com/finance/tip",
    "https://www.nerdwallet.com/mortgages/calculators/mortgage-calculator": "https://www.nerdwallet.com/mortgages/mortgage-calculator",
    "https://www.irs.gov/e-file-do-your-taxes-for-free": "https://www.irs.gov/filing/free-file-do-your-federal-taxes-for-free",
    "https://www.ramseysolutions.com/money/everydollar": "https://www.ramseysolutions.com/ramseyplus/everydollar",
    "https://www.xe.com/en-us/currencyconverter/": "https://www.xe.com/currencyconverter/",
    "https://www.oanda.com/currency-converter/en/": "https://www.oanda.com/currency-converter/",
    "https://www.annualcreditreport.com/index.action": "https://www.annualcreditreport.com",
    "https://www.microsoft.com/en-us/copilot/products/copilot-studio": "https://www.microsoft.com/en-us/microsoft-365-copilot/microsoft-copilot-studio",
    "https://crewai.com/": "https://www.crewai.com",
    "https://huggingface.co/docs/smolagents/index": "https://huggingface.co/docs/smolagents",
    "https://www.langchain.com/langsmith/observability": "https://www.langchain.com/langsmith",
    "https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro": "https://modelcontextprotocol.io",
    "https://www.anthropic.com/engineering/building-effective-agents": "https://www.anthropic.com/research/building-effective-agents",
    "https://tipslice.com/": "https://tipslice.com",
}

SITES = {
    "contractoraitools": ("ContractorAITools", "AI & software tools for contractors", C, "construction and contractor software", "contractors, builders, remodelers and trades", "#1B3A4B", "#F0B429", "C"),
    "moneytoolsdir": ("MoneyToolsDir", "Free calculators & money tools", M, "personal-finance tools", "anyone managing household money", "#0E3B2E", "#8FE3B0", "M"),
    "agentusecasesdir": ("AgentPlaybooks", "AI agent tools, frameworks & use cases", A, "AI agent tools", "builders and teams adopting AI agents", "#2A2158", "#C4B5FD", "A"),
}
e = html.escape

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", "and")).strip("-")

def pick_desc(cands, label):
    for s in cands:
        if 120 <= len(s) <= 160:
            return s
    raise SystemExit(label + " description not 120-160 chars:\n" + "\n".join(f"{len(s)} {s}" for s in cands))

def font(bold, size):
    names = ["Inter-Bold.ttf", "NotoSans-Bold.ttf", "DejaVuSans-Bold.ttf"] if bold else ["Inter-Regular.ttf", "NotoSans-Regular.ttf", "DejaVuSans.ttf"]
    roots = [
        "/usr/share/fonts/truetype/macos",
        "/usr/share/fonts/truetype/noto",
        "/usr/share/fonts/truetype/dejavu",
    ]
    for root in roots:
        for name in names:
            path = os.path.join(root, name)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def write_svg(path, letter, bg, fg):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="6" fill="{bg}"/>
<text x="16" y="22.5" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="18" font-weight="700" fill="{fg}">{letter}</text>
</svg>
'''
    open(path, "w").write(svg)

def write_ico(path, letter, bg, fg):
    size = 32
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((0, 0, size - 1, size - 1), radius=6, fill=bg)
    fnt = font(True, 20)
    box = dr.textbbox((0, 0), letter, font=fnt)
    tw, th = box[2] - box[0], box[3] - box[1]
    dr.text(((size - tw) / 2 - box[0], (size - th) / 2 - box[1] - 1), letter, font=fnt, fill=fg)
    im.save(path, format="ICO", sizes=[(16, 16), (32, 32)])

def write_og(path, name, tagline, url, bg, accent):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), bg)
    dr = ImageDraw.Draw(im)
    dr.rectangle((0, 0, 18, H), fill=accent)
    name_f, tag_f, url_f = font(True, 78), font(False, 36), font(False, 28)
    y = 170
    for line in wrap(dr, name, name_f, 1040):
        dr.text((72, y), line, font=name_f, fill="white")
        y += 92
    y += 10
    for line in wrap(dr, tagline, tag_f, 1040):
        dr.text((72, y), line, font=tag_f, fill=accent)
        y += 48
    dr.text((72, 540), url.replace("https://", ""), font=url_f, fill="#E6E8EE")
    im.save(path, "PNG", optimize=True)
    with Image.open(path) as check:
        if check.size != (1200, 630):
            raise SystemExit(f"og image {path} is {check.size}")

CSS = "body{font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:1000px;margin:auto;padding:1em;color:#1d1d1f;line-height:1.5}a{color:#0a58ca}nav{display:flex;flex-wrap:wrap;gap:1em;padding:.5em 0;border-bottom:1px solid #eee}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}.c{border:1px solid #ddd;border-radius:10px;padding:14px;background:#fff}.c h3{margin:.1em 0 .3em;font-size:1.1em}.v{color:#555;font-size:.9em;border-left:3px solid #ddd;padding-left:8px}.chip{display:inline-block;background:#f1f3f5;border-radius:99px;padding:.2em .7em;margin:.2em;font-size:.9em;text-decoration:none}.feat{border:2px dashed #f0b400;background:#fffbea}table{border-collapse:collapse;width:100%;font-size:.92em}td,th{border-bottom:1px solid #eee;padding:6px;text-align:left}small{color:#666}footer{margin-top:2em;border-top:1px solid #eee;padding-top:1em}main{display:block}"

def other_tools(current_name):
    parts = []
    for slug, info in SITES.items():
        name = info[0]
        if name == current_name:
            continue
        parts.append(f'<a href="{HOST}/{slug}/">{e(name)}</a>')
    parts.append('<a href="https://tipslice.com/">TipSlice</a>')
    return "<p>Our other free tools: " + " · ".join(parts) + "</p>"

def page(t, title, desc, body, url, root, base):
    if not 120 <= len(desc) <= 160:
        raise SystemExit(f"desc length {len(desc)} for {url}: {desc}")
    home = "./" if root == "" else root
    og = base + "og.png"
    head_links = (
        f'<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">'
        f'<link rel="icon" href="{base}favicon.ico" sizes="32x32" type="image/x-icon">'
        f'<meta property="og:image" content="{og}">'
        f'<meta property="og:image:width" content="1200">'
        f'<meta property="og:image:height" content="630">'
        f'<meta property="og:image:alt" content="{e(t)}">'
        f'<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:image" content="{og}">'
    )
    return (
        f'<!doctype html><html lang=en><head>{GA_SNIPPET}<meta charset=utf-8>'
        f'<meta name=viewport content="width=device-width,initial-scale=1">'
        f'<title>{e(title)}</title><meta name=description content="{e(desc)}">'
        f'<link rel=canonical href="{url}">'
        f'<meta property="og:title" content="{e(title)}">'
        f'<meta property="og:description" content="{e(desc)}">'
        f'<meta property="og:url" content="{url}">'
        f'<meta property="og:type" content="website">{head_links}'
        f'<style>{CSS}</style></head><body>'
        f'<nav><a href="{home}"><b>{e(t)}</b></a>'
        f'<a href="{home}#categories">Categories</a>'
        f'<a href="{root}sponsor.html">Feature your tool</a>'
        f'<a href="{root}about.html">How we curate</a>'
        f'<a href="{root}contact.html">Contact</a>'
        f'<a href="{root}privacy.html">Privacy</a></nav>'
        f'<main>{body}</main>'
        f'<footer>{other_tools(t)}<p><small>Listings are editorial and free. Sponsored placements, when sold, are labeled "Featured". '
        f'Not affiliated with listed vendors. Links last checked {TODAYL}. Vendor descriptions are quoted from each vendor\'s own homepage meta description.</small></p></footer>'
        f'</body></html>'
    )

def vendor_desc(u):
    rec = U.get(u) or U.get(OLD_OF.get(u, ""), {})
    return rec.get("desc", "")

def card(n, u, d, c=None):
    v = vendor_desc(u)
    if len(v) > 220:
        v = v[:217].rsplit(" ", 1)[0] + "…"
    vq = f'<p class=v>Vendor says: “{e(v)}”</p>' if v else ""
    cat = f"<small>{e(c)}</small><br>" if c else ""
    return f'<div class=c><h3>{e(n)}</h3><p>{e(d)}</p>{vq}{cat}<a href="{u}" rel="noopener" target="_blank">Visit {e(n)} ↗</a></div>'

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

sitemap_locs = []
for slug, (t, tag, cats, sp, aud, bg, accent, letter) in SITES.items():
    base = f"{HOST}/{slug}/"
    d = f"{ROOT}/{slug}"
    os.makedirs(d + "/c", exist_ok=True)
    for f in os.listdir(d + "/c"):
        os.remove(d + "/c/" + f)
    for stale in ("CNAME",):
        p = os.path.join(d, stale)
        if os.path.exists(p):
            os.remove(p)
    n = sum(len(ts) for c, ts in cats)
    urls = []
    write_svg(f"{d}/favicon.svg", letter, bg, "#ffffff")
    write_ico(f"{d}/favicon.ico", letter, bg, "#ffffff")
    write_og(f"{d}/og.png", t, tag, base, bg, accent)
    chips = "".join(f'<a class=chip href="c/{slugify(c)}.html">{e(c)} ({len(ts)})</a>' for c, ts in cats)
    home_desc = pick_desc([
        f"A free directory of {n} {sp} in {len(cats)} categories for {aud}. Every official link was checked on {TODAYL}.",
        f"Free directory of {n} {sp} in {len(cats)} categories for {aud}. Official links checked {TODAYL}.",
        f"{n} curated {sp} across {len(cats)} categories for {aud}. Official links checked {TODAYL}.",
    ], slug + " home")
    b = (
        f"<h1>{e(t)}: {e(tag)}</h1>"
        f"<p>A free, hand-curated directory of {n} {e(sp)} for {e(aud)}, organized into {len(cats)} categories. "
        f"Every listing links to the vendor's official site, and every link was checked on {TODAYL}.</p>"
        f"<h2 id=categories>Browse by category</h2><p>{chips}</p>"
    )
    b += (
        f'<div class="c feat"><b>Featured spot available</b><p>Reach {e(aud)} with a labeled featured card at the top of a category page. '
        f'<a href="sponsor.html">See sponsorship details</a>.</p></div>'
    )
    for c, ts in cats:
        cs = slugify(c)
        b += f"<h2>{e(c)}</h2><p>{e(I[c][0])}</p><div class=g>" + "".join(card(x, u, dd) for x, u, dd in ts[:6]) + f'</div><p><a href="c/{cs}.html">See all {len(ts)} {e(c.lower())} tools, with what to look for →</a></p>'
    faq = [
        ("Is this directory free?", "Yes. Browsing is free and listings are free. Vendors can buy a clearly labeled featured spot; that does not change editorial listings."),
        ("How are tools chosen?", "Tools are added from their official websites. Each link is checked for a working response before publishing, and dead or redirected listings are updated or removed."),
        ("Are prices listed?", "No. Pricing changes often, so check each vendor's site. Many tools are paid or freemium."),
        ("How do I suggest a tool?", "Use the contact page. Suggestions are reviewed, not guaranteed."),
    ]
    b += "<h2>FAQ</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq)
    b += ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    b += ld({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": t,
        "url": base,
        "email": CONTACT_EMAIL,
        "logo": {"@type": "ImageObject", "url": base + "og.png", "width": 1200, "height": 630},
    })
    b += ld({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": t,
        "url": base,
        "description": home_desc,
        "publisher": {"@type": "Organization", "name": t, "url": base},
    })
    b += f"<p><small>Last updated {TODAYL}.</small></p>"
    sponsor_desc = pick_desc([
        f"Sponsor a labeled featured listing on {t}. Reach {aud} with a clearly marked card in the matching category.",
    ], slug + " sponsor")
    about_desc = pick_desc([
        f"How {t} chooses and checks listings: official sites only, live links rechecked, and sponsored spots labeled apart from editorial.",
    ], slug + " about")
    contact_desc = pick_desc([
        f"Contact {t} about a listing suggestion, a correction, or a sponsorship. Email {CONTACT_EMAIL} and each note is reviewed.",
    ], slug + " contact")
    privacy_desc = pick_desc([
        f"{t} privacy policy: no accounts. Google Analytics measures page visits. GitHub Pages may log IP address and user agent.",
    ], slug + " privacy")
    P = {
        "index": (
            f"{t} – {n} {tag}",
            home_desc,
            b,
        ),
        "sponsor": (
            f"Feature your tool | {t}",
            sponsor_desc,
            f"<h1>Feature your tool on {e(t)}</h1>"
            f"<p>{e(t)} lists {n} {e(sp)} for {e(aud)}. A featured placement gives your product a labeled \"Featured\" card at the top of the category page that matches it, plus a mention on the home page.</p>"
            f"<h2>What you get</h2><ul>"
            f"<li>Featured card at the top of one category page, labeled as sponsored</li>"
            f"<li>Home-page featured spot (rotates among sponsors)</li>"
            f"<li>Sponsored links are marked rel=\"sponsored\", following Google's link guidelines</li></ul>"
            f"<h2>Price</h2><p><b>Introductory price: $99/month</b>, one category. Cancel any time.</p>"
            f'<p><a href="{CHECKOUT_LINKS[slug]}" rel="sponsored noopener" style="display:inline-block;background:#0a58ca;color:#fff;text-decoration:none;font-weight:700;padding:.65em 1.1em;border-radius:8px">Start sponsorship ($99/month)</a></p>'
            f"<p>After checkout, email <a href='mailto:{CONTACT_EMAIL}'>{CONTACT_EMAIL}</a> with your product name, the category you want, your logo and a one-line description. Your Featured card goes live after a quick manual review. We may decline sponsors that aren't a fit and refund them.</p>",
        ),
        "about": (
            f"How we curate | {t}",
            about_desc,
            f"<h1>About {e(t)}</h1><p>{e(t)} is an independent, curated directory of {e(tag.lower())}, built for {e(aud)}.</p>"
            f"<h2>How listings are chosen</h2><ul>"
            f"<li>Only products with an official, working website are listed.</li>"
            f"<li>Every link is checked for a live response before each update. The most recent check was {TODAYL}.</li>"
            f"<li>The short description is our own summary. The quoted \"Vendor says\" text is the vendor's own homepage description, copied as-is.</li>"
            f"<li>We do not list prices because they change often.</li>"
            f"<li>Sponsored placements are labeled and never replace editorial listings.</li></ul>"
            f"<h2>Corrections</h2><p>If a listing is wrong or out of date, use the contact page and it will be fixed.</p>",
        ),
        "contact": (
            f"Contact | {t}",
            contact_desc,
            f"<h1>Contact</h1><p>Suggestions, corrections and sponsorship: <a href='mailto:{CONTACT_EMAIL}'>{CONTACT_EMAIL}</a>.</p>",
        ),
        "privacy": (
            f"Privacy | {t}",
            privacy_desc,
            f"<h1>Privacy</h1>"
            f"<p>{e(t)} is a static directory. There are no accounts, and these pages do not ask you to submit personal information. We do not set our own cookies. Our host (GitHub Pages) may log standard server data such as IP address and user agent.</p>"
            f"<h2>Google Analytics</h2>"
            f"<p>{e(t)} loads Google Analytics with gtag.js. "
            f'<a href="https://policies.google.com/technologies/partner-sites">How Google uses information from sites or apps that use our services</a> '
            f"explains that when you visit a site using analytics tools such as Google Analytics, your browser automatically sends certain information to Google, including the URL of the page you are visiting and your IP address, and that Google may set cookies on your browser or read cookies that are already there. "
            f"Many sites use Google Analytics to understand how visitors engage with them. "
            f'If you do not want Analytics to be used in your browser, you can install the <a href="https://tools.google.com/dlpage/gaoptout">Google Analytics opt-out browser add-on</a>.</p>',
        ),
    }
    for k, (ti, de, bo) in P.items():
        url = base if k == "index" else base + k + ".html"
        urls.append(url)
        open(f"{d}/{k}.html", "w").write(page(t, ti, de, bo, url, "", base))
    for c, ts in cats:
        cs = slugify(c)
        intro, looks = I[c]
        url = f"{base}c/{cs}.html"
        urls.append(url)
        cat_desc = pick_desc([
            f"{len(ts)} {c.lower()} options for {aud}, with official links, a buyer's checklist, and a comparison table.",
            f"{len(ts)} {c.lower()} tools for {aud}, with official links, a buyer's checklist, and a comparison table.",
            f"Browse {len(ts)} {c.lower()} options for {aud}. Official links, a buyer's checklist, and a comparison table.",
            f"{len(ts)} {c.lower()} options for {aud}. Official links, a buyer's checklist, and a comparison table, checked {TODAYL}.",
        ], f"{slug} {c}")
        others = "".join(f'<a class=chip href="{slugify(o)}.html">{e(o)}</a>' for o, _ in cats if o != c)
        bo = (
            f'<p><small><a href="../">{e(t)}</a> › {e(c)}</small></p>'
            f"<h1>{len(ts)} {e(c)} tools</h1><p>{e(intro)}</p>"
            f"<h2>What to look for</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in looks) + "</ul>"
        )
        bo += "<h2>All listings</h2><div class=g>" + "".join(card(x, u, dd) for x, u, dd in ts) + "</div>"
        bo += (
            "<h2>Quick comparison</h2><table><tr><th>Tool</th><th>Focus</th><th>Official site</th></tr>"
            + "".join(
                f'<tr><td>{e(x)}</td><td>{e(dd)}</td><td><a href="{u}" rel="noopener">{e(re.sub(r"^https?://(www\\.)?", "", u).rstrip("/"))}</a></td></tr>'
                for x, u, dd in ts
            )
            + "</table>"
        )
        bo += f"<h2>Other categories</h2><p>{others}</p><p><small>Last updated {TODAYL}.</small></p>"
        bo += ld({
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": f"{c} tools",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": x, "url": u} for i, (x, u, dd) in enumerate(ts)],
        })
        bo += ld({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t, "item": base},
                {"@type": "ListItem", "position": 2, "name": c, "item": url},
            ],
        })
        open(f"{d}/c/{cs}.html", "w").write(
            page(
                t,
                f"{len(ts)} {c} tools ({datetime.date(2026, 10, 19).year}) | {t}",
                cat_desc,
                bo,
                url,
                "../",
                base,
            )
        )
    open(f"{d}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n")
    open(f"{d}/sitemap.xml", "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc><lastmod>{SITEMAP_LASTMOD}</lastmod></url>" for u in urls)
        + "</urlset>"
    )
    open(f"{d}/llms.txt", "w").write(
        f"# {t}\n> {tag}. Free curated directory of {n} listings. Links checked {TODAY}.\n\n"
        + "\n".join(f"## {c}\n" + "\n".join(f"- [{x}]({u}): {dd}" for x, u, dd in ts) for c, ts in cats)
        + "\n"
    )
    sitemap_locs.append(base + "sitemap.xml")
    print(slug, n, "listings", len(cats), "categories", len(urls), "pages")

write_svg(f"{ROOT}/favicon.svg", "T", "#243044", "#ffffff")
write_ico(f"{ROOT}/favicon.ico", "T", "#243044", "#ffffff")
open(f"{ROOT}/{INDEXNOW_KEY}.txt", "w").write(INDEXNOW_KEY + "\n")
open(f"{ROOT}/robots.txt", "w").write(
    "User-agent: *\nAllow: /\n\n"
    + f"Sitemap: {HOST}/sitemap.xml\n"
    + "".join(f"Sitemap: {loc}\n" for loc in sitemap_locs)
)
open(f"{ROOT}/sitemap.xml", "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    + "".join(f"<sitemap><loc>{loc}</loc><lastmod>{SITEMAP_LASTMOD}</lastmod></sitemap>" for loc in sitemap_locs)
    + "</sitemapindex>"
)

def fail(msg):
    raise SystemExit(msg)

for slug in SITES:
    for dirpath, _, files in os.walk(f"{ROOT}/{slug}"):
        for fn in files:
            if not fn.endswith((".html", ".xml", ".txt")):
                continue
            text = open(os.path.join(dirpath, fn), encoding="utf-8").read()
            for bad in ("matttotty", "gmail.com", "surge.sh", "your tool here"):
                if bad in text.lower() if bad != "surge.sh" else bad in text:
                    fail(f"{bad} in {dirpath}/{fn}")
            if fn.endswith(".html"):
                head, sep, rest = text.partition("</head>")
                if not sep:
                    fail(f"head missing in {dirpath}/{fn}")
                if head.count(GA_SNIPPET) != 1 or rest.count(GA_ID) != 0:
                    fail(f"ga tag not exactly once in head: {dirpath}/{fn}")
                if head.count(f"gtag/js?id={GA_ID}") != 1 or head.count(f"gtag('config', '{GA_ID}')") != 1:
                    fail(f"ga snippet incomplete in {dirpath}/{fn}")
                footer = text.split("<footer>", 1)[-1].split("</footer>", 1)[0]
                tools, _, _ = footer.partition("</p>")
                if not tools.startswith("<p>Our other free tools:"):
                    fail(f"footer tools missing in {dirpath}/{fn}")
                if "nofollow" in tools.lower() or "rel=" in tools.lower():
                    fail(f"footer tools links are not plain in {dirpath}/{fn}")
                if tools.count("https://tipslice.com/") != 1:
                    fail(f"tipslice footer link in {dirpath}/{fn}")
                for other, info in SITES.items():
                    href = f"{HOST}/{other}/"
                    if other == slug:
                        if href in tools:
                            fail(f"self link in footer tools {dirpath}/{fn}")
                    elif tools.count(href) != 1 or info[0] not in tools:
                        fail(f"missing footer link {other} in {dirpath}/{fn}")
                if text.lower().count("<main") != 1 or text.lower().count("</main>") != 1:
                    fail(f"main landmark missing in {dirpath}/{fn}")
                if "og:image" not in text:
                    fail(f"og:image missing in {dirpath}/{fn}")
                if re.search(r'href="[^"]*index\.html', text):
                    fail(f"index.html link in {dirpath}/{fn}")
                if 'rel=canonical href="' + HOST not in text:
                    fail(f"canonical host in {dirpath}/{fn}")
                m = re.search(r'name=description content="([^"]*)"', text)
                if not m:
                    fail(f"no description {dirpath}/{fn}")
                desc = html.unescape(m.group(1))
                if not 120 <= len(desc) <= 160:
                    fail(f"desc {len(desc)} {dirpath}/{fn}: {desc}")
    home = open(f"{ROOT}/{slug}/index.html", encoding="utf-8").read()
    if '"@type": "Organization"' not in home or '"@type": "WebSite"' not in home:
        fail(f"schema missing on {slug} home")
    if CONTACT_EMAIL not in open(f"{ROOT}/{slug}/contact.html", encoding="utf-8").read():
        fail(f"contact email missing {slug}")
    sponsor_html = open(f"{ROOT}/{slug}/sponsor.html", encoding="utf-8").read()
    if CONTACT_EMAIL not in sponsor_html:
        fail(f"sponsor email missing {slug}")
    if "not live yet" in sponsor_html.lower():
        fail(f"checkout still offline in {slug}")
    own = CHECKOUT_LINKS[slug]
    if sponsor_html.count(own) != 1:
        fail(f"checkout link count {sponsor_html.count(own)} in {slug}")
    for other, url in CHECKOUT_LINKS.items():
        if other != slug and url in sponsor_html:
            fail(f"wrong checkout link in {slug}")
    if "Start sponsorship ($99/month)" not in sponsor_html:
        fail(f"checkout button missing in {slug}")
    privacy_html = open(f"{ROOT}/{slug}/privacy.html", encoding="utf-8").read()
    for needed in (
        "https://policies.google.com/technologies/partner-sites",
        "How Google uses information from sites or apps that use our services",
        "https://tools.google.com/dlpage/gaoptout",
        "Google Analytics opt-out browser add-on",
        "loads Google Analytics with gtag.js",
    ):
        if needed not in privacy_html:
            fail(f"privacy disclosure missing {needed!r} in {slug}")
    if "nofollow" in privacy_html.lower():
        fail(f"nofollow in privacy {slug}")
    if "no analytics" in privacy_html.lower():
        fail(f"stale no-analytics claim in {slug}")
    sitemap_xml = open(f"{ROOT}/{slug}/sitemap.xml", encoding="utf-8").read()
    locs = re.findall(r"<loc>(.*?)</loc>", sitemap_xml)
    lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", sitemap_xml)
    if len(locs) != len(lastmods) or any(mod != SITEMAP_LASTMOD for mod in lastmods):
        fail(f"sitemap lastmod in {slug}: {lastmods}")
    for tip in re.findall(r'href="(https://tipslice\.com[^"]*)"', open(f"{ROOT}/{slug}/index.html", encoding="utf-8").read() + open(f"{ROOT}/{slug}/llms.txt", encoding="utf-8").read()):
        if not tip.startswith("https://tipslice.com/"):
            fail(f"tipslice link {tip}")

robots = open(f"{ROOT}/robots.txt", encoding="utf-8").read()
if "Disallow:" in robots:
    fail("root robots disallows something")
if robots.count("Sitemap:") != 1 + len(SITES):
    fail("sitemap lines " + robots)
root_sitemap = open(f"{ROOT}/sitemap.xml", encoding="utf-8").read()
root_lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", root_sitemap)
if len(root_lastmods) != len(SITES) or any(mod != SITEMAP_LASTMOD for mod in root_lastmods):
    fail(f"root sitemap lastmod {root_lastmods}")
if open(f"{ROOT}/{INDEXNOW_KEY}.txt", encoding="utf-8").read() != INDEXNOW_KEY + "\n":
    fail("indexnow key file changed")
print("checks ok")
