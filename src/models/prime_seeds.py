import math
from src.models.tree_geometry import ChristmasTree

def generate_radial_monolith(n, radius_step=0.68):
    """
    Forces trees into dense Star/Monolith patterns using Magic Layouts.
    Uses ring offsets and interlocking rotations (Outward/Inward) 
    to fit reversed trees into the gaps.
    """
    trees = []
    
    # THE MAGIC CONFIGURATIONS (from User)
    custom_layouts = {
        2: [2],
        3: [3],             # Triangle
        5: [5],             # Pentagon
        6: [1, 5],          # Pentagon + Center
        7: [1, 6],          # Hexagon + Center
        11: [1, 5, 5],      # Dense 2-Ring Pent
        13: [1, 6, 6],      # Dense 2-Ring Hex
        17: [1, 6, 10],     # The Snowflake
        19: [1, 6, 12],     # Perfect Hexagon
        23: [1, 7, 15],     # Heptagonish
        29: [1, 8, 20],     # Large Monolith
    }
    
    layout = custom_layouts.get(n, [1, n-1]) 
    current_count = 0
    
    for ring_idx, count in enumerate(layout):
        if count == 0: continue
        
        # Ring 0: Center
        if ring_idx == 0 and count == 1:
            trees.append(ChristmasTree(0, 0, 0))
            current_count += 1
            continue
            
        # Radius: Ring 1 is 1*step, Ring 2 is 2*step
        r = ring_idx * radius_step if layout[0] == 1 else (ring_idx + 1) * radius_step
        angle_step = 360.0 / count
        
        # Offset every other ring by half a step to mesh like gears
        angle_offset = (angle_step / 2) if (ring_idx % 2 == 1) else 0
        
        for i in range(count):
            if current_count >= n: break
            
            theta = (i * angle_step) + angle_offset
            theta_rad = math.radians(theta)
            
            x = r * math.cos(theta_rad)
            y = r * math.sin(theta_rad)
            
            # INTERLOCKING ROTATION:
            # Pointing outward (theta-90) is the base.
            # We alternate rotations for trees in the same ring to fit reversed shapes.
            if i % 2 == 1:
                rot = (theta - 90 + 180) % 360 # Reversed (Inward)
            else:
                rot = theta - 90 # Outward
            
            trees.append(ChristmasTree(x, y, rot))
            current_count += 1
            
    return trees

def generate_hex_monolith(n):
    """
    Dense Triangular Lattice (Hexagonal Packing).
    Denser than square grids, creates organic monolith shapes.
    """
    trees = []
    # Stride for hexagonal packing
    DX = 0.36
    DY = 0.75
    
    # We grow in "hexagonal rings" to keep it a monolith
    q_max = math.ceil(math.sqrt(n))
    for q in range(-q_max, q_max + 1):
        for r in range(-q_max, q_max + 1):
            if len(trees) >= n: break
            
            # Axial to Cartesian conversion for hex grid
            x = DX * (1.5 * q)
            y = DY * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
            
            # Alternate rotation for the Jigsaw fit
            rot = 180 if (q + r) % 2 == 1 else 0
            
            trees.append(ChristmasTree(x, y, rot))
            
    return trees

def get_prime_seed(n):
    """
    Returns the high-density Monolith for Prime N.
    """
    # Use Radial Monoliths for small N (up to 30)
    if n <= 30:
        return generate_radial_monolith(n, radius_step=0.65)
    
    # Fallback for larger N: Hexagonal Monolith
    return generate_hex_monolith(n)
