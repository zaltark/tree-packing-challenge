import sys
from pathlib import Path
import pandas as pd
import math
import matplotlib.pyplot as plt
from shapely.affinity import rotate
from shapely.ops import unary_union
from shapely.strtree import STRtree

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.brick_tiler_solver import BrickTilerSolver
from src.models.seed_solver import get_seed_layout
from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR
from scripts.visualize_results import plot_trees

def optimize_rotation_for_trees(trees):
    """
    Rotates the entire cluster of trees to minimize the bounding square side.
    """
    if not trees: return trees
    
    all_polys = [t.get_polygon() for t in trees]
    union_poly = unary_union(all_polys)
    scaled_centroid = union_poly.centroid
    scx, scy = scaled_centroid.x, scaled_centroid.y
    
    initial_bounds = union_poly.bounds
    best_side = max(initial_bounds[2]-initial_bounds[0], initial_bounds[3]-initial_bounds[1])
    best_angle = 0
    
    for angle in range(0, 180, 1):
        rot_poly = rotate(union_poly, angle, origin=(scx, scy))
        b = rot_poly.bounds
        side = max(b[2]-b[0], b[3]-b[1])
        if side < best_side:
            best_side = side
            best_angle = angle
            
    if best_angle != 0:
        ucx = float(scx) / float(SCALE_FACTOR)
        ucy = float(scy) / float(SCALE_FACTOR)
        
        new_trees = []
        rad = math.radians(best_angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        
        for t in trees:
            new_angle = t.angle + best_angle
            dx = float(t.center_x) - ucx
            dy = float(t.center_y) - ucy
            new_x = ucx + dx * cos_a - dy * sin_a
            new_y = ucy + dx * sin_a + dy * cos_a
            new_trees.append(ChristmasTree(new_x, new_y, new_angle))
        return new_trees
    return trees

def check_overlap_and_plot(n, trees):
    """
    Checks for overlap among trees. If found, plots the full config 
    and a zoomed-in view of the overlap.
    """
    polygons = [t.get_polygon() for t in trees]
    r_tree = STRtree(polygons)
    
    overlaps = []
    
    for i, poly in enumerate(polygons):
        indices = r_tree.query(poly)
        for index in indices:
            if index == i:
                continue
            # Store lower index first to avoid duplicates
            pair = tuple(sorted((i, index)))
            if pair in overlaps:
                continue
                
            if poly.intersects(polygons[index]) and not poly.touches(polygons[index]):
                intersection = poly.intersection(polygons[index])
                # Filter out microscopic float errors (optional, but good for sanity)
                if intersection.area > 1e-12:
                    overlaps.append(pair)
                    t1, t2 = trees[i], trees[index]
                    print(f"OVERLAP DETECTED for N={n}: Tree {i} intersects Tree {index} (Area: {intersection.area})")
                    print(f"  Tree {i}: ({t1.center_x}, {t1.center_y}, {t1.angle})")
                    print(f"  Tree {index}: ({t2.center_x}, {t2.center_y}, {t2.angle})")

    if overlaps:
        output_dir = PROJECT_ROOT / "results" / "debug_failures"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Plot Full Configuration
        df = pd.DataFrame([{'x': t.center_x, 'y': t.center_y, 'angle': t.angle} for t in trees])
        plot_trees(df, output_path=output_dir / f"fail_full_N{n}.png")
        
        # 2. Plot Zoomed-in Overlaps
        for idx1, idx2 in overlaps:
            fig, ax = plt.subplots(figsize=(8, 8))
            
            t1, t2 = trees[idx1], trees[idx2]
            p1, p2 = polygons[idx1], polygons[idx2]
            
            # Draw Tree 1
            x1, y1 = p1.exterior.xy
            ax.fill(x1, y1, alpha=0.5, fc='red', ec='darkred', label=f'Tree {idx1}')
            
            # Draw Tree 2
            x2, y2 = p2.exterior.xy
            ax.fill(x2, y2, alpha=0.5, fc='blue', ec='darkblue', label=f'Tree {idx2}')
            
            # Intersection
            inter = p1.intersection(p2)
            if not inter.is_empty:
                if inter.geom_type == 'MultiPolygon':
                    for geom in inter.geoms:
                        xi, yi = geom.exterior.xy
                        ax.fill(xi, yi, alpha=0.8, fc='yellow', ec='black', label='Overlap')
                elif inter.geom_type == 'Polygon':
                    xi, yi = inter.exterior.xy
                    ax.fill(xi, yi, alpha=0.8, fc='yellow', ec='black', label='Overlap')
            
            ax.legend()
            ax.set_title(f"Overlap: Tree {idx1} & {idx2} (N={n})")
            ax.set_aspect('equal')
            
            zoom_path = output_dir / f"fail_zoom_N{n}_{idx1}_{idx2}.png"
            plt.savefig(zoom_path)
            print(f"Saved overlap detail to {zoom_path}")
            plt.close(fig)
            
        return True # Overlap found
    return False # No overlap

def main():
    MAX_N = 200
    solver = BrickTilerSolver()
    
    print(f"Debugging submission for N=1 to {MAX_N}...")
    
    for n in range(1, MAX_N + 1):
        if n % 10 == 0:
            print(f"Checking N={n}...")
            
        # 1. Try Brick Tiler
        trees, side = solver.solve(n)
        
        # 2. Try Seed Layout
        seed_trees = get_seed_layout(n)
        if seed_trees:
            all_poly = [t.get_polygon() for t in seed_trees]
            bounds = unary_union(all_poly).bounds
            seed_side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])
            
            if seed_side < side - 1e-9:
                final_trees = seed_trees
            else:
                final_trees = trees
        else:
            final_trees = trees
        
        # 3. Global Rotation
        final_trees = optimize_rotation_for_trees(final_trees)
        
        # CHECK FOR OVERLAPS
        if check_overlap_and_plot(n, final_trees):
            print(f"FAILURE STOP: Overlap detected at N={n} (AFTER rotation)")
            # Check before rotation to see if it was already there
            print("Checking if overlap existed BEFORE rotation...")
            if check_overlap_and_plot(n, trees):
                print("Overlap existed BEFORE rotation!")
            else:
                print("Overlap was introduced BY rotation!")
            break

if __name__ == "__main__":
    main()
