import subprocess
import sys

sys.path.insert(0, ".")

from aevum_cost import data
from aevum_cost.calc import image_cost, video_cost, monthly


def test_image_cost():
    assert image_cost("z-image-turbo", 1000) == 5.0
    assert image_cost("flux2-dev") == 0.035
    print("PASS image cost")


def test_video_cost_and_limits():
    assert video_cost("svi-wan22", 30) == 1.2
    assert video_cost("wan2.2-14b", 30) is None      # exceeds 6s cap
    assert video_cost("ltx-2.5", 20) == 1.0
    assert video_cost("ltx-2.5", 21) is None
    print("PASS video cost + limits")


def test_monthly():
    r = monthly(50000, 100)
    assert r["self_host"]["total"] < r["api"]["total"]
    assert r["api"]["video"] == 900.0                # 100 min at $0.15/s
    print(f"PASS monthly: {r['self_host']['total']} vs {r['api']['total']}")


def test_q3_consistency():
    assert abs(data.VIDEO_API_PER_SEC * 30 - 4.50) < 1e-9
    assert abs(data.VIDEO_SELFHOST_PER_SEC * 30 - 0.72) < 1e-9
    assert len(data.Q3_HEADLINES) == 5
    print("PASS q3 consistency")


def test_cli():
    for cmd in (["image"], ["video", "--seconds", "30"],
                ["monthly", "--images", "50000", "--video-minutes", "100"],
                ["report"]):
        r = subprocess.run([sys.executable, "-m", "aevum_cost.cli", *cmd],
                           capture_output=True, text=True, cwd=".")
        assert r.returncode == 0, (cmd, r.stderr)
    print("PASS cli")


if __name__ == "__main__":
    test_image_cost(); test_video_cost_and_limits()
    test_monthly(); test_q3_consistency(); test_cli()
    print("ALL COST TESTS PASSED")
