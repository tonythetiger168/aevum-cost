"""Cost calculations on top of data.py. Pure stdlib."""
from aevum_cost import data


def image_cost(model: str, n: int = 1) -> float:
    """Self-host USD for n images on the given model."""
    return round(data.IMAGE_MODELS[model]["self_host"] * n, 4)


def video_cost(model: str, seconds: float):
    """Self-host USD for a clip; None if the model cannot reach that length."""
    m = data.VIDEO_MODELS[model]
    if m["max_seconds"] is not None and seconds > m["max_seconds"]:
        return None
    return round(m["per_sec"] * seconds, 4)


def monthly(images: int = 0, video_minutes: float = 0.0,
            image_model: str = "sd35-medium", video_model: str = "svi-wan22") -> dict:
    """Monthly estimate: self-host (chosen models) vs API (benchmark medians)."""
    self_images = image_cost(image_model, images)
    self_video = video_cost(video_model, video_minutes * 60)
    if self_video is None:  # fell outside model limit: use blended median rate
        self_video = round(data.VIDEO_SELFHOST_PER_SEC * video_minutes * 60, 2)
    api_images = round(data.API_IMAGE_BENCHMARKS["seedream-5.0-pro"] * images, 2)
    api_video = round(data.VIDEO_API_PER_SEC * video_minutes * 60, 2)
    return {
        "self_host": {"images": self_images, "video": round(self_video, 2),
                      "total": round(self_images + self_video, 2),
                      "image_model": image_model, "video_model": video_model},
        "api": {"images": api_images, "video": api_video,
                "total": round(api_images + api_video, 2),
                "image_benchmark": "seedream-5.0-pro",
                "video_benchmark": "api-median"},
    }
