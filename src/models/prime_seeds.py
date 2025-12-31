import math
from src.models.tree_geometry import ChristmasTree

def get_prime_seed(n):
    """
    Optimized symmetric triangular/stack layouts for small primes.
    Focuses on 'Nested Jigsaw' patterns.
    """
    
    # Unit offsets for nesting
    DX = 0.355
    DY = 0.805
    STRIDE_X = 0.71
    
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
        
    if n == 7:
        # Hex-like Cluster (1 Center, 6 Surround)
        # OR Tighter Block 2-3-2?
        # Let's try 2-3-2 Staggered "Honeycomb" Block
        # Row 1 (y=DY): 2 Down
        # Row 2 (y=0): 3 Up
        # Row 3 (y=-DY): 2 Down
        
        # This is 3 rows tall ~ 2.4 height.
        # Width ~ 3*0.7 = 2.1 width.
        # Very square!
        
        trees = [
            # Middle Row (3 Up)
            ChristmasTree(0, 0, 0),
            ChristmasTree(STRIDE_X, 0, 0),
            ChristmasTree(-STRIDE_X, 0, 0),
            
            # Top Row (2 Down) - Nesting in the 2 gaps between 3 trees
            ChristmasTree(DX, DY, 180),
            ChristmasTree(-DX + STRIDE_X - STRIDE_X, DY, 180), # Wait.
            # Gaps are at +/- DX roughly?
            # 0 and 0.71. Gap center ~ 0.355.
            # 0 and -0.71. Gap center ~ -0.355.
            ChristmasTree(DX, DY, 180),
            ChristmasTree(-DX, DY, 180),
            
            # Bottom Row (2 Down) - Nesting below?
            # If Middle is Up, Bottom Down fits in gaps too?
            # Symmetry: 180 rotation of Top Row?
            # Top row y=+0.8. Bot row y=-0.8?
            # Trees at +/- 0.355, -0.8, 180?
            # Wait, Down tree at -0.8 points down to -1.6.
            # Up tree at 0 points up to 0.8. Base at 0.
            # Down tree at 0.8 points down to 0. Base at 0.8.
            # So Top Row (Down) interlocks with Middle (Up).
            
            # For Bottom Row, we want trees that interlock with Middle (Up) from *below*.
            # Middle Base is at 0.
            # Up tree (0, -0.8, 0)? Tip at 0.
            # Yes, Up trees at y ~ -0.8 would touch bases with Middle. Not interlock.
            # We want Down trees at y ~ -0.?
            # No, standard brick is Up-Down.
            # Row 1: Down (Base 0.8, Tip 0)
            # Row 2: Up (Base 0, Tip 0.8) -> Interlock!
            # Row 3: Down? (Base -0.8? Tip -1.6?) No.
            # We want Row 3 to be Up?
            
            # Let's try 2-3-2 where Top/Bot are Down, Middle Up?
            # Top (Down) Base 0.8. Tip 0. Matches Mid (Up) Tip 0.8.
            # Bot (Down) Base -0.8? Tip -1.6. Mid (Up) Base 0.
            # Gap.
            
            # Better: 2-3-2 where rows alternate Up-Down-Up
            # Top (Up): y=DY? Base 0.8. Tip 1.6.
            # Mid (Down): y=0? Base 0. Tip -0.8.
            # Bot (Up): y=-DY? Base -0.8. Tip 0.
            
            # Let's try:
            # Row 1 (Top, y=0.8): 2 Up
            # Row 2 (Mid, y=0): 3 Down
            # Row 3 (Bot, y=-0.8): 2 Up
            
            # Top (2 Up): x = +/- 0.355
            ChristmasTree(DX, DY, 0),
            ChristmasTree(-DX, DY, 0),
            
            # Mid (3 Down): x = 0, +/- 0.71
            ChristmasTree(0, 0, 180),
            ChristmasTree(STRIDE_X, 0, 180),
            ChristmasTree(-STRIDE_X, 0, 180),
            
            # Bot (2 Up): x = +/- 0.355
            ChristmasTree(DX, -DY, 0),
            ChristmasTree(-DX, -DY, 0)
        ]
        return trees
        
    # Fallback: Simple centered row of bricks
    trees = []
    n_slots = (n + 1) // 2
    for i in range(n_slots):
        bx = (i - (n_slots - 1) / 2.0) * STRIDE_X
        if len(trees) < n:
            trees.append(ChristmasTree(bx, 0, 0))
        if len(trees) < n:
            trees.append(ChristmasTree(bx + DX, DY, 180))
            
    return trees