# Guia GHB

Source of <https://guia-ghb.netlify.app>: Portuguese-language educational and
harm-reduction guides. Static site, no build step.

```
site/            the whole site, deployed as-is
  index.html     homepage
  ghb/index.html            GHB / GBL / 1,4-BD guide: inline CSS+JS, two <canvas> charts
  metanfetamina/index.html  methamphetamine dossier: evidence-graded, 22 DOI refs,
                            3D molecule, circuit, PK simulator, addiction wheel
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

## Where the repository lives

`~/guia-ghb`. Do not keep it on the Desktop: iCloud Drive manages that folder
on this Mac and evicts files to the cloud, which blocks git on every read.

## History

The guide originally lived at guia-oilbong-fisica.netlify.app under a Netlify
account this machine has no access to. The first commit in this repository is
that page exactly as served; the homepage and assets were mirrored from the
same site when it moved here on 2026-09-11.
