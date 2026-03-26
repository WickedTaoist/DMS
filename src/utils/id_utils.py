import hashlib


def make_event_id(video_id: str, start_idx: int, end_idx: int) -> str:
    seed = f"{video_id}:{start_idx}:{end_idx}".encode("utf-8")
    digest = hashlib.md5(seed).hexdigest()[:10]
    return f"evt_{digest}"
