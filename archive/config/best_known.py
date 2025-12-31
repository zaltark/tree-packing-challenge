import math
try:
    from config.magic_params import BEST_KNOWN_SIDES
except ImportError:
    BEST_KNOWN_SIDES = {}

def get_target_side(n):
    """Returns the side length to beat for a given N."""
    if n in BEST_KNOWN_SIDES:
        return BEST_KNOWN_SIDES[n]
    # Fallback estimation based on current champion trend
    return math.sqrt(n * 0.55)