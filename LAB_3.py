import numpy as np
import random

# Define number of cities and their coordinates
cities = [ [0, 0], [1, 5], [5, 2], [3, 8], [7, 7],
    [9, 0], [6, 5], [4, 6], [8, 3], [2, 1]]

# Number of ants, iterations, pheromone parameters
num_ants = 5000
iterations = 10
alpha = 1    # Pheromone importance (increased a little)
beta = 1       # Heuristic importance (1/distance)
rho = 0.1    # Pheromone evaporation rate (moderate value)
q = 10        # Pheromone deposit factor (increased for stronger influence) 
# Number of cities
num_cities = len(cities)

# Create distance matrix
distances = np.zeros((num_cities, num_cities))
for i in range(num_cities):
    for j in range(num_cities):
        if i != j:
            distances[i][j] = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))

# Initialize pheromone matrix with a small constant value (not too high)
pheromone = np.ones((num_cities, num_cities)) * 0.1  # Lower initial pheromone values

# Precompute heuristic (inverse of distance)
heuristic = 1 / (distances + np.eye(num_cities))  # Avoid division by zero on diagonal
np.fill_diagonal(heuristic, 0)

# Function to construct a solution (tour) for each ant
def construct_solution():
    path = []
    visited = set()

    # Randomly choose a starting city
    current_city = random.randint(0, num_cities - 1)
    path.append(current_city)
    visited.add(current_city)

    while len(path) < num_cities:
        probabilities = calculate_transition_probabilities(current_city, visited)
        next_city = np.random.choice(range(num_cities), p=probabilities)
        path.append(next_city)
        visited.add(next_city)
        current_city = next_city

    return path

# Function to calculate transition probabilities for the ants
def calculate_transition_probabilities(current_city, visited):
    probabilities = np.zeros(num_cities)
    pheromone_strength = pheromone[current_city]
    heuristic_info = heuristic[current_city]

    # Calculate probability for each city based on pheromone and heuristic
    for city in range(num_cities):
        if city not in visited:
            probabilities[city] = (pheromone_strength[city] ** alpha) * (heuristic_info[city] ** beta)

    total_prob = np.sum(probabilities)
    if total_prob == 0:
        unvisited = [city for city in range(num_cities) if city not in visited]
        for city in unvisited:
            probabilities[city] = 1.0
        total_prob = len(unvisited)

    return probabilities / total_prob

# Function to calculate the total distance of a given path
def calculate_distance(path):
    distance = 0
    for i in range(len(path)):
        from_city = path[i]
        to_city = path[(i + 1) % num_cities]  # wrap around to start
        distance += distances[from_city][to_city]
    return distance

# Function to update pheromone levels based on solutions
def update_pheromones(all_paths, all_distances):
    global pheromone
    pheromone *= (1 - rho)  # Evaporate pheromone

    # Update pheromones for each path based on its quality (distance)
    for path, distance in zip(all_paths, all_distances):
        pheromone_deposit = q / distance
        for i in range(len(path)):
            from_city = path[i]
            to_city = path[(i + 1) % num_cities]
            pheromone[from_city][to_city] += pheromone_deposit
            pheromone[to_city][from_city] += pheromone_deposit  # symmetric update

    # Normalize pheromone levels and add slight randomness to prevent stagnation
    pheromone = pheromone / np.sum(pheromone)  # Normalize to avoid infinite growth
    pheromone += np.random.rand(num_cities, num_cities) * 0.01  # Small noise for exploration

# Main loop to run the Ant Colony Optimization
best_distance = float('inf')
best_path = None

for iteration in range(iterations):
    all_paths = []
    all_distances = []

    # Each ant constructs a solution
    for ant in range(num_ants):
        path = construct_solution()
        distance = calculate_distance(path)
        all_paths.append(path)
        all_distances.append(distance)

        if distance < best_distance:
            best_distance = distance
            best_path = path

    # Update pheromones based on solutions found by ants
    update_pheromones(all_paths, all_distances)

    # Output the best distance at this iteration
    print(f"Iteration {iteration + 1}/{iterations} - Best distance: {best_distance:.2f}")

# Output the best path and its distance
print("\nBest path found:", best_path)
print("Best path distance:", round(best_distance, 2))
