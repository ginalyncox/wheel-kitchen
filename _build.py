"""Simple static site builder: stamps shared shell around content fragments."""
import os, re, pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "pages"
OUT = ROOT  # write built pages next to index.html

# ---------- Shared shell ----------
NAV = [
    ("Home", "index.html"),
    ("Kitchen Setup", "kitchen-setup.html"),
    ("Stovetop & Oven", "stovetop-oven.html"),
    ("Prep & Reach", "prep-reach.html"),
    ("Toolkit", "toolkit.html"),
    ("Meal Planning", "meal-planning.html"),
    ("Safety", "safety.html"),
    ("Cleanup", "cleanup.html"),
    ("Groceries", "groceries.html"),
    ("Troubleshooting", "troubleshooting.html"),
    ("About", "about.html"),
]

LOGO_SVG = '''
<svg class="brand__mark" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <!-- Wheel -->
  <circle cx="14" cy="26" r="10"/>
  <circle cx="14" cy="26" r="2" fill="currentColor" stroke="none"/>
  <line x1="14" y1="16" x2="14" y2="36"/>
  <line x1="4" y1="26" x2="24" y2="26"/>
  <!-- Wheat sprig -->
  <path d="M28 20 L34 6" />
  <path d="M31 14 Q34 14 34 11" />
  <path d="M31 14 Q28 14 28 11" />
  <path d="M30 17 Q33 17 33 14" />
  <path d="M30 17 Q27 17 27 14" />
</svg>
'''.strip()

def build_header(current: str) -> str:
    items = []
    for label, href in NAV:
        aria = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{aria}>{label}</a></li>')
    nav_items = "\n            ".join(items)
    return f'''<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="container site-header__inner">
    <a href="index.html" class="brand" aria-label="Gina Makes home">
      {LOGO_SVG}
      <span>
        <span class="brand__wordmark">Gina Makes</span>
        <span class="brand__sub">Wheel + Kitchen</span>
      </span>
    </a>
    <nav class="site-nav" aria-label="Primary">
      <button class="site-nav__toggle" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
      </button>
      <ul id="primary-nav" class="site-nav__list">
            {nav_items}
      </ul>
      <button class="theme-toggle" data-theme-toggle aria-label="Switch color mode"></button>
    </nav>
  </div>
</header>
'''

FOOTER = '''
<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <div class="brand" style="pointer-events:none">
          ''' + LOGO_SVG + '''
          <span>
            <span class="brand__wordmark">Gina Makes</span>
            <span class="brand__sub">Wheel + Kitchen</span>
          </span>
        </div>
        <p class="site-footer__blurb" style="margin-top:var(--space-4)">
          A research-backed field guide to cooking real food in a real kitchen — from a manual wheelchair. Published by Gina Makes.
        </p>
      </div>
      <div>
        <h3>Guide</h3>
        <ul>
          <li><a href="kitchen-setup.html">Kitchen setup</a></li>
          <li><a href="stovetop-oven.html">Stovetop &amp; oven</a></li>
          <li><a href="prep-reach.html">Prep &amp; reach</a></li>
          <li><a href="toolkit.html">Toolkit</a></li>
          <li><a href="safety.html">Safety</a></li>
        </ul>
      </div>
      <div>
        <h3>More</h3>
        <ul>
          <li><a href="meal-planning.html">Meal planning</a></li>
          <li><a href="cleanup.html">Cleanup</a></li>
          <li><a href="groceries.html">Groceries</a></li>
          <li><a href="troubleshooting.html">Troubleshooting</a></li>
          <li><a href="about.html">About &amp; sources</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__legal">
      <div>&copy; 2026 Gina Makes LLC. Built with care in Des Moines, Iowa.</div>
      <div>Educational content, not medical or occupational-therapy advice.</div>
    </div>
  </div>
</footer>
'''

HEAD = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Gina Makes: Wheel + Kitchen</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title} — Gina Makes: Wheel + Kitchen">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Ccircle cx='20' cy='20' r='10' fill='none' stroke='%234E6A4E' stroke-width='3'/%3E%3Ccircle cx='20' cy='20' r='2' fill='%234E6A4E'/%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
{header}
<main id="main">
{content}
</main>
{footer}
<script src="js/site.js"></script>
</body>
</html>
'''

def parse_front(text: str):
    # Parse a simple front matter delimited by --- lines. Returns dict + body.
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    header = text[3:end].strip()
    body = text[end+4:].lstrip("\n")
    meta = {}
    for line in header.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body

def build():
    for src in sorted(SRC.glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        meta, body = parse_front(raw)
        title = meta.get("title", src.stem)
        desc = meta.get("desc", "Cooking in a normal kitchen from a manual wheelchair.")
        current = src.name  # matches nav href
        html = HEAD.format(
            title=title, desc=desc,
            header=build_header(current),
            content=body,
            footer=FOOTER,
        )
        out = OUT / src.name
        out.write_text(html, encoding="utf-8")
        print("built", out.name)

if __name__ == "__main__":
    build()
