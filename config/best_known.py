import math

# Target side lengths derived from Greedy Baseline: Score = (Side^2) / N => Side = sqrt(Score * N)
BEST_KNOWN_SIDES = {
    1: 0.92,
    50: 6.41,
    100: 9.27,
    250: 14.54
}

def get_target_side(n):
    """Returns the side length to beat for a given N."""
    if n in BEST_KNOWN_SIDES:
        return BEST_KNOWN_SIDES[n]
    # Fallback estimation for other N
    return math.sqrt(n * 0.85)
