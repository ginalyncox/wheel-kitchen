"""Simple static site builder: stamps shared shell around content fragments."""
import html
import pathlib
from string import Template

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "pages"
OUT = ROOT  # write built pages next to index.html

# ---------- Shared shell ----------
NAV = [
    ("Home", "index.html"),
    ("Setup", "kitchen-setup.html"),
    ("Stove &amp; oven", "stovetop-oven.html"),
    ("Prep", "prep-reach.html"),
    ("Toolkit", "toolkit.html"),
    ("Planning", "meal-planning.html"),
    ("Safety", "safety.html"),
    ("Cleanup", "cleanup.html"),
    ("Groceries", "groceries.html"),
    ("Fixes", "troubleshooting.html"),
    ("About", "about.html"),
]

LOGO_SVG = '''
<svg class="brand__mark" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <!-- Wheel -->
  <circle cx="14" cy="26" r="10"/>
  <circle cx="14" cy="26" r="1.8" fill="currentColor" stroke="none"/>
  <line x1="14" y1="17" x2="14" y2="35"/>
  <line x1="5" y1="26" x2="23" y2="26"/>
  <!-- Wheat sprig, contained within viewBox -->
  <path d="M30 20 L34 10" />
  <path d="M31.6 16 Q34.5 16 34.5 13" />
  <path d="M31.6 16 Q28.5 16 28.5 13" />
  <path d="M30.6 18.5 Q33.5 18.5 33.5 15.5" />
  <path d="M30.6 18.5 Q27.5 18.5 27.5 15.5" />
</svg>
'''.strip()

# Fallback icon so the control is not empty before JS paints
THEME_TOGGLE_FALLBACK = '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'''

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
      <button type="button" class="site-nav__toggle" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
      </button>
      <ul id="primary-nav" class="site-nav__list" role="list">
            {nav_items}
      </ul>
      <button type="button" class="theme-toggle" data-theme-toggle aria-label="Switch color mode">{THEME_TOGGLE_FALLBACK}</button>
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
        <ul role="list">
          <li><a href="kitchen-setup.html">Kitchen setup</a></li>
          <li><a href="stovetop-oven.html">Stovetop &amp; oven</a></li>
          <li><a href="prep-reach.html">Prep &amp; reach</a></li>
          <li><a href="toolkit.html">Toolkit</a></li>
          <li><a href="safety.html">Safety</a></li>
        </ul>
      </div>
      <div>
        <h3>More</h3>
        <ul role="list">
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

# Use $-placeholders so fragment content with `{`/`}` cannot break the template.
HEAD = Template('''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$full_title</title>
  <meta name="description" content="$desc">
  <meta property="og:title" content="$full_title">
  <meta property="og:description" content="$desc">
  <meta property="og:type" content="article">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Ccircle cx='20' cy='20' r='10' fill='none' stroke='%234E6A4E' stroke-width='3'/%3E%3Ccircle cx='20' cy='20' r='2' fill='%234E6A4E'/%3E%3C/svg%3E">
  <script>
    (function () {
      var mode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', mode);
    })();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&amp;family=Work+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
$header
<main id="main">
$content
</main>
$footer
<script src="js/site.js"></script>
</body>
</html>
''')

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

def page_title(title: str) -> str:
    if title == "Wheel + Kitchen":
        return "Gina Makes: Wheel + Kitchen"
    return f"{title} — Gina Makes: Wheel + Kitchen"

def build():
    for src in sorted(SRC.glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        meta, body = parse_front(raw)
        title = meta.get("title", src.stem)
        desc = meta.get("desc", "Cooking in a normal kitchen from a manual wheelchair.")
        current = src.name  # matches nav href
        html_out = HEAD.substitute(
            full_title=html.escape(page_title(title), quote=False),
            desc=html.escape(desc, quote=True),
            header=build_header(current),
            content=body,
            footer=FOOTER,
        )
        out = OUT / src.name
        out.write_text(html_out, encoding="utf-8")
        print("built", out.name)

if __name__ == "__main__":
    build()
