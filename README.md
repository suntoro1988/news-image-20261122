# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/suntoro1988/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/suntoro1988/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world news of Sunday 22 November 2026: 45 stories from 7 regions and 20 fields, each verified to two sources. The day's biggest story is the collapse of the COP31 climate talks in Antalya with no deal, followed by the Democrats locking 258 House seats — their biggest majority since 1992 — and Verstappen winning a chaotic Las Vegas Grand Prix. Every story is dated to 22 November; a DATE CHECK box names the older news deliberately left out (Kerch Bridge strikes, the Chapo Isidro capture, the Bayelsa boat sinking, the EU–Indonesia deal, the ICJ Myanmar ruling, the FBI database hack). The image is drawn in code by `draw.py` from the verified list in `news.json`, with a UTC timeline of the day, key numbers, region counts, and a dotted world map with numbered pins.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `entry.png` to the output directory. To redraw the image from its data, run `python3 draw.py` first (needs Pillow; the result is byte-identical to the shipped `entry.png`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=makefun-vase-isthmus-atrium&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
