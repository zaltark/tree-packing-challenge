import sys
from pathlib import Path
import pandas as pd
from decimal import Decimal

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.packing_targets import TargetLibrary

def audit_efficiency():
    print(f"{ 'N':<4} | {'Target Side':<12} | {'Score Area':<12} | {'Tree Area':<10} | {'Efficiency':<10} | {'Grid':<8}")
    print("-" * 75)
    
    # Approx area of 1 packed tree in a brick
    TREE_PACKED_AREA = 0.35855
    
    bad_configs = []
    
    for n in range(1, 201):
        t = TargetLibrary.get_target(n)
        
        score_area = t.side_length ** 2
        min_possible_area = n * TREE_PACKED_AREA
        
        eff = min_possible_area / score_area
        
        # Flag inefficient configs (arbitrary threshold, say < 0.7)
        if eff < 0.75:
            bad_configs.append(n)
            
        if n in [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 50, 100, 200]:
             print(f"{n:<4} | {t.side_length:<12.4f} | {score_area:<12.4f} | {min_possible_area:<10.4f} | {eff:<10.4f} | {t.cols}x{t.rows}")

    print(f"\nInefficient Configs (Eff < 0.75): {len(bad_configs)} found.")
    print(f"Examples: {bad_configs[:20]}...")

if __name__ == "__main__":
    audit_efficiency()
