import argparse
import json

from aevum_cost import data
from aevum_cost.calc import image_cost, video_cost, monthly


def _money(x):
    return f"${x:,.4f}".rstrip("0").rstrip(".") if x < 100 else f"${x:,.2f}"


def cmd_image(args):
    rows = [(m, image_cost(m)) for m in data.IMAGE_MODELS]
    rows.sort(key=lambda r: r[1])
    if args.json:
        print(json.dumps({m: c for m, c in rows}, indent=2))
        return
    print("Self-host cost per image (2x RTX 4090, power + amortized):")
    for m, c in rows:
        print(f"  {m:<14} {_money(c)}/image")
    best_api = min(data.API_IMAGE_BENCHMARKS.values())
    print(f"\nCheapest API benchmark: {_money(best_api)}/image "
          f"({min(data.API_IMAGE_BENCHMARKS, key=data.API_IMAGE_BENCHMARKS.get)})")
    print(f"API premium up to {data.NANO_BANANA_PRO_PREMIUM}x (Nano Banana Pro, Q3 2026)")


def cmd_video(args):
    s = args.seconds
    if args.json:
        print(json.dumps({m: video_cost(m, s) for m in data.VIDEO_MODELS},
                         indent=2))
        return
    print(f"Self-host cost for a {s:g}s clip:")
    for m in sorted(data.VIDEO_MODELS, key=lambda k: data.VIDEO_MODELS[k]["per_sec"]):
        c = video_cost(m, s)
        lim = data.VIDEO_MODELS[m]["max_seconds"]
        note = _money(c) if c is not None else f"n/a (max {lim}s)"
        print(f"  {m:<12} {note}")
    print(f"\nAPI median ({s:g}s): {_money(data.VIDEO_API_PER_SEC * s)}  "
          f"| self-host median: {_money(data.VIDEO_SELFHOST_PER_SEC * s)}")


def cmd_monthly(args):
    r = monthly(args.images, args.video_minutes)
    if args.json:
        print(json.dumps(r, indent=2))
        return
    print(f"Monthly: {args.images:,} images + {args.video_minutes:g} min video")
    print(f"  self-host ({r['self_host']['image_model']} / "
          f"{r['self_host']['video_model']}): {_money(r['self_host']['total'])}")
    print(f"  API (benchmarks):                     {_money(r['api']['total'])}")
    ref = data.Q3_REFERENCE_MONTHLY
    print(f"\nQ3 reference (50k images + 100 min): API {_money(ref['api'])} vs "
          f"self-host {_money(ref['self_host'])}, payback {ref['payback_months']} months")


def cmd_report(args):
    print("Aevum Cost Report - 2026 Q3 headlines:")
    for i, h in enumerate(data.Q3_HEADLINES, 1):
        print(f"  {i}. {h}")


def main():
    p = argparse.ArgumentParser(prog="aevum-cost",
                                description="Real GPU cost per image / per video second")
    sub = p.add_subparsers(dest="cmd")
    pi = sub.add_parser("image", help="per-image self-host table")
    pv = sub.add_parser("video", help="cost for a clip of N seconds")
    pv.add_argument("--seconds", type=float, default=30)
    pm = sub.add_parser("monthly", help="monthly estimate vs API")
    pm.add_argument("--images", type=int, default=0)
    pm.add_argument("--video-minutes", type=float, default=0.0)
    sub.add_parser("report", help="quarterly headline numbers")
    for sp in (pi, pv, pm):
        sp.add_argument("--json", action="store_true")
    args = p.parse_args()
    {"image": cmd_image, "video": cmd_video,
     "monthly": cmd_monthly, "report": cmd_report,
     None: cmd_image}[args.cmd](args)


if __name__ == "__main__":
    main()
