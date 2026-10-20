import hashlib as _hashlib, os as _os
"""Shared head, bar and foot for playnordant.com's pages (kept outside the site repo)."""
SITE = "https://playnordant.com"
PLAY = "https://play.google.com/store/apps/details?id=dev.ribby.nordant"

def head(title, description, path, noindex=False):
    full = title if title == "Nordant" else f"{title} · Nordant"
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full}</title>
  <meta name="description" content="{description}">{robots}
  <link rel="canonical" href="{SITE}{path}">
  <meta property="og:title" content="{full}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE}/assets/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#080a12">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@500;600&family=Barlow+Condensed:wght@700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v={STYLE_VERSION}">
</head>
<body>
"""

def bar(current=""):
    def link(href, text, cls=""):
        mark = ' aria-current="page"' if href == current else ""
        c = f' class="{cls}"' if cls else ""
        return f'<a{c} href="{href}"{mark}>{text}</a>'
    return f"""<header class="bar"><div class="bar-in">
  <a class="mark" href="/"><img src="/assets/favicon-32.png" alt="">NORDANT</a>
  <nav class="nav">{link("/leaderboard", "Leaderboard")}{link("/support", "Support")}{link("/get", "Get the game", "hide-sm")}</nav>
</div></header>
"""

# The stylesheet's version (a hash of it): a changed one is fetched afresh, not kept from a visit before (Pages lets browsers keep it ten minutes).
STYLE_VERSION = _hashlib.sha1(open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "styles.css"), "rb").read()).hexdigest()[:10]

FOOT = """<footer class="foot"><div class="foot-in">
  <nav class="foot-links">
    <a href="/leaderboard">Leaderboard</a>
    <a href="/support">Support</a>
    <a href="/privacy">Privacy</a>
    <a href="/terms">Terms</a>
    <a class="wide" href="/delete-account">Delete your account</a>
  </nav>
  <div class="made"><span>&copy; 2026 ribby.dev LLC</span><a href="mailto:support@playnordant.com">support@playnordant.com</a></div>
</div></footer>
</body>
</html>
"""
