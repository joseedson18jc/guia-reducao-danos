# Guia GHB

Source of <https://guia-ghb.netlify.app>: a Portuguese-language harm-reduction
guide on GHB, GBL and 1,4-butanodiol. Static site, no build step.

```
site/            the whole site, deployed as-is
  index.html     homepage
  ghb/index.html the guide: inline CSS, inline JS, two <canvas> charts
  ghb/og-ghb-v2.png, og.png, favicons, robots.txt, sitemap.xml
```

## Preview locally

```bash
python3 -m http.server 8899 --directory site
```

then open <http://localhost:8899/ghb/>.

## Publish

```bash
npx netlify-cli login        # once per machine
python3 deploy.py --draft    # preview at a temporary URL, production untouched
python3 deploy.py            # publish, then verify the live bytes
```

## History

The guide originally lived at guia-oilbong-fisica.netlify.app under a Netlify
account this machine has no access to. The first commit in this repository is
that page exactly as served; the homepage and assets were mirrored from the
same site when it moved here on 2026-09-11.
