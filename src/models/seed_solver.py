import math
from src.models.tree_geometry import ChristmasTree, SAFE_TOUCH_BUFFER

def get_seed_layout(n):
    """
    Optimized symmetric triangular/stack layouts for small N.
    Focuses on 'Nested Jigsaw' patterns.
    """
    
    # Unit offsets for nesting (Synchronized with SAFE_TOUCH_BUFFER)
    DX = 0.35 + SAFE_TOUCH_BUFFER
    DY = 0.80 + SAFE_TOUCH_BUFFER
    STRIDE_X = 0.70 + (2 * SAFE_TOUCH_BUFFER)
    
    if n == 1:
        return [ChristmasTree(0, 0, 0)]
        
    if n == 2:
        return [
            ChristmasTree(-DX/2, 0, 0),
            ChristmasTree(DX/2, DY, 180)
        ]
        
    if n == 3:
        # Perfect Symmetric Trio (Triangle pointing up)
        return [
            ChristmasTree(0, 0, 0),
            ChristmasTree(DX, DY, 180),
            ChristmasTree(-DX, DY, 180)
        ]
        
    if n == 5:
        # Cross / Diamond (1-3-1) - More square-like than 3-2 stack
        # Top Row (1 down)
        # Mid Row (3 up)
        # Bot Row (1 down)
        # Note: 180 deg trees are "down" (tip down? No, 180 deg tip points DOWN).
        # Normal (0) tip points UP (y=0.8). Base at y=0.
        # 180: Tip at y=-0.8 (relative). Base at y=0.
        
        # Center row (y=0): 3 Up trees. (-0.71, 0, 0.71)
        # Top row (y=0.8): 1 Down tree. Nesting in gaps?
        # Bot row (y=-0.8): 1 Down tree.
        
        return [
            ChristmasTree(0, 0, 0),             # Center
            ChristmasTree(STRIDE_X, 0, 0),      # Right
            ChristmasTree(-STRIDE_X, 0, 0),     # Left
            ChristmasTree(DX, DY, 180),         # Top-Right Gap
            ChristmasTree(-DX, -DY, 0)          # Bot-Left Gap? No, symmetric.
            # Let's try explicit 1-3-1
        ]
        # Reverting to 2-row block for N=5 because 1-3-1 is very tall (3 rows).
        # Best N=5 is likely 3-2 or 2-3 block.
        # Try a tighter 2-3 block (2 Up, 3 Down)
        return [
             ChristmasTree(-DX, DY, 180),
             ChristmasTree(0, DY, 180),
             ChristmasTree(DX, DY, 180),
             ChristmasTree(-STRIDE_X/2, 0, 0),
             ChristmasTree(STRIDE_X/2, 0, 0)
        ]
        
        # N=7 layout disabled due to cluster collisions with new precision.
        
        # BrickTiler is preferred.
        
        
        
        return None
        
    