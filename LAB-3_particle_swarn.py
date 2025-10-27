import numpy as np

# Objective function: f(x, y) = x^2 + y^2
def objective(position):
    return position[0]**2 + position[1]**2

# PSO Parameters
NUM_PARTICLES = 30
DIMENSIONS = 2
MAX_ITER = 50

W = 0.7    # inertia weightS
C1 = 1.5   # cognitive coefficient
C2 = 1.5   # social coefficient

# Search space boundaries
X_MIN, X_MAX = -10, 10
Y_MIN, Y_MAX = -10, 10

class Particle:
    def __init__(self):
        # Initialize position randomly within bounds
        self.position = np.array([
            np.random.uniform(X_MIN, X_MAX),
            np.random.uniform(Y_MIN, Y_MAX)
        ])
        # Initialize velocity randomly
        self.velocity = np.array([
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1)
        ])
        # Personal best position starts as current position
        self.best_position = np.copy(self.position)
        self.best_fitness = objective(self.position)
        
    def update_velocity(self, global_best_position):
        r1 = np.random.random(DIMENSIONS)
        r2 = np.random.random(DIMENSIONS)
        cognitive = C1 * r1 * (self.best_position - self.position)
        social = C2 * r2 * (global_best_position - self.position)
        self.velocity = W * self.velocity + cognitive + social
        
    def update_position(self):
        self.position += self.velocity
        # Clamp to search space bounds
        self.position[0] = np.clip(self.position[0], X_MIN, X_MAX)
        self.position[1] = np.clip(self.position[1], Y_MIN, Y_MAX)
        
        # Evaluate fitness and update personal best if needed
        fitness = objective(self.position)
        if fitness < self.best_fitness:
            self.best_fitness = fitness
            self.best_position = np.copy(self.position)

def pso():
    # Initialize swarm
    swarm = [Particle() for _ in range(NUM_PARTICLES)]
    # Find global best among all particles
    global_best_position = swarm[0].best_position
    global_best_fitness = swarm[0].best_fitness
    
    for particle in swarm:
        if particle.best_fitness < global_best_fitness:
            global_best_fitness = particle.best_fitness
            global_best_position = particle.best_position
    
    # PSO main loop
    for iteration in range(MAX_ITER):
        for particle in swarm:
            particle.update_velocity(global_best_position)
            particle.update_position()
            
            # Update global best if needed
            if particle.best_fitness < global_best_fitness:
                global_best_fitness = particle.best_fitness
                global_best_position = particle.best_position
        
        # Print progress
        print(f"Iteration {iteration+1}/{MAX_ITER} — Best Fitness: {global_best_fitness:.6f}")
        
    print("\nOptimization complete!")
    print(f"Best position found: x = {global_best_position[0]:.6f}, y = {global_best_position[1]:.6f}")
    print(f"Best objective value: {global_best_fitness:.6f}")

if __name__ == "__main__":
    pso()
