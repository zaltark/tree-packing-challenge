import random
import copy
from src.models.bio_growth_solver import BioGrowthSolver

class BioOptimizer:
    """Evolves the DNA for the BioGrowthSolver."""

    def __init__(self, population_size=12):
        self.population = [self._random_dna() for _ in range(population_size)]
        self.best_dna = None
        self.best_score = float('inf')

    def _random_dna(self):
        return {
            'c_factor': random.uniform(0.3, 0.7),
            'golden_angle': random.uniform(137.0, 138.0),
            'square_factor': random.uniform(0.5, 1.0),
            'rot_mode': random.choice(['interlock', 'radial', 'flat']),
            'seed_data': [
                (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.choice([0, 90, 180, 270]))
                for _ in range(4)
            ]
        }

    def evolve(self, num_trees, generations=5):
        for gen in range(generations):
            scored_pop = []
            for dna in self.population:
                solver = BioGrowthSolver(dna)
                _, side = solver.solve(num_trees)
                score = (side**2) / num_trees
                scored_pop.append((score, dna))
                
                if score < self.best_score:
                    self.best_score = score
                    self.best_dna = copy.deepcopy(dna)

            scored_pop.sort(key=lambda x: x[0])
            print(f"Gen {gen}: Best Score = {scored_pop[0][0]:.6f}")

            # Selection & Reproduction
            new_pop = [x[1] for x in scored_pop[:3]] # Elitism
            
            while len(new_pop) < len(self.population):
                parent = random.choice(scored_pop[:6])[1]
                child = copy.deepcopy(parent)
                # Mutation
                child['c_factor'] += random.uniform(-0.05, 0.05)
                child['square_factor'] = max(0, min(1, child['square_factor'] + random.uniform(-0.1, 0.1)))
                if random.random() < 0.2:
                    child['rot_mode'] = random.choice(['interlock', 'radial', 'flat'])
                new_pop.append(child)
            
            self.population = new_pop

        return self.best_dna, self.best_score
