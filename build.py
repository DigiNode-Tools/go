#!/usr/bin/env python3
#
# Name:    build.py
# Purpose: Build go.diginode.tools - short links for DigiNode Tools. Run by the "Build and publish" GitHub Action
#          whenever links.json changes, and every hour.
#
#          - Named links, from links.json: go.diginode.tools/<name> goes to its address. DigiNode Tools can print
#            these links, so where one goes can be changed here at any time - every DigiNode follows straight away,
#            without upgrading.
#          - DigiFacts' short links (e.g. go.diginode.tools/7ttm, and /7TTM in capitals for QR codes): the pages are
#            made by the DigiFacts build (short-links.json on digifacts.diginode.tools), with the DigiFact's preview
#            card and click counting, and copied here.
#          - 404.html: a DigiFact short link that's newer than the last build is sent to its page on
#            digifacts.diginode.tools instead.
#
# Usage:   build.py OUT_DIR

import html
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "go.diginode.tools"
DIGIFACTS_LINKS = "https://digifacts.diginode.tools/short-links.json"
# A DigiFact's short link: four characters with no vowels (so a named link, which must have one, never clashes)
DIGIFACT_CODE_RE = re.compile(r"[bcdfghjkmnpqrstvwxz2-9]{4}")
NAME_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
RESERVED = {"index", "404", "cname"}


def fail(msg):
    sys.exit(f"ERROR: {msg}")


def redirect_page(name, url):
    u = html.escape(url, quote=True)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>DigiNode Tools link</title>'
            f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={u}">'
            f'<script>location.replace({json.dumps(url)})</script></head>'
            f'<body><p>Going to <a href="{u}">{u}</a></p></body></html>\n')


NOT_FOUND = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Link not found</title>
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<script>
// A DigiFact's short link (four characters, e.g. /7ttm or /7TTM) that's newer than this site: its page is
// already on the DigiFacts website
(function () {
  var code = location.pathname.replace(/^\\/+|\\/+$/g, "").replace(/\\.html$/, "").toLowerCase();
  if (/^[bcdfghjkmnpqrstvwxz2-9]{4}$/.test(code)) {
    location.replace("https://digifacts.diginode.tools/l/" + code + ".html" + location.search);   // Keeps a ?tag
  }
})();
</script>
<style>body{font:17px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif;max-width:560px;margin:15vh auto;padding:0 16px;color:#1d2330}
@media (prefers-color-scheme:dark){body{background:#0f1520;color:#e6ebf2}a{color:#5aa9ff}}</style></head>
<body><h1>Link not found</h1><p>This short link doesn't exist (or no longer does).</p>
<p><a href="https://diginode.tools">Go to diginode.tools</a></p></body></html>
"""


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: build.py OUT_DIR")
    out = sys.argv[1]
    files = {}

    # Named links
    with open(os.path.join(ROOT, "links.json"), encoding="utf-8") as f:
        links = json.load(f)
    for name, url in links.items():
        if name.startswith("_"):
            continue
        if not NAME_RE.fullmatch(name) or not re.search(r"[aeiouy]", name) or name in RESERVED:
            fail(f'links.json: "{name}" - names are lower case words (letters, numbers and hyphens) with a vowel')
        if not isinstance(url, str) or not re.fullmatch(r"https://\S+", url):
            fail(f'links.json: "{name}" should go to an address starting with https://')
        files[f"{name}.html"] = redirect_page(name, url)

    # DigiFacts' short links (pages made by the DigiFacts build)
    source = os.environ.get("DIGIFACTS_LINKS_FILE")   # For testing: a local short-links.json
    if source:
        with open(source, encoding="utf-8") as f:
            digifacts = json.load(f)
    else:
        req = urllib.request.Request(DIGIFACTS_LINKS, headers={"User-Agent": "go.diginode.tools build"})
        with urllib.request.urlopen(req, timeout=30) as r:
            digifacts = json.load(r)
    for code, link in digifacts.items():
        if not DIGIFACT_CODE_RE.fullmatch(code):
            fail(f"short-links.json: unexpected code {code!r}")
        files[f"{code}.html"] = link["page"]
        files[f"{code.upper()}.html"] = link["qr_page"]

    files["index.html"] = redirect_page("index", "https://diginode.tools/")
    files["404.html"] = NOT_FOUND
    files[".nojekyll"] = ""

    os.makedirs(out, exist_ok=True)
    for path, content in files.items():
        with open(os.path.join(out, path), "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Built {len(files)} files: {sum(1 for n in links if not n.startswith('_'))} named links, "
          f"{len(digifacts)} DigiFact links")


if __name__ == "__main__":
    main()
