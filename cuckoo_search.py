import numpy as np
import random

# Step 1: Define the objective function (for optimization)
def objective_function(x):
    # Example: Sphere function (minimization)
    return np.sum(x**2)

# Step 2: Initialize parameters
n_nests = 50  # Number of nests
max_iter = 100  # Maximum number of iterations
pa = 0.25  # Probability of discovery (egg being discovered by host)
n_dim = 10  # Number of dimensions (problem size)
alpha = 1.5  # Scaling factor for Lévy flights

# Step 3: Initialize population (random positions)
nests = np.random.uniform(-10, 10, (n_nests, n_dim))

# Step 4: Evaluate fitness (objective function value for each nest)
fitness = np.apply_along_axis(objective_function, 1, nests)

# Step 5: Lévy flight approximation (using a simplified version without external dependencies)
def levy_flight(n_dim, alpha=1.5):
    # Simplified Lévy flight step using a random walk with a power law
    # We use a normal distribution for this approximation, though it's less accurate than the original Levy distribution
    u = np.random.normal(0, 1, n_dim)
    v = np.random.normal(0, 1, n_dim)
    step = u / np.power(np.abs(v), 1 / alpha)
    return step

# Step 6: Abandon worst nests and replace them with new ones
def replace_worst_nests(nests, fitness, pa, max_iter):
    # Sort nests based on fitness values
    sorted_indices = np.argsort(fitness)
    best_nests = nests[sorted_indices[:n_nests // 2]]
    worst_nests = nests[sorted_indices[n_nests // 2:]]
    
    # Abandon the worst nests and replace them
    for i in range(n_nests // 2):
        if random.random() < pa:
            # Generate a new nest using Lévy flight
            step = levy_flight(n_dim, alpha)
            new_nest = best_nests[i] + step
            new_nest = np.clip(new_nest, -10, 10)  # Ensure within bounds
            nests[sorted_indices[n_nests // 2 + i]] = new_nest
    return nests

# Step 7: Iterate and perform optimization
best_solution = None
best_fitness = float('inf')

for iteration in range(max_iter):
    # Evaluate fitness of each nest
    fitness = np.apply_along_axis(objective_function, 1, nests)

    # Find the best solution
    min_fitness_idx = np.argmin(fitness)
    min_fitness_value = fitness[min_fitness_idx]
    if min_fitness_value < best_fitness:
        best_fitness = min_fitness_value
        best_solution = nests[min_fitness_idx]

    # Replace worst nests with new solutions
    nests = replace_worst_nests(nests, fitness, pa, max_iter)

    # Print progress (every 10 iterations)
    # if iteration % 10 == 0:
    print(f"Iteration {iteration}: Best Fitness = {best_fitness}")

# Step 8: Output the best solution
print("\nBest Solution Found:")
print(f"Position: {best_solution}")
print(f"Fitness: {best_fitness}")
