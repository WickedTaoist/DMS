from typing import List


def smooth_labels(labels: List[str], max_gap_frames: int) -> List[str]:
    """
    Fill short normal gaps between suspicious segments to reduce flickering.

    This function intentionally keeps simple logic for research iteration.
    """
    if not labels:
        return labels
    smoothed = labels[:]
    n = len(labels)
    for i in range(1, n - 1):
        if labels[i] == "normal" and labels[i - 1] != "normal":
            j = i
            while j < n and labels[j] == "normal":
                j += 1
            gap = j - i
            if j < n and gap <= max_gap_frames and labels[j] != "normal":
                for k in range(i, j):
                    smoothed[k] = labels[i - 1]
    return smoothed
