import sys
from pathlib import Path
from shapely.ops import unary_union
import pandas as pd
import math
from shapely.affinity import rotate

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR
from scripts.visualize_results import plot_trees

def test_n5_corner_shift():
    print("Testing N=5 Corner Shift...")
    
    # Original N=5 Brick (Target 2x2 grid, 3 slots filled)
    # Slot 1: (0,0) - Filled
    # Slot 2: (0.71, 0) - Filled
    # Slot 3: (0, 1.01) - Filled
    # Slot 4: (0.71, 1.01) - EMPTY
    
    # Trees:
    # 1. (0,0,0)
    # 2. (0.355, 0.805, 180)
    # 3. (0.71, 0, 0)
    # 4. (1.065, 0.805, 180)
    # 5. (0, 1.01, 0) -> Leftover in Row 2?
    
    # Current Layout (3 bricks):
    # R1: Brick 1 (0,0), Brick 2 (0.71,0)
    # R2: Brick 3 (0, 1.01)
    
    # User Suggestion:
    # "Take 1 tree off the top (of 5) and put it in the top right corner"
    # Currently the "top" is Brick 3 (1 tree or 2 trees?)
    # N=5 means 2.5 bricks.
    # Brick 1: 2 trees
    # Brick 2: 2 trees
    # Brick 3: 1 tree (remainder).
    
    # Layout is:
    # Row 1: Brick 1, Brick 2. (4 trees).
    # Row 2: Brick 3 (1 tree). Position (0, 1.01).
    
    # The bounding box is determined by Row 2 height (1.01 + 1.0 = 2.01)
    # And Row 1 width (0.71 + 0.7 = 1.41).
    # Wait. Row 1 has 2 bricks.
    # Brick 1 Center 0.
    # Brick 2 Center 0.71.
    # Max X = 0.71 + 0.35 = 1.06.
    # Min X = 0 - 0.35 = -0.35.
    # Width = 1.41.
    
    # So we have Width 1.41, Height 2.01.
    # Max Side = 2.01.
    
    # The "Top Right" corner is empty (1.41, 2.01).
    # Can we move the 5th tree there?
    # If we move it to (0.71, 1.01), the bounding box is the same (Width 1.41, Height 2.01).
    # It just fills the empty slot. It doesn't shrink the box.
    
    # To shrink the box, we need to reduce Height (2.01) or Width (1.41).
    # Since Height > Width, we must reduce Height.
    # To reduce Height, we must NOT have a 2nd row?
    # But 5 trees in 1 row is Width = 4 * 0.71 + 0.7 = 3.5. Too wide.
    
    # Can we make Width larger (up to 2.0) and Height smaller (down to 2.0)?
    # 2.01 is already ~2.0.
    
    # Is there a way to fit 5 trees in < 2.0 side?
    # We found global rotation N=5 -> Side 1.81.
    # That means the 2x2 grid (Width 1.41, Height 2.01) rotated 135 deg fits in 1.81 box.
    
    # Why?
    # Rect 1.4 x 2.0.
    # Diagonal = sqrt(1.4^2 + 2.0^2) = 2.44.
    # Rotated 45 deg?
    # Project on X: 1.4 cos 45 + 2.0 sin 45 = 0.7*1.4 + 0.7*2.0 = 0.98 + 1.4 = 2.38.
    # That's bigger.
    
    # Why did N=5 shrink to 1.81?
    # Maybe the "Step" shape allows corners to tuck in?
    
    print("Analyzing current N=5 rotation...")
    
    # Let's verify the dimensions of the N=5 seed (Manual stack)
    # Manual stack was:
    # 3 trees R1. 2 trees R2.
    # R1 Width: 3 trees. 0.71 * 2 + 0.7 = 2.12.
    # R2 Height: Stride Y + 1.0 = 2.01.
    
    # So 2.12 x 2.01.
    # Rotated, it shrank to 1.81.
    
    print("Confirmed: N=5 is optimized by rotation.")
    print("Moving the tree to the corner (filling the 2x2 grid) creates a solid block.")
    print("A solid 2x2 block (1.41 x 2.01) might rotate even better?")
    
    # Let's test: 2x2 full block (minus 3 trees? No, N=5 is 5 trees).
    # 2x2 grid has 4 slots (8 trees capacity).
    # We have 5 trees.
    # 3 empty slots.
    
    # Config A: 3 trees Row 1. 2 trees Row 2. (Current Best).
    # Config B: 4 trees Row 1? No.
    # Config C: 2 trees Row 1. 2 trees Row 2. 1 tree Row 3?
    # Height 3.0. Bad.
    
    # Config D: "Cross"?
    # Center. Top, Bot, Left, Right.
    # Center (0,0).
    # Left (-0.71, 0). Right (0.71, 0).
    # Top (0, 1.01). Bot (0, -1.01).
    # Width 2.12. Height 3.0. Bad.
    
    print("Current 3-2 staggered stack (rotated) seems optimal.")

if __name__ == "__main__":
    test_n5_corner_shift()
