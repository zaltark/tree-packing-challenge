import numpy as np
from shapely.strtree import STRtree
from decimal import Decimal
from src.models.tree_geometry import SCALE_FACTOR

class PackingEngine:
    """Handles collision detection and scoring for tree packing."""
    
    def __init__(self):
        self.placed_trees = [] # List of ChristmasTree objects
        self.spatial_index = None

    def _update_spatial_index(self):
        """Rebuilds the STRtree index from placed trees."""
        if not self.placed_trees:
            self.spatial_index = None
            return
        
        polygons = [t.get_polygon() for t in self.placed_trees]
        self.spatial_index = STRtree(polygons)

    def is_valid_placement(self, new_tree):
        """
        Checks if a new tree can be placed without overlapping existing ones.
        Uses STRtree for efficient spatial queries.
        """
        if not self.placed_trees:
            return True
        
        new_poly = new_tree.get_polygon()
        
        # If we have many trees, use the spatial index
        if self.spatial_index:
            # query returns indices of geometries whose bounding box intersects new_poly's bounding box
            potential_indices = self.spatial_index.query(new_poly)
            for idx in potential_indices:
                if self.placed_trees[idx].get_polygon().intersects(new_poly):
                    return False
        else:
            # Fallback for very few trees or if index isn't built
            for tree in self.placed_trees:
                if tree.intersects(new_tree):
                    return False
        
        return True

    def add_tree(self, tree):
        """Adds a tree to the list and refreshes the spatial index."""
        self.placed_trees.append(tree)
        self._update_spatial_index()

    def calculate_score(self):
        """Calculates (SideLength^2) / N using the official scaled metric."""
        if not self.placed_trees:
            return 0.0
        
        n = len(self.placed_trees)
        
        # Find the bounding square
        min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
        
        for tree in self.placed_trees:
            bounds = tree.get_polygon().bounds # (minx, miny, maxx, maxy)
            min_x = min(min_x, bounds[0])
            min_y = min(min_y, bounds[1])
            max_x = max(max_x, bounds[2])
            max_y = max(max_y, bounds[3])
            
        # The coordinates in the objects are scaled by 1e18.
        width = (max_x - min_x)
        height = (max_y - min_y)
        
        side_length_scaled = max(width, height)
        
        # Official Formula: (SideLengthScaled^2) / (ScaleFactor^2) / N
        # We perform calculation using Decimal for precision if possible, or float if speed is needed.
        # But here we are using floats from bounds.
        # For precision, we should ideally use Decimals, but bounds returns floats.
        # The discrepancy is acceptable for engine estimation, but final score check should use metric.py
        
        score = (Decimal(side_length_scaled) ** 2) / (SCALE_FACTOR ** 2) / Decimal(n)
        return float(score)

    def get_placements_df(self):
        """Returns the placements in a format suitable for submission/visualization."""
        import pandas as pd
        data = []
        for i, tree in enumerate(self.placed_trees):
            data.append({
                'id': i,
                'x': tree.center_x,
                'y': tree.center_y,
                'angle': tree.angle
            })
        return pd.DataFrame(data)
