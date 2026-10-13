def clamp(value, minimum=0.0, maximum=1.0):
    return max(minimum, min(value, maximum))


def lerp(start, end, t):
    t = clamp(t)
    return start + (end - start) * t


def ease_out_cubic(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t):
    t = clamp(t)

    if t < 0.5:
        return 4 * t * t * t

    return 1 - ((-2 * t + 2) ** 3) / 2


def ease_out_back(t):
    """
    Slight overshoot at the end.
    Good for countdown numbers / snapping.
    """
    t = clamp(t)

    c1 = 1.70158
    c3 = c1 + 1

    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2