import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tree_geometry import ChristmasTree

def test_tree_logic():
    print("Testing Tree Geometry...")
    
    # Create two trees far apart
    tree1 = ChristmasTree(center_x=0, center_y=0, angle=0)
    tree2 = ChristmasTree(center_x=5, center_y=5, angle=0)
    
    print(f"Tree 1 and Tree 2 intersect? {tree1.intersects(tree2)}") # Should be False
    
    # Create two trees overlapping
    tree3 = ChristmasTree(center_x=0.1, center_y=0.1, angle=45)
    print(f"Tree 1 and Tree 3 intersect? {tree1.intersects(tree3)}") # Should be True
    
    print("Test Complete.")

if __name__ == "__main__":
    test_tree_logic()
