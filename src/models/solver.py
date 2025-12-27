import numpy as np
import random
from decimal import Decimal
from src.models.tree_geometry import ChristmasTree
from src.models.engine import PackingEngine

class SlideInSolver:
    """
    Baseline solver that uses a 'slide-in' mechanic and weighted angles
    to pack trees greedily.
    """
    def __init__(self, engine=None):
        self.engine = engine if engine else PackingEngine()

    def generate_weighted_angle(self):
        """
        Biases angles toward 0, 90, 180, 270 degrees for tighter packing.
        Based on the heuristic: abs(sin(2*angle))
        """
        # For baseline, we can just return one of the cardinal directions 
        # or use the notebook's probability distribution.
        # Simplified: Pick from [0, 90, 180, 270] or a random angle.
        if random.random() < 0.8:
            return random.choice([0, 90, 180, 270])
        return random.uniform(0, 360)

    def solve(self, num_trees=100, max_attempts=500):
        """
        Attempts to pack num_trees using a simplified slide-in approach.
        """
        print(f"Starting solver to pack {num_trees} trees...")
        
        for i in range(num_trees):
            angle = self.generate_weighted_angle()
            placed = False
            
            # Try different start positions or random placements
            for attempt in range(max_attempts):
                # Random candidate position (initially naive random placement)
                # In a real slide-in, we'd start at the edge and decrement/increment.
                x = random.uniform(-10, 10)
                y = random.uniform(-10, 10)
                
                new_tree = ChristmasTree(center_x=x, center_y=y, angle=angle)
                
                if self.engine.is_valid_placement(new_tree):
                    self.engine.add_tree(new_tree)
                    placed = True
                    if (i + 1) % 10 == 0:
                        print(f"Placed {i+1} trees...")
                    break
            
            if not placed:
                print(f"Warning: Could not place tree {i+1} after {max_attempts} attempts.")
                break
                
        print(f"Finished. Total trees placed: {len(self.engine.placed_trees)}")
        print(f"Current Score: {self.engine.calculate_score():.6f}")
        return self.engine.get_placements_df()

if __name__ == "__main__":
    # Quick local test
    solver = SlideInSolver()
    placements = solver.solve(num_trees=20)
    print(placements.head())
