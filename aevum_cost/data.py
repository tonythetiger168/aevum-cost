"""Aevum Cost data - 2026 Q3.

Self-host rates: measured on 2x RTX 4090, power + amortized hardware,
from aevum-platform app/router.py (image) and app/video.py (video).
API benchmarks: vendor list prices / median of major vendors,
from aevum-platform docs/COST_REPORT_Q3.md and docs/SEEDREAM_COMPARISON.md.
"""

# self-host cost per image, USD
IMAGE_MODELS = {
    "z-image-turbo": {"self_host": 0.005,
                      "note": "cost floor $0.003/image at scale (Q3 report)"},
    "sd35-medium":   {"self_host": 0.018},
    "qwen-image":    {"self_host": 0.022},
    "flux2-dev":     {"self_host": 0.035},
}

# API list price per image, USD (benchmark vendors)
API_IMAGE_BENCHMARKS = {
    "seedream-4.0":     0.03,
    "seedream-4.5":     0.04,
    "seedream-5.0-lite": 0.035,
    "seedream-5.0-pro": 0.045,
}

# self-host cost per video second, USD
VIDEO_MODELS = {
    "ltx-video":  {"per_sec": 0.015, "max_seconds": 5},
    "wan2.2-5b":  {"per_sec": 0.02,  "max_seconds": 5},
    "svi-wan22":  {"per_sec": 0.04,  "max_seconds": None},  # SVI error-recycling: unbounded
    "ltx-2.5":    {"per_sec": 0.05,  "max_seconds": 20},
    "wan2.2-14b": {"per_sec": 0.06,  "max_seconds": 6},
}

# Q3 2026 medians / ratios
VIDEO_30S_API_MEDIAN = 4.50        # median across major API vendors
VIDEO_30S_SELFHOST_MEDIAN = 0.72   # mixed routing, measured
VIDEO_API_PER_SEC = round(VIDEO_30S_API_MEDIAN / 30, 4)      # 0.15
VIDEO_SELFHOST_PER_SEC = round(VIDEO_30S_SELFHOST_MEDIAN / 30, 4)  # 0.024
NANO_BANANA_PRO_PREMIUM = 9.6      # highest API/self-host ratio observed
LTX25_AV_20S_SELFHOST = 0.20       # 20s audio+video joint generation

Q3_HEADLINES = [
    "Sora 2 API sunset 2026-09-24",
    "30s video median: API $4.50 vs self-host $0.72 (6.3x)",
    "Highest API premium: Nano Banana Pro 9.6x",
    "Cost floor: Z-Image Turbo self-host $0.003/image at scale",
    "LTX 2.5 rewrote the curve: 20s audio+video self-host $0.20",
]

# Reference case from Q3 report: 50k images + 100 min video per month
Q3_REFERENCE_MONTHLY = {"api": 4050.0, "self_host": 890.0, "payback_months": 2.3}
