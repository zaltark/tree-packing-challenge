from decimal import Decimal, getcontext
from shapely import affinity
from shapely.geometry import Polygon

from config.magic_params import TREE_COORDS

getcontext().prec = 25
SCALE_FACTOR = Decimal('1e18')

class ChristmasTree:
    def __init__(self, center_x='0', center_y='0', angle='0'):
        self.center_x = Decimal(str(center_x))
        self.center_y = Decimal(str(center_y))
        self.angle = Decimal(str(angle))
        
        self.initial_polygon = Polygon(TREE_COORDS)
        self._update_polygon()

    def _update_polygon(self):
        rotated = affinity.rotate(self.initial_polygon, float(self.angle), origin=(0, 0))
        self.polygon = affinity.translate(rotated, xoff=float(self.center_x), yoff=float(self.center_y))

    def get_polygon(self):
        return self.polygon

    def intersects(self, other_tree):
        return self.polygon.intersects(other_tree.polygon) and not self.polygon.touches(other_tree.polygon)