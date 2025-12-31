import sys
from pathlib import Path
from decimal import Decimal

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree

def find_interlock():
    print("Searching for perfect Jigsaw interlock...")
    t_up = ChristmasTree(0, 0, 0)
    
    # Start inverted tree far away and slide it in
    best_dy = 2.0
    best_dx = 0.0
    
    # We want Tree B (inverted) to slot into the side of Tree A
    # Target your specific Jigsaw pattern (dx around 0.35)
    for dx in [x * 0.005 for x in range(60, 81)]: # 0.30 to 0.40
        dy = 1.5
        while dy > 0.4:
            t_down = ChristmasTree(dx, dy, 180)
            if t_up.intersects(t_down):
                # Found collision! The previous DY was safe.
                safe_dy = dy + 0.01
                # Calculate bounding box side length for this pair
                # ... (simplified check) ...
                if safe_dy < best_dy:
                    best_dy = safe_dy
                    best_dx = dx
                break
            dy -= 0.01
            
    print(f"Perfect Interlock Found: dx={best_dx:.3f}, dy={best_dy:.3f}")
    return best_dx, best_dy

if __name__ == "__main__":
    find_interlock()
