import pytest
import numpy as np


def compute_finger_states(lm_list):
    """
    Computes finger up/down state from a list of 21 hand landmarks [id, x, y].
    Matches the geometric detection algorithm in Mini Projects/FingerState/FingerState.py.
    """
    if len(lm_list) < 21:
        return [0, 0, 0, 0, 0]

    tip_ids = [4, 8, 12, 16, 20]
    pip_ids = [3, 7, 11, 15, 19]
    fingers = []

    # Thumb calculation (distance to pinky MCP landmark 17)
    thumb_tip = lm_list[4]
    thumb_mcp = lm_list[2]
    pinky_mcp = lm_list[17]

    dist_tip_to_pinky = np.hypot(thumb_tip[1] - pinky_mcp[1], thumb_tip[2] - pinky_mcp[2])
    dist_mcp_to_pinky = np.hypot(thumb_mcp[1] - pinky_mcp[1], thumb_mcp[2] - pinky_mcp[2])
    fingers.append(1 if dist_tip_to_pinky > dist_mcp_to_pinky else 0)

    # 4 fingers (Index, Middle, Ring, Pinky) - Y-coordinate comparison
    for i in range(1, 5):
        if lm_list[tip_ids[i]][2] < lm_list[pip_ids[i]][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def test_insufficient_landmarks():
    assert compute_finger_states([]) == [0, 0, 0, 0, 0]
    assert compute_finger_states([[i, 100, 100] for i in range(10)]) == [0, 0, 0, 0, 0]


def test_all_fingers_up():
    # Build 21 landmarks where tips are above PIPs (lower Y)
    lm = [[i, 200, 300] for i in range(21)]
    # Pinky MCP at (100, 300)
    lm[17] = [17, 100, 300]
    # Thumb MCP at (200, 300) -> dist = 100
    lm[2] = [2, 200, 300]
    # Thumb tip at (300, 300) -> dist = 200 (further than MCP)
    lm[4] = [4, 300, 300]

    # For index (8), middle (12), ring (16), pinky (20): tips at Y=100, pips at Y=200
    tip_ids = [8, 12, 16, 20]
    pip_ids = [7, 11, 15, 19]
    for tip, pip in zip(tip_ids, pip_ids):
        lm[tip] = [tip, 200, 100]
        lm[pip] = [pip, 200, 200]

    states = compute_finger_states(lm)
    assert states == [1, 1, 1, 1, 1]


def test_closed_fist():
    # Build 21 landmarks where tips are curled down below PIPs (higher Y)
    lm = [[i, 200, 300] for i in range(21)]
    lm[17] = [17, 200, 300]
    lm[2] = [2, 200, 300]
    lm[4] = [4, 200, 300]  # thumb folded in

    tip_ids = [8, 12, 16, 20]
    pip_ids = [7, 11, 15, 19]
    for tip, pip in zip(tip_ids, pip_ids):
        lm[tip] = [tip, 200, 350]  # Tip lower than PIP
        lm[pip] = [pip, 200, 250]

    states = compute_finger_states(lm)
    assert states == [0, 0, 0, 0, 0]


def test_index_finger_pointing_only():
    lm = [[i, 200, 300] for i in range(21)]
    lm[17] = [17, 200, 300]
    lm[2] = [2, 200, 300]
    lm[4] = [4, 200, 300]  # thumb closed

    # Index finger extended (tip 8 at Y=100, pip 7 at Y=200)
    lm[8] = [8, 200, 100]
    lm[7] = [7, 200, 200]

    # Middle, Ring, Pinky curled
    for tip, pip in zip([12, 16, 20], [11, 15, 19]):
        lm[tip] = [tip, 200, 350]
        lm[pip] = [pip, 200, 250]

    states = compute_finger_states(lm)
    assert states == [0, 1, 0, 0, 0]
