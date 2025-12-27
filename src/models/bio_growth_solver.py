import math
import numpy as np
from decimal import Decimal
from shapely import affinity
from shapely.strtree import STRtree
from shapely.ops import unary_union

from src.models.tree_geometry import ChristmasTree

class BioGrowthSolver:
    def __init__(self, dna):
        self.dna = dna
        self.c_factor = dna.get('c_factor', 0.5)
        self.golden_angle = dna.get('golden_angle', 137.5077)
        self.square_factor = dna.get('square_factor', 1.0)
        self.rot_mode = dna.get('rot_mode', 'interlock')

    def get_spiral_pos(self, step):
        theta = step * self.golden_angle
        rad_theta = math.radians(theta)
        r = self.c_factor * math.sqrt(step)
        cos_t, sin_t = math.cos(rad_theta), math.sin(rad_theta)
        square_scale = 1.0 / max(abs(cos_t), abs(sin_t)) if step > 0 else 1.0
        actual_scale = 1.0 + (square_scale - 1.0) * self.square_factor
        return r * actual_scale * cos_t, r * actual_scale * sin_t, theta

    def solve(self, num_trees):
        placed_trees = []
        seed_data = self.dna.get('seed_data', [])
        for i in range(min(num_trees, len(seed_data))):
            x, y, a = seed_data[i]
            new_tree = ChristmasTree(center_x=x, center_y=y, angle=a)
            valid = True
            for p in placed_trees:
                if new_tree.intersects(p):
                    valid = False
                    break
            if valid: placed_trees.append(new_tree)

        for n_idx in range(len(placed_trees), num_trees):
            placed_polygons = [p.get_polygon() for p in placed_trees]
            tree_index = STRtree(placed_polygons)
            tree, search_step = ChristmasTree(), 1
            placed = False
            while search_step < 10000:
                cx, cy, _ = self.get_spiral_pos(search_step)
                if self.rot_mode == 'interlock': rotation = 180 if (n_idx % 2 == 0) else 0
                elif self.rot_mode == 'radial': rotation = math.degrees(math.atan2(-cy, -cx)) - 90
                else: rotation = 0
                tree.center_x, tree.center_y, tree.angle = Decimal(str(cx)), Decimal(str(cy)), Decimal(str(rotation))
                tree._update_polygon()
                poly = tree.get_polygon()
                possible = tree_index.query(poly)
                if not any(poly.intersects(placed_polygons[i]) and not poly.touches(placed_polygons[i]) for i in possible):
                    placed = True
                    break
                search_step += 1
            if placed: placed_trees.append(tree)

        return self._finalize(placed_trees, num_trees)

    def _finalize(self, trees, target_n):
        if not trees: return [], float('inf')
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
        penalty = (target_n - len(trees)) * 10
        return trees, side + penalty