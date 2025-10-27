import random
import math

# --- 1. Define cities with (x, y) coordinates ---
# For demonstration, we'll create some random cities.
# In a real application, you would load these from a file.
NUM_CITIES = 20
CITIES = [(random.randint(0, 200), random.randint(0, 200)) for _ in range(NUM_CITIES)]

# --- Helper Function: distance ---
def distance(city1, city2):
    """Return Euclidean distance between city1 and city2."""
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

# --- Helper Function: tourDistance ---
def tour_distance(route):
    """
    Calculate the total distance of a tour.
    A route is a list of city indices, e.g., [0, 3, 1, 2, ...].
    """
    total_dist = 0
    num_cities = len(route)
    for i in range(num_cities):
        # Get the distance between the current city and the next city
        from_city = CITIES[route[i]]
        # If it's the last city, the next city is the starting city
        to_city = CITIES[route[(i + 1) % num_cities]]
        total_dist += distance(from_city, to_city)
    return total_dist

# --- Helper Function: fitness ---
def fitness(route):
    """
    Calculate the fitness of a route. Fitness is the inverse of the tour distance.
    A shorter distance means a higher fitness.
    """
    return 1 / tour_distance(route)

# --- GA Function: initializePopulation ---
def initialize_population(pop_size, num_cities):
    """Create 'popSize' random routes, each visiting all cities exactly once."""
    population = []
    base_route = list(range(num_cities))
    for _ in range(pop_size):
        route = random.sample(base_route, len(base_route)) # Create a random permutation
        population.append(route)
    return population

# --- GA Function: calculateFitness (for the whole population) ---
def calculate_all_fitness(population):
    """For each route in the population, compute its fitness."""
    return [fitness(route) for route in population]

# --- GA Function: selectMatingPool ---
def select_mating_pool(population, fitness_scores, num_parents):
    """Use roulette wheel selection to pick 'numParents' routes."""
    # random.choices allows for weighted selection with replacement
    parents = random.choices(
        population=population,
        weights=fitness_scores,
        k=num_parents
    )
    return parents

# --- GA Function: crossover ---
def crossover(parent1, parent2):
    """
    Create a child route using Ordered Crossover (OX1).
    A random slice is taken from parent1, and the rest is filled from parent2.
    """
    child = [None] * len(parent1)
    
    # Choose a random slice from parent1
    start, end = sorted(random.sample(range(len(parent1)), 2))
    
    # Copy the slice from parent1 to the child
    child[start:end] = parent1[start:end]
    
    # Fill the remaining cities from parent2
    parent2_pointer = 0
    for i in range(len(child)):
        if child[i] is None:
            while parent2[parent2_pointer] in child:
                parent2_pointer += 1
            child[i] = parent2[parent2_pointer]
            parent2_pointer += 1
            
    return child

# --- GA Function: crossoverPopulation ---
def crossover_population(parents, offspring_size):
    """Create 'offspringSize' children using crossover."""
    offspring = []
    # Ensure there are always enough parents for the next crossover operation
    num_parents = len(parents)
    for i in range(offspring_size):
        # Pick two distinct parents for crossover
        parent1 = parents[i % num_parents]
        parent2 = parents[(i + 1) % num_parents]
        offspring.append(crossover(parent1, parent2))
    return offspring

# --- GA Function: mutatePopulation ---
def mutate_population(population, mutation_rate):
    """
    For each route, with a given probability, swap two random cities.
    This is known as Swap Mutation.
    """
    mutated_pop = []
    for route in population:
        mutated_route = route[:] # Create a copy
        if random.random() < mutation_rate:
            # Select two random indices to swap
            idx1, idx2 = random.sample(range(len(mutated_route)), 2)
            # Swap the cities
            mutated_route[idx1], mutated_route[idx2] = mutated_route[idx2], mutated_route[idx1]
        mutated_pop.append(mutated_route)
    return mutated_pop

# --- Main GA Function: geneticAlgorithm ---
def genetic_algorithm(pop_size, max_generations, num_parents, mutation_rate, patience):
    """The main function to run the genetic algorithm for TSP."""
    
    # Initialize population and evaluate its fitness
    population = initialize_population(pop_size, NUM_CITIES)
    fitness_scores = calculate_all_fitness(population)
    
    # Track the best route found so far
    best_fitness_idx = fitness_scores.index(max(fitness_scores))
    best_route = population[best_fitness_idx]
    best_distance = tour_distance(best_route)
    
    unchanged_generations = 0

    print(f"Initial best distance: {best_distance:.2f}")

    for gen in range(max_generations):
        # Select parents
        parents = select_mating_pool(population, fitness_scores, num_parents)
        
        # Create offspring via crossover
        offspring_size = pop_size - len(parents)
        offspring = crossover_population(parents, offspring_size)
        
        # Mutate the offspring
        mutated_offspring = mutate_population(offspring, mutation_rate)
        
        # The new population is a combination of the best parents (elitism) and the new offspring
        population = parents + mutated_offspring
        
        # Evaluate fitness of the new population
        fitness_scores = calculate_all_fitness(population)
        
        # Find the best route in the current generation
        current_best_idx = fitness_scores.index(max(fitness_scores))
        current_best_route = population[current_best_idx]
        current_best_distance = tour_distance(current_best_route)

        # Update the overall best route if the current one is better
        if current_best_distance < best_distance:
            best_distance = current_best_distance
            best_route = current_best_route
            unchanged_generations = 0
            print(f"Generation {gen + 1}: New best distance = {best_distance:.2f}")
        else:
            unchanged_generations += 1

        # Stop if the solution hasn't improved for many generations
        if unchanged_generations >= patience:
            print(f"\nStopping early after {patience} generations without improvement.")
            break
            
    return best_route, best_distance


if __name__ == "__main__":
    # GA Hyperparameters
    POP_SIZE = 100
    MAX_GENERATIONS = 500
    NUM_PARENTS = 20
    MUTATION_RATE = 0.02
    PATIENCE = 50 # For early stopping

    # Run the algorithm
    final_route, final_distance = genetic_algorithm(
        pop_size=POP_SIZE,
        max_generations=MAX_GENERATIONS,
        num_parents=NUM_PARENTS,
        mutation_rate=MUTATION_RATE,
        patience=PATIENCE
    )

    print("\n" + "="*40)
    print("Genetic Algorithm Finished!")
    print(f"Optimal route found: {final_route}")
    print(f"Total distance: {final_distance:.2f}")
    print("="*40)
