# Private Competition Data - Santa 2025 Tree Packing
from decimal import Decimal

# Exact Tree Vertices (Clockwise from Tip)
# Derived from: 
# top_w=0.25, mid_w=0.4, base_w=0.7, trunk_w=0.15
# tip_y=0.8, tier_1_y=0.5, tier_2_y=0.25, base_y=0.0, trunk_h=0.2
TREE_COORDS = [
    (0.0, 0.8),           # Tip
    (0.125, 0.5),         # Top Tier Edge (R)
    (0.0625, 0.5),        # Top Tier Step (R)
    (0.2, 0.25),          # Mid Tier Edge (R)
    (0.1, 0.25),          # Mid Tier Step (R)
    (0.35, 0.0),          # Base Tier Edge (R)
    (0.075, 0.0),         # Trunk Edge (R)
    (0.075, -0.2),        # Trunk Bottom (R)
    (-0.075, -0.2),       # Trunk Bottom (L)
    (-0.075, 0.0),        # Trunk Edge (L)
    (-0.35, 0.0),         # Base Tier Edge (L)
    (-0.1, 0.25),         # Mid Tier Step (L)
    (-0.2, 0.25),         # Mid Tier Edge (L)
    (-0.0625, 0.5),       # Top Tier Step (L)
    (-0.125, 0.5)         # Top Tier Edge (L)
]

# Scale Factor for Metric
SCALE_FACTOR = Decimal('1e18')

# Benchmarking Targets (Side Lengths to beat)
# N=200 is the primary competition limit
BEST_KNOWN_SIDES = {
    1: 0.92,
    50: 6.05,
    100: 7.95,
    200: 10.51
}

# Jigsaw Empirical Offsets (Refined for Jigsaw interlock)
JIGSAW_DX = 0.40
JIGSAW_DY = 0.69