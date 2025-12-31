import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import math

import numpy as np

from shapely.affinity import rotate

from shapely.ops import unary_union

from src.models.brick_tiler_solver import BrickTilerSolver

from src.submission.formatter import SubmissionFormatter

from src.models.metric import score, ParticipantVisibleError

from src.models.prime_seeds import get_prime_seed



def optimize_rotation_for_trees(trees):



    """



    Rotates the entire cluster of trees to minimize the bounding square side.



    """



    if not trees: return trees



    



    # 1. Find Best Angle using Scaled Polygons (Shapely)



    # This part was working fine for finding the angle



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



            



    # 2. Apply Best Rotation to Unscaled Tree Objects



    if best_angle != 0:



        # Calculate Unscaled Centroid



        # We can't use scaled_centroid / 1e18 because of precision loss?



        # Better to compute mean of centers?



        # Actually, the rotation in shapely was around the polygon centroid.



        # We must rotate the trees around the SAME relative point in unscaled space.



        



        # Unscaled centroid = Scaled Centroid / SCALE_FACTOR



        from src.models.tree_geometry import SCALE_FACTOR



        ucx = float(scx) / float(SCALE_FACTOR)



        ucy = float(scy) / float(SCALE_FACTOR)



        



        new_trees = []



        rad = math.radians(best_angle)



        cos_a = math.cos(rad)



        sin_a = math.sin(rad)



        



        for t in trees:



            new_angle = t.angle + best_angle



            



            dx = float(t.center_x) - ucx



            dy = float(t.center_y) - ucy



            



            # Rotate (dx, dy)



            new_dx = dx * cos_a - dy * sin_a



            new_dy = dx * sin_a + dy * cos_a



            



            new_x = ucx + new_dx



            new_y = ucy + new_dy



            



            from src.models.tree_geometry import ChristmasTree



            new_t = ChristmasTree(new_x, new_y, new_angle)



            new_trees.append(new_t)



            



        return new_trees



        



    return trees



def main():

    MAX_N = 200

    all_results = {}

    

    # Use our best robust model: BrickTiler

    solver = BrickTilerSolver()

    

    print(f"Generating submission for N=1 to {MAX_N} using Ensemble + Global Rotation...")

    

    # Solve for each N individually to optimize the score for each configuration

    for n in range(1, MAX_N + 1):

        # 1. Try Brick Tiler

        trees, side = solver.solve(n)

        

        # 2. Try Prime Seed

        seed_trees = get_prime_seed(n)

        if seed_trees:

            all_poly = [t.get_polygon() for t in seed_trees]

            bounds = unary_union(all_poly).bounds

            seed_side = max(bounds[2]-bounds[0], bounds[3]-bounds[1])

            

            # 3. Pick Winner (Pre-Rotation)

            if seed_side < side - 1e-9:

                final_trees = seed_trees

            else:

                final_trees = trees

        else:

             final_trees = trees

        

        # 4. Global Rotation Optimization

        final_trees = optimize_rotation_for_trees(final_trees)

            

        data = []

        for t in final_trees:

            data.append({

                'x': t.center_x,

                'y': t.center_y,

                'angle': t.angle

            })

        all_results[n] = pd.DataFrame(data)

        

        if n % 25 == 0:

            print(f"Solved configuration for N={n}...")



    # Save to final submission file

    output_path = PROJECT_ROOT / "results" / "brick_tiler_submission.csv"

    SubmissionFormatter.create_submission_file(all_results, output_path)

    print(f"\nSUCCESS: Final submission generated at {output_path}")



    # Verify the submission

    print("\nVerifying submission against official metric...")

    try:

        # Read back the generated file to ensure integrity

        submission_df = pd.read_csv(output_path)

        dummy_solution = pd.DataFrame(columns=['id'])

        

        final_score = score(dummy_solution, submission_df, 'id')

        print(f"VERIFICATION PASSED! Total Score: {final_score}")

        

    except ParticipantVisibleError as e:

        print(f"VERIFICATION FAILED (Participant Error): {e}")

    except Exception as e:

        print(f"VERIFICATION FAILED (System Error): {e}")



if __name__ == "__main__":

    main()
