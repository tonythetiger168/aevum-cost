# aevum-cost

Real cost of AI image/video generation — per image, per second,
self-host vs API. Zero dependencies, data updated quarterly.

    pip install aevum-cost
    aevum-cost image                       # per-image table, 4 self-host models
    aevum-cost video --seconds 30          # per-model cost for a 30s clip
    aevum-cost monthly --images 50000 --video-minutes 100
    aevum-cost report                      # 2026 Q3 headline numbers

## 2026 Q3 headlines
- 30s video, median: **API $4.50 vs self-host $0.72 — 6.3x gap**
- Highest API premium: Nano Banana Pro **9.6x**
- Cost floor: Z-Image Turbo self-host **$0.003/image** at scale
- LTX 2.5 rewrote the curve: 20s audio+video self-host **$0.20**
- Sora 2 API sunset 2026-09-24

Self-host rates are measured on 2x RTX 4090 (power + amortized hardware);
API prices are list prices from vendor pages. Sources per figure in
`aevum_cost/data.py`. Methodology PRs welcome.

## See also
- [aevum-scorer](https://github.com/aevum-ai/aevum-scorer) — quality scoring pipeline
- [aevum-workflows](https://github.com/aevum-ai/aevum-workflows) — 336 ComfyUI workflows

---
Quarterly reports are published by [Aevum](https://aevum.ai?utm_source=cost),
the self-hosted video generation platform. Self-hosting section of each
report shows the hardware math behind these numbers. Apache-2.0.
