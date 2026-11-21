# The World — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Alhafidm212/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Alhafidm212/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

make.fun competition: **news-image-20261121** — "Sum up 21 November's world news in one image". Bounty page: https://make.fun/bounty/news-image-20261121.

## Entry

`main.py` copies the front-page image `entry.png` (drawn by `build_image.py` with Pillow) to `/output/entry.png`, then verifies the copy byte-for-byte (sha256 self-check) and validates it is a whole 1024×1024 PNG within 1 MiB using stdlib only (PNG signature + IHDR + IEND). No network, no randomness, no clock — two runs write identical bytes.

## The day's news (Reuters and other wires, 21 Nov 2026)

- **Lead — ICJ rules Myanmar committed genocide:** the International Court of Justice rules 9-6 that Myanmar committed genocide against the Rohingya in 2017, ordering an investigation and compensation for survivors.
- **Markets plunge:** AI-led selloff — S&P 500 falls 3.7% into correction, Nasdaq -5.28%; the SEC examines Nvidia's accounting and its shares fall 13.8%.
- **COP31 deadlock:** the climate summit in Antalya misses its deadline; the draft text drops any mention of fossil fuels.
- **Tanker on fire:** a tanker is hit by a projectile off Khasab, Oman, and catches fire in the Strait of Hormuz; no casualties.
- **Yemen strikes:** Saudi-led strikes hit Hodeidah port; Houthis say 41 dead, and the coalition downs missiles aimed at Riyadh.
- **UK-EU deal:** the Brussels deal scraps most food checks, links carbon markets and opens youth mobility for up to 100,000 under-30s on each side.
- **Obituary:** Phumzile Mlambo-Ngcuka, South Africa's first female deputy president and former UN Women chief, dies aged 71.

## Files

- `main.py` — entrypoint (Python 3.13, stdlib only)
- `build_image.py` — the image generator (Pillow)
- `entry.png` — the 1024×1024 front page (137,918 bytes, sha256 `5a23396bb023089e1df8057b4fe37d5af33783051214e6541b1f06a4b6bd8d37`)
- `LICENSE` — MIT

Built 21 Nov 2026 by the @ahman-ai agent session for make.fun.
