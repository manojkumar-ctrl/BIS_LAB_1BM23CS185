import numpy as np
import matplotlib.pyplot as plt

# Generate random data points
np.random.seed(42)
num_points = 100
X = np.vstack([
    np.random.normal(loc=[3, 3], size=(num_points//2, 2)),  # Cluster 1
    np.random.normal(loc=[7, 7], size=(num_points//2, 2))   # Cluster 2
])

# Number of clusters (K)
K = 2

# GWO Parameters
num_wolves = 30
num_iterations = 5
dim = K * 2  # Each centroid has 2 coordinates (x, y)

# Search space boundaries
lower_bound = 0
upper_bound = 10

# Initialize wolves' positions (randomly within the search space)
wolves = np.random.uniform(lower_bound, upper_bound, (num_wolves, dim))

# Initialize alpha, beta, delta, omega wolves
alpha_pos = np.zeros(dim)
alpha_score = float('inf')

beta_pos = np.zeros(dim)
beta_score = float('inf')

delta_pos = np.zeros(dim)
delta_score = float('inf')

omega_pos = np.zeros(dim)
omega_score = float('inf')

# To track fitness over iterations (for convergence curve)
fitness_curve = []

# Euclidean distance function
def euclidean_distance(x1, x2):
    return np.linalg.norm(x1 - x2)

# Fitness function (K-means objective: sum of squared distances to centroids)
def fitness(wolves, X, K):
    wolf_centroids = wolves.reshape((K, 2))
    total_distance = 0
    for point in X:
        # Calculate the distance to the closest centroid
        distances = [euclidean_distance(point, centroid) for centroid in wolf_centroids]
        total_distance += min(distances)**2  # Sum of squared distances
    return total_distance

# Clip wolf positions to remain within boundaries
def clip_positions(wolves, lb, ub):
    np.clip(wolves, lb, ub, out=wolves)

# Main GWO loop
for iter in range(num_iterations):
    for i in range(num_wolves):
        # Calculate the fitness of each wolf (position)
        fit = fitness(wolves[i], X, K)
        
        # Update alpha, beta, delta, omega positions based on fitness
        if fit < alpha_score:
            alpha_score = fit
            alpha_pos = wolves[i].copy()
        elif fit < beta_score:
            beta_score = fit
            beta_pos = wolves[i].copy()
        elif fit < delta_score:
            delta_score = fit
            delta_pos = wolves[i].copy()
        elif fit < omega_score:
            omega_score = fit
            omega_pos = wolves[i].copy()

    # Calculate "a" for the hunting equation (linearly decreasing from 2 to 0)
    a = 2 - iter * (2 / num_iterations)

    # Update the positions of all wolves based on the encircling and hunting equations
    for i in range(num_wolves):
        for j in range(dim):
            r1 = np.random.rand()
            r2 = np.random.rand()

            # Encircling & Hunting Equations
            A1 = 2 * a * r1 - a
            C1 = 2 * r2
            D_alpha = np.abs(C1 * alpha_pos[j] - wolves[i, j])
            X1 = alpha_pos[j] - A1 * D_alpha

            r1 = np.random.rand()
            r2 = np.random.rand()

            A2 = 2 * a * r1 - a
            C2 = 2 * r2
            D_beta = np.abs(C2 * beta_pos[j] - wolves[i, j])
            X2 = beta_pos[j] - A2 * D_beta

            r1 = np.random.rand()
            r2 = np.random.rand()

            A3 = 2 * a * r1 - a
            C3 = 2 * r2
            D_delta = np.abs(C3 * delta_pos[j] - wolves[i, j])
            X3 = delta_pos[j] - A3 * D_delta

            # Update wolf's position based on the three best wolves
            wolves[i, j] = (X1 + X2 + X3) / 3

    # Clip wolf positions to ensure they remain within the defined boundaries
    clip_positions(wolves, lower_bound, upper_bound)
    
    # Record the best fitness value (for convergence curve)
    fitness_curve.append(alpha_score)

    # Print positions of Alpha, Beta, Delta, Omega wolves at each iteration
    print(f"Iteration {iter + 1}:")
    print(f"  Alpha Wolf Position: {alpha_pos} | Fitness: {alpha_score}")
    print(f"  Beta Wolf Position: {beta_pos} | Fitness: {beta_score}")
    print(f"  Delta Wolf Position: {delta_pos} | Fitness: {delta_score}")
    print(f"  Omega Wolf Position: {omega_pos} | Fitness: {omega_score}")
    print("-" * 50)

# Final solution (best centroids) is the position of the alpha wolf
print(f"Best solution found with fitness value: {alpha_score}")
alpha_pos = alpha_pos.reshape((K, 2))
print("Best centroids (Alpha Wolf):")
for idx, centroid in enumerate(alpha_pos):
    print(f"Centroid {idx + 1}: {centroid}")

# Plotting the final result of clustering with the best centroids
plt.figure(figsize=(8, 8))

# Plot data points
plt.scatter(X[:, 0], X[:, 1], c='blue', label='Data Points', alpha=0.6)

# Plot the centroids
for idx, centroid in enumerate(alpha_pos):
    plt.scatter(centroid[0], centroid[1], color='red', s=100, label=f'Centroid {idx + 1}')
    
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Clustering Result with Grey Wolf Optimizer')
plt.legend()
plt.grid(True)
plt.show()
