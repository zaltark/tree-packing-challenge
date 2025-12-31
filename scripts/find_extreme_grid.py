import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shapely.affinity import translate
from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

def find_extreme_grid():
    dx = 0.45
    dy = 0.25
    
    t1 = ChristmasTree(0, 0, 0)
    t2 = ChristmasTree(dx, dy, 180)
    
    # Unit = Brick (T1, T2)
    
    print(f"Finding Grid Stride for dx={dx}, dy={dy}...")
    
    # 1. Stride X (sx)
    # Brick 2 at (sx, 0)
    # Check T3(sx, 0) vs Brick 1
    # Check T4(sx+dx, dy) vs Brick 1
    
    sx = 0.7 # Minimum width
    while True:
        t3 = ChristmasTree(sx, 0, 0)
        t4 = ChristmasTree(sx + dx, dy, 180)
        
        if not (t3.intersects(t1) or t3.intersects(t2) or t4.intersects(t1) or t4.intersects(t2)):
            break
        sx += 0.001
        
    print(f"sx = {sx:.4f}")
    
    # 2. Stride Y (sy)
    # Brick 3 at (0, sy)
    # Check T5(0, sy) vs Brick 1
    # Check T6(dx, sy+dy) vs Brick 1
    
    sy = 0.5 # Try small
    while True:
        t5 = ChristmasTree(0, sy, 0)
        t6 = ChristmasTree(dx, sy + dy, 180)
        
        if not (t5.intersects(t1) or t5.intersects(t2) or t6.intersects(t1) or t6.intersects(t2)):
            break
        sy += 0.001
        
    print(f"sy = {sy:.4f}")
    
    area_per_tree = (sx * sy) / 2.0
    print(f"Area/Tree: {area_per_tree:.6f}")
    print(f"Current Best Submission Eff: 0.35855")

if __name__ == "__main__":
    find_extreme_grid()
