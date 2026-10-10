# Meringo Listen — website

The marketing + legal site for **Meringo Listen**, served at **https://meringolisten.app**.

It is a static, single-page site (no build step, no framework), built on the Meringo Labs
house kit like [`meringo-web`](https://github.com/meringo-music/meringo-web), the Meringo site.
Just HTML, the kit's three CSS files, self-hosted fonts, and screenshots.

```
index.html            # the whole page; its own <style> holds page-only rules, no script
404.html              # served by GitHub Pages for any missing path
colors_and_type.css   # house kit: tokens, @font-face, type roles
room-listen.css       # house kit: Listen's differences from the base
house.css             # house kit: the h- components
CNAME                 # meringolisten.app  (GitHub Pages custom domain)
robots.txt · sitemap.xml
assets/fonts/         # Cormorant Garamond · Inter · Share Tech Mono (woff2) + OFL.txt
assets/img/           # listen-icon.svg (the launcher icon, also the favicon) · meringo-mark.svg
assets/screens/       # app screenshots (WebP + PNG fallback)
assets/og.png         # 1200x630 social card
tools/og/make_og.py   # regenerates assets/og.png (needs Pillow, fontTools, brotli)
```

The three kit files, the fonts and the two marks are vendored byte for byte from the house
kit (`meringo-labs/design/`, checked against its `MANIFEST.txt`). Never edit them here:
change the kit, then copy them again.

## Preview locally

```powershell
python -m http.server 8102    # then open http://127.0.0.1:8102
```

Serve the repo root: the pages use root paths (`/house.css`, `/assets/...`), so opening
`index.html` straight from disk loads no styles.

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

## Launch day: flip beta → live

The site ships in **"Request access"** mode for closed testing. To switch to the live
Google Play CTA when the app is public, change one attribute in `index.html`:

```html
<body data-cta-state="beta">   <!-- change to:  data-cta-state="live" -->
```

That hides every `.cta-state-beta` element and shows the `.cta-state-live` ones
(the title page, the header link, the FAQ and the get-it section): the Google Play button to
`https://play.google.com/store/apps/details?id=app.meringo.listen`.

The attribute can't switch what sits in `<head>`. Check these in the same change: the
`<title>`, the meta description, the og and twitter tags, and the first JSON-LD block (its
`offers.availability` is `PreOrder`, and it carries no `softwareVersion`).

## Play Console note

Use **`https://meringolisten.app/#privacy`** as the privacy-policy URL (the internal
launch docs had a `meringo.app/listen/privacy` placeholder — this domain supersedes it).

## Regenerate assets

- **Screenshots** — drop new PNGs in `assets/screens/`, then make WebP siblings:
  `ffmpeg -i in.png -c:v libwebp -quality 80 -compression_level 6 out.webp`
- **OG card** — `python tools/og/make_og.py`
