import math
import numpy as np
from decimal import Decimal
from shapely import affinity
from shapely.strtree import STRtree
from shapely.ops import unary_union

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

class PhyllotaxisSolver:
    """
    Biologically inspired solver using Fermat's Spiral with Interlocking Seeds.
    """

    def __init__(self, c_factor=0.5, use_interlocking=True):
        self.GOLDEN_ANGLE = 137.50776405
        self.c_factor = c_factor
        self.use_interlocking = use_interlocking

    def _get_dense_seed(self):
        """Creates a tightly packed core of 4 interlocked trees."""
        seed = [
            ChristmasTree(center_x='0.2', center_y='0.2', angle='0'),
            ChristmasTree(center_x='-0.2', center_y='-0.2', angle='180'),
            ChristmasTree(center_x='-0.2', center_y='0.2', angle='0'),
            ChristmasTree(center_x='0.2', center_y='-0.2', angle='180')
        ]
        return seed

    def solve_next(self, num_trees, existing_trees=None):
        if num_trees == 0: return [], Decimal('0')

        if existing_trees is None:
            # START WITH DENSE SEED
            placed_trees = self._get_dense_seed()
            # If user only wanted N < 4, truncate
            placed_trees = placed_trees[:num_trees]
        else:
            placed_trees = list(existing_trees)

        num_to_add = num_trees - len(placed_trees)

        if num_to_add > 0:
            for n_idx in range(len(placed_trees), num_trees):
                placed_polygons = [p.get_polygon() for p in placed_trees]
                tree_index = STRtree(placed_polygons)
                
                tree_to_place = ChristmasTree()
                
                search_step = 0
                placed = False
                while search_step < 15000:
                    theta = search_step * self.GOLDEN_ANGLE
                    radius = self.c_factor * math.sqrt(search_step)
                    rad_theta = math.radians(theta)
                    cx = radius * math.cos(rad_theta)
                    cy = radius * math.sin(rad_theta)
                    
                    # INTERLOCKING LOGIC
                    # Alternate rotation to slot triangles together
                    if self.use_interlocking:
                        rotation = 180 if (n_idx % 2 == 0) else 0
                    else:
                        angle_to_center = math.degrees(math.atan2(-cy, -cx))
                        rotation = angle_to_center - 90
                    
                    tree_to_place.center_x = Decimal(str(cx))
                    tree_to_place.center_y = Decimal(str(cy))
                    tree_to_place.angle = Decimal(str(rotation))
                    tree_to_place._update_polygon()
                    
                    candidate_poly = tree_to_place.get_polygon()
                    possible_indices = tree_index.query(candidate_poly)
                    
                    if not any(candidate_poly.intersects(placed_polygons[i]) and \
                               not candidate_poly.touches(placed_polygons[i]) \
                               for i in possible_indices):
                        placed = True
                        break
                    search_step += 1

                if placed:
                    placed_trees.append(tree_to_place)
                else:
                    # Emergency placement
                    tree_to_place.center_x = Decimal('100')
                    tree_to_place._update_polygon()
                    placed_trees.append(tree_to_place)

        # Calculate Score
        all_polygons = [t.get_polygon() for t in placed_trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1]) / float(SCALE_FACTOR)
        return placed_trees, side