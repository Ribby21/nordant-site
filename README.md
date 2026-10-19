# nordant-site

The website for **Nordant**, at https://playnordant.com: static HTML and one stylesheet, hosted on GitHub Pages.

The pages are written by `scripts/build.py` (shared head, bar and foot in `scripts/parts.py`):
edit the text there and run `python scripts/build.py .` from this folder, rather than editing the HTML.

| Page | What it's for |
|---|---|
| `index.html` | Home: what the game is, the Google Play badge |
| `leaderboard.html` | The top ranked players, read live from the game's server (`GET /v1/leaderboard`) |
| `get.html` | A link to share: sends Android phones straight to Google Play |
| `support.html` | Support and FAQ (the store listings need a support URL) |
| `privacy.html`, `terms.html` | The privacy policy and terms of service |
| `delete-account.html` | How to delete an account (Google Play requires this URL) |

Keep `/privacy.html` and `/delete-account.html` where they are: the Play listing links to them.
