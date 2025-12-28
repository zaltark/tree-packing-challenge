import math
from src.models.tree_geometry import ChristmasTree
from src.models.prime_seeds import generate_radial_monolith, generate_hex_monolith
from shapely.ops import unary_union

class PrimeSolver:
    """
    Expert B: The Prime Solver (Monolith Factory).
    Generates high-density radial and hexagonal monoliths.
    Tries multiple tight mathematical configurations to find the best fit.
    """

    def __init__(self, iterations=0):
        self.iterations = iterations

    def solve(self, n_trees, seed_trees=None):
        if n_trees == 0: return [], 0
        
        best_trees = []
        best_side = float('inf')
        
        # 1. Search Strategy: Try different tight radii for the Monolith
        # From very tight (0.5) to safe (0.8)
        if n_trees <= 30:
            radii = [0.55, 0.6, 0.65, 0.68, 0.72, 0.75, 0.8]
            for r in radii:
                candidate = generate_radial_monolith(n_trees, radius_step=r)
                if not self._has_overlap(candidate):
                    side = self._get_side(candidate)
                    if side < best_side:
                        best_side = side
                        best_trees = candidate
        else:
            # For larger N, use Hex Monolith
            candidate = generate_hex_monolith(n_trees)
            if not self._has_overlap(candidate):
                best_trees = candidate
                best_side = self._get_side(candidate)

        if not best_trees:
            # Final emergency fallback: force-space them
            best_trees = generate_radial_monolith(n_trees, radius_step=1.0)
            best_side = self._get_side(best_trees)

        return best_trees, best_side

    def _has_overlap(self, trees):
        for i in range(len(trees)):
            for j in range(i+1, len(trees)):
                if trees[i].intersects(trees[j]):
                    return True
        return False

    def _get_side(self, trees):
        all_polygons = [t.get_polygon() for t in trees]
        bounds = unary_union(all_polygons).bounds
        return max(bounds[2]-bounds[0], bounds[3]-bounds[1])
