import math
from dataclasses import dataclass

@dataclass
class PackingTarget:
    n_trees: int
    ideal_side: float # Theoretical minimum based on area
    target_side: float # Achievable side using interlock grid
    rows: int
    cols: int

class TargetLibrary:
    """
    Library of target boxes for N trees.
    Calculates the 'Ideal Box' based on tree base dimensions (0.7 x 1.0)
    and nesting efficiency (approx 0.358 area per tree).
    """
    TREE_AREA = 0.7 # Bounding box area
    NESTED_AREA = 0.35855 # Area per tree in a perfect brick grid
    
    @staticmethod
    def get_target(n):
        # 1. Theoretical Minimum
        # Area = N * NESTED_AREA
        # Side = sqrt(Area)
        ideal = math.sqrt(n * TargetLibrary.NESTED_AREA)
        
        # 2. Achievable Grid (Bricks)
        # Using Brick = 0.71 x 1.01 (contains 2 trees)
        n_bricks = (n + 1) // 2
        
        best_side = float('inf')
        best_rows, best_cols = 1, n_bricks
        
        # We search for the rows/cols that minimize max(W, H)
        # Brick Width = 0.71, Brick Height = 1.205 (approx)
        B_W = 0.71
        B_H = 1.205
        
        for r in range(1, n_bricks + 1):
            c = math.ceil(n_bricks / r)
            # Span = (count - 1) * stride + unit_size
            # Simplified: count * stride (close enough for targeting)
            w = c * 0.71
            h = r * 1.01 # This is the brick center stride
            # A single brick is ~1.2 tall. 
            # R bricks stacked with 1.01 stride = (R-1)*1.01 + 1.2
            h_real = (r - 1) * 1.01 + 1.205
            
            side = max(w, h_real)
            if side < best_side:
                best_side = side
                best_rows, best_cols = r, c
                
        return PackingTarget(
            n_trees=n,
            ideal_side=ideal,
            target_side=best_side,
            rows=best_rows,
            cols=best_cols
        )

    @staticmethod
    def generate_report(max_n=200):
        print(f"{'N':<4} | {'Ideal':<8} | {'Target':<8} | {'Grid':<8} | {'Efficiency':<6}")
        print("-" * 50)
        for n in range(1, max_n + 1):
            t = TargetLibrary.get_target(n)
            eff = (t.ideal_side / t.target_side)**2
            print(f"{n:<4} | {t.ideal_side:<8.4f} | {t.target_side:<8.4f} | {t.cols}x{t.rows:<5} | {eff:.2f}")

if __name__ == "__main__":
    TargetLibrary.generate_report(20)