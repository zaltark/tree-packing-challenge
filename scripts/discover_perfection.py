import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree

def find_magic_numbers():
    print("Searching for the absolute tightest safe interlock...")
    t1 = ChristmasTree(0, 0, 0)
    
    # 1. Find safe interlock for Tree B (Down)
    # Target your pattern: dx ~ 0.35, dy ~ 0.8
    best_dy = 1.0
    for dy in np.arange(1.0, 0.5, -0.001):
        t2 = ChristmasTree(0.35, dy, 180)
        if t1.intersects(t2):
            best_dy = dy + 0.002 # Safe buffer
            break
    
    # 2. Find safe Horizontal Stride (sx)
    # How far to the next brick?
    best_sx = 1.0
    brick1 = [t1, ChristmasTree(0.35, best_dy, 180)]
    for sx in np.arange(1.0, 0.6, -0.001):
        t_next = ChristmasTree(sx, 0, 0)
        if any(t_next.intersects(b) for b in brick1):
            best_sx = sx + 0.002
            break
            
    # 3. Find safe Vertical Stride (sy)
    best_sy = 1.0
    for sy in np.arange(1.0, 0.6, -0.001):
        t_above = ChristmasTree(0, sy, 0)
        if any(t_above.intersects(b) for b in brick1):
            best_sy = sy + 0.002
            break

    print(f"MAGIC NUMBERS FOUND:")
    print(f"Jigsaw DX: 0.35")
    print(f"Jigsaw DY: {best_dy:.4f}")
    print(f"Stride X: {best_sx:.4f}")
    print(f"Stride Y: {best_sy:.4f}")
    
    return 0.35, best_dy, best_sx, best_sy

if __name__ == "__main__":
    find_magic_numbers()
