import math
import numpy as np
from decimal import Decimal
from shapely import affinity
from shapely.strtree import STRtree
from shapely.ops import unary_union

from src.models.tree_geometry import ChristmasTree

class HybridPhyllotaxisSolver:
    def __init__(self, core_ratio=0.7, c_factor=0.35):
        self.core_ratio = core_ratio
        self.c_factor = c_factor
        self.golden_angle = 137.5077

    def solve(self, num_trees):
        if num_trees == 0: return [], 0
        
        num_core = int(num_trees * self.core_ratio)
        if num_core == 0 and num_trees > 0: num_core = 1
        
        placed_trees = []

        # --- PHASE 1: CORE ---
        for n_idx in range(num_core):
            placed_polygons = [p.get_polygon() for p in placed_trees]
            tree_index = STRtree(placed_polygons) if placed_polygons else None
            tree = ChristmasTree()
            search_step = 0
            while search_step < 10000:
                theta = search_step * self.golden_angle
                r = self.c_factor * math.sqrt(search_step)
                rad_t = math.radians(theta)
                cx, cy = r * math.cos(rad_t), r * math.sin(rad_t)
                rotation = 180 if (n_idx % 2 == 0) else 0
                tree.center_x, tree.center_y, tree.angle = Decimal(str(cx)), Decimal(str(cy)), Decimal(str(rotation))
                tree._update_polygon()
                if not tree_index:
                    placed_trees.append(tree)
                    break
                poly = tree.get_polygon()
                possible = tree_index.query(poly)
                if not any(poly.intersects(placed_polygons[i]) and not poly.touches(placed_polygons[i]) for i in possible):
                    placed_trees.append(tree)
                    break
                search_step += 1

        # --- PHASE 2: CORNERS ---
        if len(placed_trees) < num_trees:
            all_poly = [p.get_polygon() for p in placed_trees]
            bounds = unary_union(all_poly).bounds
            minx, miny, maxx, maxy = bounds
            
            targets = [(minx, miny), (maxx, miny), (minx, maxy), (maxx, maxy)]
            tree_index = STRtree(all_poly)
            
            for n_idx in range(len(placed_trees), num_trees):
                placed = False
                for tx, ty in targets:
                    # Search around corner
                    for dist in np.arange(0.1, 10.0, 0.5):
                        for angle in range(0, 360, 45):
                            rad = math.radians(angle)
                            cx, cy = tx + dist * math.cos(rad), ty + dist * math.sin(rad)
                            tree = ChristmasTree(center_x=cx, center_y=cy, angle=0)
                            poly = tree.get_polygon()
                            possible = tree_index.query(poly)
                            if not any(poly.intersects(all_poly[i]) and not poly.touches(all_poly[i]) for i in possible):
                                placed_trees.append(tree)
                                all_poly.append(poly) # Update local list
                                tree_index = STRtree(all_poly) # Rebuild index
                                placed = True
                                break
                        if placed: break
                    if placed: break
                
                if not placed:
                    # Last resort: Place far right
                    tree = ChristmasTree(center_x=maxx + 5, center_y=0, angle=0)
                    placed_trees.append(tree)
                    all_poly.append(tree.get_polygon())
                    tree_index = STRtree(all_poly)

        all_polygons = [t.get_polygon() for t in placed_trees]
        final_bounds = unary_union(all_polygons).bounds
        side = max(final_bounds[2]-final_bounds[0], final_bounds[3]-final_bounds[1])
        return placed_trees, side
