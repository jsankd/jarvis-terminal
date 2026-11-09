#!/usr/bin/env python3
"""Build index.html (the installable app) from src/artifact.html (the Claude artifact page).

The artifact page is an HTML fragment (Claude wraps it at publish time). This script
wraps it into a full document, adds the web-app manifest, icons, a service worker,
a draggable title strip for window-controls-overlay mode, and hides the ANLZ panel
(it needs Claude's in-page runtime, which only exists inside Claude).

Usage: python3 tools/build_pwa.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "src" / "artifact.html").read_text(encoding="utf-8")

# 1) split fragment into head part (fonts + style) and body part (.wrap + script)
cut = src.index('<div class="wrap">')
head, body = src[:cut], src[cut:]
head = re.sub(r"<title>.*?</title>\s*", "", head, flags=re.S)
head = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*', "", head)

# 2) hide ANLZ (needs window.claude) — keep it in the DOM so its script still runs
def once(s, a, b):
    assert s.count(a) == 1, a[:60]
    return s.replace(a, b)

body = once(body, '<section class="p s12" id="p-anlz">', '<section class="p s12" id="p-anlz" hidden>')
body = once(body, '<button class="fk" type="button" data-go="p-anlz">', '<button class="fk" type="button" data-go="p-anlz" hidden>')
body = once(body, 'placeholder="SEMI · KR · N3 · ANLZ · HELP 입력 후 Enter  ( / 키 )"', 'placeholder="SEMI · KR · N3 · HELP 입력 후 Enter  ( / 키 )"')

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
body{margin:0;padding-top:max(14px, env(safe-area-inset-top, 0px));padding-bottom:max(40px, env(safe-area-inset-bottom, 0px))}
.wco-bar{display:none}
@media (display-mode: window-controls-overlay){
  .wco-bar{display:flex;align-items:center;gap:10px;position:fixed;z-index:200;left:env(titlebar-area-x,0);top:env(titlebar-area-y,0);
    width:env(titlebar-area-width,100%);height:env(titlebar-area-height,32px);padding:0 12px;box-sizing:border-box;background:#000;
    border-bottom:1px solid #1d1d1d;font:600 11px "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.12em;color:#5e5e5e;
    -webkit-app-region:drag;app-region:drag;-webkit-user-select:none;user-select:none}
  .wco-bar b{background:#ffa733;color:#000;padding:1px 6px}
  body{padding-top:calc(env(titlebar-area-height,32px) + 10px)}
}
@media (display-mode: standalone){ .p{scroll-margin-top:12px} }
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
