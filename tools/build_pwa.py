#!/usr/bin/env python3
"""Build index.html (the installable app) from src/launchpad.html (the Claude artifact page).

The artifact page is an HTML fragment (Claude wraps it at publish time). This script
wraps it into a full document, adds the web-app manifest, icons and service worker,
a draggable title strip for window-controls-overlay mode, serves the grid library
from vendor/ (so the app also opens offline), and takes the ANLZ panel out
(it needs Claude's in-page runtime, which only exists inside Claude).

src/artifact.html is the older single-page layout. It stays as the source of the
"JARVIS 터미널" Claude artifact.

Usage: python3 tools/build_pwa.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "src" / "launchpad.html").read_text(encoding="utf-8")


def once(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:70])
    return s.replace(a, b)


# 1) split the fragment into head part (fonts + style) and body part (.app + scripts)
cut = src.index('<div class="app">')
head, body = src[:cut], src[cut:]
head = re.sub(r"<title>.*?</title>\s*", "", head, flags=re.S)
head = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*', "", head)

# 2) grid library from this site instead of the CDN
body = once(body, '<script src="https://cdn.jsdelivr.net/npm/gridstack@10.3.1/dist/gridstack-all.js"></script>',
            '<script src="vendor/gridstack-all.js"></script>')

# 3) ANLZ needs window.claude: keep its DOM (its script still runs) but drop it from the workspace
body = once(body, 'Array.prototype.forEach.call(document.querySelectorAll("#ws > .grid-stack-item"),function(it){ ITEMS[it.getAttribute("gs-id")]=it; });',
            'Array.prototype.forEach.call(document.querySelectorAll("#ws > .grid-stack-item"),function(it){ ITEMS[it.getAttribute("gs-id")]=it; });\n'
            'if(ITEMS.anlz){ parking.appendChild(ITEMS.anlz); delete ITEMS.anlz; }')
body, n = re.subn(r',\["anlz",\d+,\d+,\d+,\d+\]\]', ']', body)
assert n == 1, n
body = once(body, '["ANLZ","기사 붙여넣기 분석","p","anlz"],', '')

APP_HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>JARVIS 터미널</title>
<meta name="description" content="외신 중심 시장 브리핑 터미널">
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="dark">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/favicon-64.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="JARVIS">
"""

APP_STYLE = """<style>
/* app shell: safe areas, title strip for window-controls-overlay */
[hidden]{display:none!important}
body{margin:0;padding-top:max(10px, env(safe-area-inset-top, 0px))}
.statusbar{padding-bottom:env(safe-area-inset-bottom, 0px)}
.wco-bar{display:none}
@media (display-mode: window-controls-overlay){
  .wco-bar{display:flex;align-items:center;gap:10px;position:fixed;z-index:200;left:env(titlebar-area-x,0);top:env(titlebar-area-y,0);
    width:env(titlebar-area-width,100%);height:env(titlebar-area-height,32px);padding:0 12px;box-sizing:border-box;background:#000;
    border-bottom:1px solid #1d1d1d;font:600 11px "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.12em;color:#5e5e5e;
    -webkit-app-region:drag;app-region:drag;-webkit-user-select:none;user-select:none}
  .wco-bar b{background:#ffa733;color:#000;padding:1px 6px}
  body{padding-top:calc(env(titlebar-area-height,32px) + 6px)}
  .grid-stack-item.gmax{top:calc(env(titlebar-area-height,32px) + 6px)!important}
}
</style>
</head>
<body>
<div class="wco-bar" aria-hidden="true"><b>JRVS</b>MARKET INTELLIGENCE</div>
"""

APP_TAIL = """
<script>
if("serviceWorker" in navigator){ window.addEventListener("load",function(){ navigator.serviceWorker.register("sw.js").catch(function(){}); }); }
</script>
</body>
</html>
"""

out = APP_HEAD + head + APP_STYLE + body + APP_TAIL
(ROOT / "index.html").write_text(out, encoding="utf-8")
print("index.html", len(out), "bytes")
