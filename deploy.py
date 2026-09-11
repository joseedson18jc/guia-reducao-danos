#!/usr/bin/env python3
"""
Publish the site/ folder to https://guia-ghb.netlify.app

    npx netlify-cli login        # once per machine
    python3 deploy.py --draft    # preview deploy at a temporary URL, production untouched
    python3 deploy.py            # publish to production

The whole site lives in site/, so this is a plain snapshot deploy. After a
production deploy the script fetches the live pages and confirms their bytes
match the files here.
"""
import hashlib
import os
import subprocess
import sys

SITE_ID = "d2e20143-bd73-4cb8-afef-fb8597f94724"
LIVE_URL = "https://guia-ghb.netlify.app"
REPO = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(REPO, "site")
NETLIFY = ["npx", "--yes", "netlify-cli"]
CHECK = {"/": "index.html", "/ghb/": "ghb/index.html", "/metanfetamina/": "metanfetamina/index.html"}


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def strip_netlify_injections(html: bytes) -> bytes:
    """Netlify adds a hosting comment, two meta tags and a script to HTML on
    free-plan sites. Remove them so live bytes can be compared to the repo."""
    import re
    text = html.decode("utf-8", errors="replace")
    text = re.sub(r"<!-- This site is hosted on Netlify\..*?-->\n?", "", text, flags=re.S)
    text = re.sub(r'<meta name="(?:hosting-provider|netlify-deploy)"[^>]*>\n?', "", text)
    text = re.sub(r'<script async src="/\.netlify/scripts/hud[^>]*></script>\n?', "", text)
    return text.encode("utf-8")


def fetch(path: str) -> bytes:
    # curl, not urllib: this Mac's python.org Python has no CA bundle.
    res = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                          "--max-time", "60", "-H", "Accept-Encoding: identity",
                          "-H", "Cache-Control: no-cache", "--output", "-", LIVE_URL + path],
                         capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.decode(errors="replace").strip())
    return res.stdout


def main():
    draft = "--draft" in sys.argv
    if not os.path.isfile(os.path.join(SITE_DIR, "ghb", "index.html")):
        sys.exit("site/ghb/index.html not found")
    args = NETLIFY + ["deploy", "--site", SITE_ID, "--dir", SITE_DIR,
                      "--message", "deploy.py from guia-ghb repository"]
    if not draft:
        args.append("--prod")
    print(("Draft" if draft else "Production") + " deploy of site/ …", flush=True)
    rc = subprocess.run(args, cwd=REPO).returncode
    if rc != 0:
        sys.exit(f"netlify deploy exited with status {rc}; the previous deploy remains live.")
    if draft:
        return
    print("\nVerifying live pages…")
    ok = True
    for path, rel in CHECK.items():
        local = sha1(open(os.path.join(SITE_DIR, rel), "rb").read())
        try:
            live = sha1(strip_netlify_injections(fetch(path)))
        except RuntimeError as e:
            print(f"  {path}: fetch failed: {e}"); ok = False; continue
        match = live == local
        ok &= match
        print(f"  {path}: {'OK, matches repository' if match else 'DIFFERS from repository (CDN cache? retry in a minute)'}")
    print("\nLive:", LIVE_URL + "/ghb/" if ok else "verification incomplete, see above")


if __name__ == "__main__":
    main()
