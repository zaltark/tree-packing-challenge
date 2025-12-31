import sys
from pathlib import Path
import matplotlib.pyplot as plt
from shapely.ops import unary_union
from shapely.affinity import rotate

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree, SCALE_FACTOR

def visualize_optimal_brick():
    print("Visualizing Mathematical Exact Brick Pair...")
    
    # Optimal Parameters from Solver
    dx = 0.355
    dy = 0.805
    
    # Create the Pair
    t1 = ChristmasTree(0, 0, 0)
    t2 = ChristmasTree(dx, dy, 180)
    
    trees = [t1, t2]
    
    # Setup Plot
    fig, ax = plt.subplots(figsize=(10, 12))
    
    # Plot Trees
    colors = ['#2ecc71', '#27ae60'] # Light and Dark Green
    labels = ['Tree 1 (0°)', 'Tree 2 (180°)']
    
    all_poly = []
    
    for i, t in enumerate(trees):
        poly = t.get_polygon()
        all_poly.append(poly)
        
        x, y = poly.exterior.xy
        x = [val / float(SCALE_FACTOR) for val in x]
        y = [val / float(SCALE_FACTOR) for val in y]
        
        ax.fill(x, y, alpha=0.6, fc=colors[i], ec='black', label=labels[i])
        
        # Plot center point
        cx = float(t.center_x)
        cy = float(t.center_y)
        ax.plot(cx, cy, 'rx', markersize=10)
        ax.text(cx, cy, f" ({cx:.3f}, {cy:.3f})", fontsize=9)

    # Calculate Bounds
    union_poly = unary_union(all_poly)
    minx, miny, maxx, maxy = union_poly.bounds
    
    w = (maxx - minx) / float(SCALE_FACTOR)
    h = (maxy - miny) / float(SCALE_FACTOR)
    area = w * h
    
    # Draw Bounding Box
    px = minx / float(SCALE_FACTOR)
    py = miny / float(SCALE_FACTOR)
    
    rect = plt.Rectangle((px, py), w, h, 
                         linewidth=2, edgecolor='red', facecolor='none', linestyle='--', 
                         label=f'Bounding Box\n{w:.4f} x {h:.4f}\nArea: {area:.4f}')
    ax.add_patch(rect)
    
    # Dimensions Text
    info_text = (
        f"Optimal Offsets:\n"
        f"dx = {dx}\n"
        f"dy = {dy}\n\n"
        f"Bounding Box:\n"
        f"Width = {w:.4f}\n"
        f"Height = {h:.4f}\n"
        f"Area = {area:.4f}\n"
        f"Efficiency = {(0.7*2)/area:.2%}" # Assuming 0.7 base area per tree? No, just relative.
    )
    
    ax.text(0.05, 0.95, info_text, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_aspect('equal')
    ax.set_title("Mathematical Exact Brick Pair (The Fundamental Unit)")
    ax.legend(loc='lower right')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Set limits with margin
    margin = 0.2
    ax.set_xlim(px - margin, px + w + margin)
    ax.set_ylim(py - margin, py + h + margin)
    
    output_path = PROJECT_ROOT / "results" / "plots" / "optimal_brick_pair.png"
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    visualize_optimal_brick()
