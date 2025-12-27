import math
import random
from decimal import Decimal
import numpy as np
from shapely import affinity
from shapely.strtree import STRtree
from shapely.ops import unary_union

from src.models.tree_geometry import ChristmasTree

class SlideInSolver:
    def __init__(self):
        pass

    def generate_weighted_angle(self):
        while True:
            angle = random.uniform(0, 360)
            rad = math.radians(angle)
            if random.uniform(0, 1) < abs(math.sin(2 * rad)):
                return angle

    def solve_next(self, num_trees, existing_trees=None):
        if num_trees == 0: return [], Decimal('0')
        placed_trees = list(existing_trees) if existing_trees else []
        num_to_add = num_trees - len(placed_trees)

        if num_to_add > 0:
            unplaced_trees = [ChristmasTree(angle=0) for _ in range(num_to_add)]
            if not placed_trees: 
                first = unplaced_trees.pop(0)
                first.angle = Decimal(str(random.uniform(0, 360)))
                first._update_polygon() 
                placed_trees.append(first)

            for tree_to_place in unplaced_trees:
                placed_polygons = [p.get_polygon() for p in placed_trees]
                tree_index = STRtree(placed_polygons)
                best_px, best_py, best_angle = 0, 0, 0
                min_radius = Decimal('Infinity')

                for _ in range(10):
                    angle = self.generate_weighted_angle()
                    rad_angle = math.radians(angle)
                    vx, vy = Decimal(str(math.cos(rad_angle))), Decimal(str(math.sin(rad_angle)))
                    radius, step_in = Decimal('20.0'), Decimal('0.5')
                    tree_to_place.angle = Decimal(str(angle))
                    tree_to_place._update_polygon() 
                    current_poly = tree_to_place.get_polygon() 

                    collision_found = False
                    while radius >= 0:
                        px, py = radius * vx, radius * vy
                        candidate_poly = affinity.translate(current_poly, xoff=float(px), yoff=float(py))
                        possible_indices = tree_index.query(candidate_poly)
                        if any(candidate_poly.intersects(placed_polygons[i]) and not candidate_poly.touches(placed_polygons[i]) for i in possible_indices):
                            collision_found = True
                            break
                        radius -= step_in

                    if collision_found:
                        step_out = Decimal('0.05')
                        while True:
                            radius += step_out
                            px, py = radius * vx, radius * vy
                            candidate_poly = affinity.translate(current_poly, xoff=float(px), yoff=float(py))
                            possible_indices = tree_index.query(candidate_poly)
                            if not any(candidate_poly.intersects(placed_polygons[i]) and not candidate_poly.touches(placed_polygons[i]) for i in possible_indices):
                                break
                    else:
                        radius, px, py = Decimal('0'), Decimal('0'), Decimal('0')

                    if radius < min_radius:
                        min_radius, best_px, best_py, best_angle = radius, px, py, angle

                tree_to_place.center_x, tree_to_place.center_y, tree_to_place.angle = best_px, best_py, Decimal(str(best_angle))
                tree_to_place._update_polygon()
                placed_trees.append(tree_to_place)

        all_polygons = [t.get_polygon() for t in placed_trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        return placed_trees, Decimal(str(side))
