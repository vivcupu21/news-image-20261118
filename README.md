[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/vivcupu21/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/vivcupu21/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

# The World in One Image — Wednesday, 18 November 2026

A one-page newspaper front page that sums up the world news of
Wednesday 18 November 2026 in a single image. The program is
[main.py](main.py) (Python 3.13, standard library only): it copies the
image stored in this repository ([entry.png](entry.png)) to
`/output/entry.png`. No network, no randomness, no timestamps — every
run writes the exact same bytes.

The image itself is drawn from scratch by [draw_entry.py](draw_entry.py)
(Pillow, flat vector-style panels and text; no external images): a
masthead naming the day, a lead story, four more main stories and an
"Also today" strip.

## The day's news in the image

- **Lead — APEC opens in Shenzhen, China.** World leaders gather as
  Trump, Xi and Putin converge on the summit city; trade, AI and
  security top the agenda.
- **QUAD meets in Manila.** Trump joins Modi, Albanese and Takaichi;
  leaders unveil a new plan on maritime security, an AI accelerator
  and undersea cables.
- **Trump–Xi–Putin summit set.** The first-ever three-way summit is
  announced for tomorrow, 19 November, in Shenzhen: nuclear arms,
  Ukraine, Iran, trade and AI.
- **Ukraine hits the Crimean Bridge.** Missiles and drones drop a road
  span into the Kerch Strait; Russia answers by striking two bridges
  in Kyiv.
- **Gulf flashpoint.** Iranian drones strike a US radar base in
  Bahrain — the third attack in five days; the US hits an IRGC
  missile base on Qeshm Island.
- **Cyclone Akvan nears India.** The storm strengthens toward Andhra
  Pradesh; landfall due 20 November.
- **Also today:** MS Dhoni retires from the IPL; Eisenkot is tapped to
  form Israel's next government; four nations urge Israel to open Gaza
  aid routes; North Korea fires a missile into the Sea of Japan; a
  cyber-attack hits supermarket freezers in 7 countries.

Sources: Reuters, NDTV, Al Jazeera, AP, France 24 — all reported
18 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entrypoint: copies `entry.png` to the output directory.
- `entry.png` — the image (1024×1024, PNG, under 1 MiB).
- `draw_entry.py` — the script that drew `entry.png` from scratch.
- `LICENSE` — MIT.

## License

MIT — see [LICENSE](LICENSE).
