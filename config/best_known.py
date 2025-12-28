import math

# Updated targets from Centric Crystal Growth: Side = sqrt(Score * N)
# Competition primary goal: N=200
BEST_KNOWN_SIDES = {
    1: 0.92,
    50: 6.05,
    100: 7.95,
    200: 10.51 # Calculated from champion performance
}

def get_target_side(n):
    """Returns the side length to beat for a given N."""
    if n in BEST_KNOWN_SIDES:
        return BEST_KNOWN_SIDES[n]
    # Fallback estimation based on current champion trend
    return math.sqrt(n * 0.55)
