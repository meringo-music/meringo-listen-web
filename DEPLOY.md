# Meringo Listen — website

The marketing + legal site for **Meringo Listen**, served at **https://meringolisten.app**.

It is a static, single-page site (no build step, no framework) — the same shape as
[`meringo-web`](https://github.com/meringo-music/meringo-web), the Meringo Music site.
Just HTML, one CSS file, self-hosted fonts, and screenshots.

```
index.html            # the whole page (inline <style> + <script>)
colors_and_type.css   # design tokens + @font-face + type classes
CNAME                 # meringolisten.app  (GitHub Pages custom domain)
robots.txt · sitemap.xml
assets/fonts/         # Cormorant Garamond · Outfit · JetBrains Mono (woff2)
assets/screens/       # device screenshots (WebP + PNG fallback)
assets/og.png         # 1200x630 social card
assets/logo.svg · logo-icon.svg
tools/og/make_og.py   # regenerates assets/og.png (needs Pillow)
```

## Preview locally

```powershell
python -m http.server 8099    # then open http://127.0.0.1:8099
```

## One-time hosting setup (mirrors meringo.app)

**1 — GitHub repo + Pages**

1. Create a repo named **`meringo-listen-web`** under the **`meringo-music`** org and push these files to `main` (root).
2. Repo → **Settings → Pages** → *Build and deployment* → **Deploy from a branch** → branch **`main`**, folder **`/ (root)`**.
3. Set **Custom domain** to `meringolisten.app` (this is what the `CNAME` file already contains).
4. After DNS resolves (below), tick **Enforce HTTPS**.

**2 — Porkbun DNS** (Domain Management → `meringolisten.app` → DNS / Edit)

Delete the default Porkbun **parking** records (the apex `A`/`ALIAS` pointing at Porkbun, the default `www` record) and disable **URL Forwarding**. Then add — identical to what `meringo.app` uses:

| Type  | Host (Porkbun) | Answer                  | TTL |
|-------|----------------|-------------------------|-----|
| A     | *(blank = @)*  | `185.199.108.153`       | 600 |
| A     | *(blank)*      | `185.199.109.153`       | 600 |
| A     | *(blank)*      | `185.199.110.153`       | 600 |
| A     | *(blank)*      | `185.199.111.153`       | 600 |
| AAAA  | *(blank)*      | `2606:50c0:8000::153`   | 600 |
| AAAA  | *(blank)*      | `2606:50c0:8001::153`   | 600 |
| AAAA  | *(blank)*      | `2606:50c0:8002::153`   | 600 |
| AAAA  | *(blank)*      | `2606:50c0:8003::153`   | 600 |
| CNAME | `www`          | `meringo-music.github.io` | 600 |

**3 — Verify**

```powershell
nslookup meringolisten.app       # expect the four 185.199.108-111.153 addresses
```
Then in GitHub Pages wait for "DNS check successful" and enable **Enforce HTTPS**.
(Porkbun's `ALIAS` type could flatten the apex to `meringo-music.github.io` instead of
the four A records, but A records match Music exactly — prefer them. Leave email/MX alone.)

## Launch day (target 2026-09-08): flip beta → live

The site ships in **"Request access"** mode for closed testing. To switch to the live
Google Play CTA when the app is public, change one attribute in `index.html`:

```html
<body data-cta-state="beta">   <!-- change to:  data-cta-state="live" -->
```

That hides every `.cta-state-beta` element and shows the `.cta-state-live` ones
(hero, nav, FAQ, get-app) — the Google Play button to
`https://play.google.com/store/apps/details?id=app.meringo.listen`.

## Play Console note

Use **`https://meringolisten.app/#privacy`** as the privacy-policy URL (the internal
launch docs had a `meringo.app/listen/privacy` placeholder — this domain supersedes it).

## Regenerate assets

- **Screenshots** — drop new PNGs in `assets/screens/`, then make WebP siblings:
  `ffmpeg -i in.png -c:v libwebp -quality 80 -compression_level 6 out.webp`
- **OG card** — `python tools/og/make_og.py`
