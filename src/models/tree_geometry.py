import math
from decimal import Decimal, getcontext
from shapely import affinity
from shapely.geometry import Polygon
import shapely

# Import private competition params
try:
    from config.magic_params import TREE_COORDS, SCALE_FACTOR
except ImportError:
    # Default fallback if magic_params is missing (though it should be local)
    TREE_COORDS = []
    SCALE_FACTOR = Decimal('1e18')

getcontext().prec = 25

class ChristmasTree:
    """Represents a single, rotatable Christmas tree of a fixed size."""
    
    def __init__(self, center_x='0', center_y='0', angle='0'):
        self.center_x = Decimal(str(center_x))
        self.center_y = Decimal(str(center_y))
        self.angle = Decimal(str(angle))
        
        # Initialize polygon using official coordinates
        self.initial_polygon = Polygon(TREE_COORDS)
        self._update_polygon()

    def _update_polygon(self):
        """Recalculates the shapely polygon using optimized affinity transforms."""
        # Note: We perform operations in standard units. 
        # Metric applies SCALE_FACTOR to final points.
        rotated = affinity.rotate(self.initial_polygon, float(self.angle), origin=(0, 0))
        
        # Ensure validity
        if not rotated.is_valid:
            rotated = rotated.buffer(0)
            
        self.polygon = affinity.translate(
            rotated, 
            xoff=float(self.center_x), 
            yoff=float(self.center_y)
        )

    def get_polygon(self):
        """Returns the current shapely polygon."""
        return self.polygon

    def intersects(self, other_tree):
        """Checks if this tree intersects with another ChristmasTree object."""
        # Rules: Overlapping (sharing interior) is forbidden. Touching is allowed.
        return self.polygon.intersects(other_tree.polygon) and not self.polygon.touches(other_tree.polygon)