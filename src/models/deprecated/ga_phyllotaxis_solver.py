import random
import math
import pandas as pd
from decimal import Decimal
from src.models.phyllotaxis_solver import PhyllotaxisSolver
from src.models.tree_geometry import ChristmasTree

class OrganismGenome:
    """Represents the 'DNA' of a packing strategy."""
    def __init__(self, c_factor=None, angle_step=None, rot_multiplier=None):
        # Initialize with random values if not provided
        self.c_factor = c_factor if c_factor is not None else random.uniform(0.4, 0.8)
        self.angle_step = angle_step if angle_step is not None else random.uniform(130, 145)
        self.rot_multiplier = rot_multiplier if rot_multiplier is not None else random.uniform(-1, 1)
        self.fitness = float('inf')

    @classmethod
    def crossover(cls, parent1, parent2):
        """Creates a child by blending parent genomes."""
        child = cls(
            c_factor=random.choice([parent1.c_factor, parent2.c_factor]),
            angle_step=(parent1.angle_step + parent2.angle_step) / 2,
            rot_multiplier=random.choice([parent1.rot_multiplier, parent2.rot_multiplier])
        )
        return child

    def mutate(self, rate=0.1):
        """Randomly tweaks parameters."""
        if random.random() < rate:
            self.c_factor += random.uniform(-0.05, 0.05)
        if random.random() < rate:
            self.angle_step += random.uniform(-2, 2)
        if random.random() < rate:
            self.rot_multiplier += random.uniform(-0.2, 0.2)

class GAPhyllotaxisSolver:
    """
    Genetic Algorithm that evolves the parameters of a Phyllotaxis growth pattern.
    """
    def __init__(self, population_size=20):
        self.population = [OrganismGenome() for _ in range(population_size)]
        self.best_genome = None

    def evaluate_fitness(self, genome, num_trees):
        """Runs a packing simulation with the genome's parameters and returns the score."""
        # Create a modified solver using the genome's 'DNA'
        solver = PhyllotaxisSolver(c_factor=genome.c_factor)
        # Override the golden angle with the genome's angle
        solver.GOLDEN_ANGLE = genome.angle_step
        
        # Modified placement logic to use rotation multiplier
        def custom_solve_next(n_target, existing):
            if existing is None: existing = []
            placed_trees = list(existing)
            
            # Simplified logic for speed during GA evaluation
            for i in range(len(placed_trees), n_target):
                # Search loop from solver
                step = 0
                while step < 5000:
                    theta = step * genome.angle_step
                    radius = genome.c_factor * math.sqrt(step)
                    rad_theta = math.radians(theta)
                    cx = radius * math.cos(rad_theta)
                    cy = radius * math.sin(rad_theta)
                    
                    # Local rotation modified by rot_multiplier
                    angle_to_center = math.degrees(math.atan2(-cy, -cx))
                    rotation = (angle_to_center - 90) * genome.rot_multiplier
                    
                    tree = ChristmasTree(center_x=cx, center_y=cy, angle=rotation)
                    
                    # Check collision (using a simple check for speed)
                    collision = False
                    for p in placed_trees:
                        if tree.intersects(p):
                            collision = True
                            break
                    
                    if not collision:
                        placed_trees.append(tree)
                        break
                    step += 1
            
            # Calculate score
            from shapely.ops import unary_union
            from src.models.tree_geometry import SCALE_FACTOR
            all_poly = [t.get_polygon() for t in placed_trees]
            bounds = unary_union(all_poly).bounds
            side = max(bounds[2]-bounds[0], bounds[3]-bounds[1]) / float(SCALE_FACTOR)
            return (side ** 2) / n_target

        try:
            fitness = custom_solve_next(num_trees, [])
            return fitness
        except Exception:
            return float('inf')

    def evolve(self, num_trees, generations=10):
        print(f"Evolving packing strategy for N={num_trees}...")
        
        for gen in range(generations):
            # 1. Evaluate Fitness
            for genome in self.population:
                if genome.fitness == float('inf'):
                    genome.fitness = self.evaluate_fitness(genome, num_trees)
            
            # 2. Sort by fitness
            self.population.sort(key=lambda x: x.fitness)
            self.best_genome = self.population[0]
            
            print(f"Gen {gen}: Best Score = {self.best_genome.fitness:.6f} "
                  f"(c={self.best_genome.c_factor:.3f}, step={self.best_genome.angle_step:.2f})")
            
            # 3. Selection & Crossover
            new_population = self.population[:5] # Keep top 5 (Elitism)
            
            while len(new_population) < len(self.population):
                p1, p2 = random.sample(self.population[:10], 2)
                child = OrganismGenome.crossover(p1, p2)
                child.mutate()
                new_population.append(child)
                
            self.population = new_population

        return self.best_genome
