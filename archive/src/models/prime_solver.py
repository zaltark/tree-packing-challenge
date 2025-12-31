import math
from src.models.tree_geometry import ChristmasTree
from src.models.prime_seeds import generate_from_library, generate_hex_monolith, PRIME_LIBRARY
from shapely.ops import unary_union

class PrimeSolver:
    """
    Expert B: The Prime Solver (Monolith Factory).
    Uses the Prime Library for optimized small-N configurations.
    """

    def __init__(self, iterations=0):
        self.iterations = iterations

    def solve(self, n_trees, seed_trees=None):
        if n_trees == 0: return [], 0
        
        best_trees = []
        best_side = float('inf')
        
        # 1. Try the tuned Library configuration first
        candidate = generate_from_library(n_trees)
        if not self._has_overlap(candidate):
            best_trees = candidate
            best_side = self._get_side(candidate)
            
        # 2. If it's a small N, search around the library radius to squeeze it
        if n_trees <= 30:
            # Radius search: library step +/- 0.1
            lib_step = 0.65
            if n_trees in PRIME_LIBRARY:
                lib_step = PRIME_LIBRARY[n_trees]['radius_step']
            
            for r in [lib_step - 0.05, lib_step - 0.02, lib_step + 0.02, lib_step + 0.05]:
                # Temporary hack to try different radii while keeping library structure
                # We reuse the logic but with custom radius
                candidate = self._generate_custom_radial(n_trees, r)
                if candidate and not self._has_overlap(candidate):
                    side = self._get_side(candidate)
                    if side < best_side:
                        best_side = side
                        best_trees = candidate

        # 3. Fallback to Hex Monolith if no valid library/radial fit found
        if not best_trees:
            candidate = generate_hex_monolith(n_trees)
            if not self._has_overlap(candidate):
                best_trees = candidate
                best_side = self._get_side(candidate)

        return best_trees, best_side

    def _generate_custom_radial(self, n, step):
        """Helper to test variations of the library layouts."""
        if n not in PRIME_LIBRARY: return None
        
        config = PRIME_LIBRARY[n]
        # Same logic as library but with custom step
        trees = []
        layout = config['layout']
        rot_mode = config['rot_mode']
        current_count = 0
        for ring_idx, count in enumerate(layout):
            r = ring_idx * step if layout[0] == 1 else (ring_idx + 1) * step
            angle_step = 360.0 / count
            angle_offset = (angle_step / 2) if (ring_idx % 2 == 1) else 0
            for i in range(count):
                if current_count >= n: break
                theta = (i * angle_step) + angle_offset
                theta_rad = math.radians(theta)
                x, y = r * math.cos(theta_rad), r * math.sin(theta_rad)
                rot = (theta - 90 + 180) % 360 if (rot_mode == 'interlock' and i % 2 == 1) else (theta - 90)
                trees.append(ChristmasTree(x, y, rot))
                current_count += 1
        return trees

    def _has_overlap(self, trees):
        if not trees: return True
        for i in range(len(trees)):
            for j in range(i+1, len(trees)):
                if trees[i].intersects(trees[j]):
                    return True
        return False

    def _get_side(self, trees):
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        return max(bounds[2]-bounds[0], bounds[3]-bounds[1])