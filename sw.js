/* JARVIS terminal service worker.
   - page and data.json: network first, cached copy when offline (so the last brief still opens)
   - map, icons, manifest: cache first */
const CACHE = "jarvis-v1";
const SHELL = ["./", "index.html", "map.json", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/favicon-64.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const fresh = req.mode === "navigate" || url.pathname.endsWith("/data.json") || url.pathname.endsWith("/index.html") || url.pathname.endsWith("/");
  if (fresh) {
    const netReq = req.mode === "navigate" ? req : new Request(req, { cache: "no-store" });
    e.respondWith(
      fetch(netReq)
        .then((res) => {
          if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req.mode === "navigate" ? "index.html" : url.pathname, copy)); }
          return res;
        })
        .catch(() => caches.match(req.mode === "navigate" ? "index.html" : url.pathname).then((r) => r || caches.match(req, { ignoreSearch: true })))
    );
    return;
  }
  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then((hit) =>
      hit || fetch(req).then((res) => { if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); } return res; })
    )
  );
});
