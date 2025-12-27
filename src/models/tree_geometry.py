from decimal import Decimal, getcontext
from shapely import affinity
from shapely.geometry import Polygon

# Set precision as defined in the competition
getcontext().prec = 25
SCALE_FACTOR = Decimal('1e18')

class ChristmasTree:
    """Represents a single, rotatable Christmas tree of a fixed size."""
    
    def __init__(self, center_x='0', center_y='0', angle='0'):
        self.center_x = Decimal(str(center_x))
        self.center_y = Decimal(str(center_y))
        self.angle = Decimal(str(angle))

        # Tree Dimensions
        trunk_w = Decimal('0.15')
        trunk_h = Decimal('0.2')
        base_w = Decimal('0.7')
        mid_w = Decimal('0.4')
        top_w = Decimal('0.25')
        tip_y = Decimal('0.8')
        tier_1_y = Decimal('0.5')
        tier_2_y = Decimal('0.25')
        base_y = Decimal('0.0')
        trunk_bottom_y = -trunk_h

        # Polygon Coordinates (Clockwise from tip)
        # Using the scale factor to maintain precision in shapely (which uses floats)
        coords = [
            (Decimal('0.0') * SCALE_FACTOR, tip_y * SCALE_FACTOR),                   # Tip
            (top_w / Decimal('2') * SCALE_FACTOR, tier_1_y * SCALE_FACTOR),          # R-Top
            (top_w / Decimal('4') * SCALE_FACTOR, tier_1_y * SCALE_FACTOR),
            (mid_w / Decimal('2') * SCALE_FACTOR, tier_2_y * SCALE_FACTOR),          # R-Mid
            (mid_w / Decimal('4') * SCALE_FACTOR, tier_2_y * SCALE_FACTOR),
            (base_w / Decimal('2') * SCALE_FACTOR, base_y * SCALE_FACTOR),           # R-Bot
            (trunk_w / Decimal('2') * SCALE_FACTOR, base_y * SCALE_FACTOR),          # R-Trunk
            (trunk_w / Decimal('2') * SCALE_FACTOR, trunk_bottom_y * SCALE_FACTOR),
            (-(trunk_w / Decimal('2')) * SCALE_FACTOR, trunk_bottom_y * SCALE_FACTOR), # L-Trunk
            (-(trunk_w / Decimal('2')) * SCALE_FACTOR, base_y * SCALE_FACTOR),
            (-(base_w / Decimal('2')) * SCALE_FACTOR, base_y * SCALE_FACTOR),          # L-Bot
            (-(mid_w / Decimal('4')) * SCALE_FACTOR, tier_2_y * SCALE_FACTOR),
            (-(mid_w / Decimal('2')) * SCALE_FACTOR, tier_2_y * SCALE_FACTOR),         # L-Mid
            (-(top_w / Decimal('4')) * SCALE_FACTOR, tier_1_y * SCALE_FACTOR),
            (-(top_w / Decimal('2')) * SCALE_FACTOR, tier_1_y * SCALE_FACTOR),         # L-Top
        ]
        
        # Convert Decimals to floats for Shapely
        float_coords = [(float(x), float(y)) for x, y in coords]
        initial_polygon = Polygon(float_coords)

        # Apply Rotation and Translation
        # Note: Shapely's affinity operations use floats. 
        # The scale factor helps mitigate precision loss during these operations.
        rotated = affinity.rotate(initial_polygon, float(self.angle), origin=(0, 0))
        self.polygon = affinity.translate(
            rotated, 
            xoff=float(self.center_x * SCALE_FACTOR), 
            yoff=float(self.center_y * SCALE_FACTOR)
        )

    def get_polygon(self):
        """Returns the shapely Polygon object."""
        return self.polygon

    def intersects(self, other_tree):
        """Checks if this tree intersects with another ChristmasTree object."""
        return self.polygon.intersects(other_tree.polygon)
