import sys
from pathlib import Path
import math

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.packing_targets import TargetLibrary

def calculate_perfect_score():
    """
    Calculates the theoretical perfect score if every configuration 
    achieved the 'Ideal Side' (perfect area packing with no gaps).
    """
    total_perfect_score = 0.0
    total_target_score = 0.0
    
    print(f"{'N':<4} | {'Ideal Side':<10} | {'Perfect Score':<12} | {'Target Side':<10} | {'Target Score':<12}")
    print("-" * 60)
    
    for n in range(1, 201):
        t = TargetLibrary.get_target(n)
        
        # Perfect Score = (Ideal Side^2) / N
        # Ideal Side = sqrt(N * 0.35855)
        # So Perfect Score = (N * 0.35855) / N = 0.35855
        # It's constant!
        perfect_score = (t.ideal_side ** 2) / n
        
        # Target Score = (Target Side^2) / N
        target_score = (t.target_side ** 2) / n
        
        total_perfect_score += perfect_score
        total_target_score += target_score
        
        if n in [1, 5, 10, 50, 100, 200]:
             print(f"{n:<4} | {t.ideal_side:<10.4f} | {perfect_score:<12.4f} | {t.target_side:<10.4f} | {target_score:<12.4f}")
             
    print("-" * 60)
    print(f"Total Perfect Score (Theoretical Limit): {total_perfect_score:.4f}")
    print(f"Total Target Score (Brick Grid Limit):   {total_target_score:.4f}")
    print(f"Current Best Submission:                 94.0289")

if __name__ == "__main__":
    calculate_perfect_score()
