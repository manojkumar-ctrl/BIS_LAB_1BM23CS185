import numpy as np
import random

# Step 1: Define the objective function (for optimization)
def objective_function(routes, depot, customers, vehicle_capacity):
    """
    Evaluates the total distance of the given routes. Penalizes routes with capacity violations.
    
    :param routes: List of routes for each vehicle (list of customer indices).
    :param depot: Coordinates of the depot (starting point for all vehicles).
    :param customers: List of customer coordinates.
    :param vehicle_capacity: Maximum capacity of each vehicle.
    :return: Fitness value (lower is better).
    """
    total_distance = 0
    penalty = 0

    for route in routes:
        route_distance = 0
        load = 0

        # Calculate distance for the current route
        last_point = depot  # Start from the depot
        for customer_idx in route:
            customer = customers[customer_idx]
            route_distance += np.linalg.norm(np.array(last_point) - np.array(customer))
            load += 1  # Increase load (in this case, 1 per customer for simplicity)
            last_point = customer

        # Return to depot
        route_distance += np.linalg.norm(np.array(last_point) - np.array(depot))

        # Check if vehicle capacity is violated
        if load > vehicle_capacity:
            penalty += 1000  # Large penalty for exceeding capacity

        total_distance += route_distance

    # Add penalty for capacity violations
    return total_distance + penalty


# Step 2: Initialize parameters
n_nests = 50  # Number of nests (candidate solutions)
max_iter = 10  # Maximum number of iterations
pa = 0.25  # Probability of discovery (egg being discovered by host)
n_vehicles = 5  # Number of vehicles
n_customers = 20  # Number of customers
vehicle_capacity = 4  # Maximum number of customers a vehicle can serve
depot = (0, 0)  # Coordinates of the depot

# Create random customer locations
np.random.seed(42)
customers = [(np.random.randint(1, 50), np.random.randint(1, 50)) for _ in range(n_customers)]


# Step 3: Initialize population (random routes for each vehicle)
def create_random_routes():
    customer_indices = list(range(n_customers))
    np.random.shuffle(customer_indices)
    
    # Split customers randomly among vehicles (simple greedy assignment)
    routes = [customer_indices[i::n_vehicles] for i in range(n_vehicles)]
    return routes


# Step 4: Evaluate fitness (objective function value for each nest)
nests = [create_random_routes() for _ in range(n_nests)]
fitness = [objective_function(routes, depot, customers, vehicle_capacity) for routes in nests]


# Step 5: 2-opt Mutation (swapping two customers to improve the solution)
def two_opt_mutation(routes):
    """
    Apply a 2-opt mutation to a set of routes.
    
    :param routes: List of routes to apply 2-opt mutation.
    :return: New set of routes after applying 2-opt mutation.
    """
    # Pick a random route and perform 2-opt swap on it
    route = random.choice(routes)
    if len(route) < 2:
        return routes
    
    # Randomly select two different indices in the route
    i, j = random.sample(range(len(route)), 2)
    if i > j:
        i, j = j, i  # Ensure i < j
    
    # Perform the 2-opt swap (reversing the section between i and j)
    new_route = route[:i] + list(reversed(route[i:j+1])) + route[j+1:]
    
    # Replace the old route with the new one
    new_routes = [list(route) if route != routes[k] else new_route for k, route in enumerate(routes)]
    return new_routes


# Step 6: Abandon worst nests and replace them with new ones
def replace_worst_nests(nests, fitness, pa):
    sorted_indices = np.argsort(fitness)
    best_nests = [nests[i] for i in sorted_indices[:n_nests // 2]]
    worst_nests = [nests[i] for i in sorted_indices[n_nests // 2:]]

    for i in range(n_nests // 2):
        if random.random() < pa:
            # Generate a new nest using 2-opt mutation (swap customers in the route)
            new_nest = two_opt_mutation(best_nests[i])
            nests[sorted_indices[n_nests // 2 + i]] = new_nest
    return nests


# Step 7: Iterate and perform optimization
best_solution = None
best_fitness = float('inf')

for iteration in range(max_iter):
    # Evaluate fitness of each nest (path)
    fitness = [objective_function(routes, depot, customers, vehicle_capacity) for routes in nests]

    # Find the best solution (path)
    min_fitness_idx = np.argmin(fitness)
    min_fitness_value = fitness[min_fitness_idx]
    if min_fitness_value < best_fitness:
        best_fitness = min_fitness_value
        best_solution = nests[min_fitness_idx]

    # Replace worst nests with new solutions
    nests = replace_worst_nests(nests, fitness, pa)

    # Print progress (every 10 iterations)
    # if iteration % 10 == 0:
    print(f"Iteration {iteration}: Best Fitness = {best_fitness}")


# Step 8: Output the best solution (routes)
print("\nBest Solution Found:")
for i, route in enumerate(best_solution):
    print(f"Vehicle {i + 1}: {route} -> Distance: {objective_function([route], depot, customers, vehicle_capacity)}")
