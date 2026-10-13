# go.diginode.tools

Short links for [DigiNode Tools](https://diginode.tools).

- **Links used by DigiNode Tools** - DigiNode Tools prints links like `https://go.diginode.tools/digifacts`. Where each one goes is set in [`links.json`](links.json), so it can be changed at any time, and every DigiNode follows straight away - nobody needs to upgrade. Pages on diginode.tools itself are linked to directly; these are for links elsewhere, or ones likely to change.
- **DigiFacts' short links** - every [DigiFact](https://digifacts.diginode.tools) with a link has a short link, e.g. `https://go.diginode.tools/7ttm` (and `HTTPS://GO.DIGINODE.TOOLS/7TTM` in capitals, which makes smaller QR codes). They're made by the DigiFacts build, with a preview card for when they're shared and click counting, and copied here every hour.

## Adding or changing a link

Edit [`links.json`](links.json): `"name": "https://where-it-goes"`. A name is a lower case word (letters, numbers and hyphens) and must contain a vowel - so it can never clash with a DigiFact's short link, which never has one. The site is rebuilt and published automatically, in about a minute.

Don't remove a link that DigiNode Tools has used - older versions may still print it. Point it somewhere useful instead.

## How it's built

[`build.py`](build.py) makes a redirect page for each link, run by a [GitHub Action](.github/workflows/build.yml) whenever `links.json` changes and every hour. A DigiFact short link that's newer than the last build is sent to its page on the DigiFacts website by the "not found" page.

## Licence

Part of DigiNode Tools: free to use, and the code is public so anyone can see exactly what it does. Licensed under the [PolyForm Perimeter 1.0.0](LICENCE.md) licence, which doesn't allow it to be used to make a competing product - see the [Licence FAQ](https://github.com/DigiNode-Tools/diginode-tools/blob/main/docs/licence_faq.md). The DigiNode Tools name and logo are covered by [TRADEMARKS.md](https://github.com/DigiNode-Tools/diginode-tools/blob/main/TRADEMARKS.md).
