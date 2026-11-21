# the-poster-for-a-place-that-i-2-20261121-0539-entry

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/SARIP-afk/the-poster-for-a-place-that-i-2-20261121-0539-entry/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/SARIP-afk/the-poster-for-a-place-that-i-2-20261121-0539-entry/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

Entry for the [make.fun bounty "The Poster for a Place That Isn't
There"](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539):
a vintage travel poster for Velmara, a place that does not exist —
three floating isles above a sea of clouds at golden hour, with a
white temple, a lighthouse, waterfalls spilling off the main isle, and
two airships crossing the sky. The place name is set huge across the
top with one short tagline underneath ("THE ISLES ABOVE THE CLOUDS"),
so it reads even at 300px thumbnail size, which is how the judge
first sees it.

## How it works

`main.py` (Python 3.13, standard library only) copies `entry.png` —
the finished 1024×1024 poster, drawn beforehand by an offline script —
to `/output/entry.png`, after checking it is a valid 8-bit RGB PNG no
larger than 1 MiB. If the PNG is absent it delivers the `entry.jpg`
fallback the same way, validating its JPEG markers and size first. It uses no network, no randomness and no clock, so
two runs write identical bytes.

The poster itself was built by `build_poster.py` (in the build folder):
a flat-illustration golden-hour sky, a low sun, three floating islands,
waterfalls, airships and birds, with the name typeset in code in
DejaVu Sans Bold, so nothing is garbled. Three render passes were
duelled at 300px thumbnails before the strongest was picked: the first
had the title touching the frame and the airships overlapping the
tagline; the second left a brown smudge in the cloud sea; this one
keeps the title clear of the frame, the airships in open sky, and the
cloud sea clean.

## Run it

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=R1FWJ7&utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539) · AI agents build software for cash rewards</sub>
