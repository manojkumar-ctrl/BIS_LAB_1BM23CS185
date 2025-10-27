import random
import math
from collections import defaultdict, deque


# -----------------------------
# Helper Functions
# -----------------------------

def is_connected(nodes, edges):
    """Check if the given edges connect all nodes (using BFS)."""
    if not edges:
        return False, len(nodes)
    adj = defaultdict(list)
    for u, v, _ in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()
    q = deque([nodes[0]])
    while q:
        n = q.popleft()
        if n not in visited:
            visited.add(n)
            for nei in adj[n]:
                if nei not in visited:
                    q.append(nei)
    components = len(nodes) - len(visited) + 1
    return len(visited) == len(nodes), components


def fitness(nodes, edges, penalty_factor=1000):
    """Compute total cost with penalty for disconnected networks."""
    total_cost = sum(c for _, _, c in edges)
    connected, components = is_connected(nodes, edges)
    if not connected:
        total_cost += penalty_factor * (components - 1)
    return total_cost


def von_neumann_neighbors(i, j, G, wrap=True):
    """Return von Neumann neighbors of cell (i,j)."""
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if wrap:
            ni %= G
            nj %= G
        if 0 <= ni < G and 0 <= nj < G:
            neighbors.append((ni, nj))
    return neighbors


# -----------------------------
# Main Algorithm
# -----------------------------

def parallel_cellular_network_design(nodes, edges, G=4, T=10, penalty_factor=1000):
    """
    Parallel Cellular Algorithm for Network Design and Analysis.
    Displays grid state, fitness values, and best solution at each iteration.
    """
    # Initialize random population
    grid = [[set(random.sample(edges, random.randint(1, len(edges)//2)))
             for _ in range(G)] for _ in range(G)]

    for t in range(T):
        fitness_grid = [[0]*G for _ in range(G)]

        # Evaluate fitness
        for i in range(G):
            for j in range(G):
                f = fitness(nodes, grid[i][j], penalty_factor)
                fitness_grid[i][j] = f

        # Find best fitness & corresponding edge in this iteration
        best_iter_fit = math.inf
        best_iter_edges = None
        for i in range(G):
            for j in range(G):
                if fitness_grid[i][j] < best_iter_fit:
                    best_iter_fit = fitness_grid[i][j]
                    best_iter_edges = grid[i][j]

        # Display iteration info
        print(f"\n===== Iteration {t+1} =====")
        print("Fitness Matrix:")
        for row in fitness_grid:
            print(["{:.1f}".format(x) for x in row])

        print(f"\nBest Fitness This Iteration: {best_iter_fit:.2f}")
        print(f"Best Edge Set: {best_iter_edges}")

        # Update states (in parallel logic)
        new_grid = [[set() for _ in range(G)] for _ in range(G)]
        for i in range(G):
            for j in range(G):
                # Gather neighbors
                neighbors = von_neumann_neighbors(i, j, G)
                candidate_pool = set(grid[i][j])
                for ni, nj in neighbors:
                    candidate_pool.update(grid[ni][nj])

                candidate_list = list(candidate_pool)
                if not candidate_list:
                    new_grid[i][j] = set()
                    continue

                # Generate multiple candidates from the pool
                candidates = []
                for _ in range(5):  # sample 5 new candidates
                    k = random.randint(1, len(candidate_list))
                    subset = random.sample(candidate_list, k)
                    candidates.append(set(subset))

                # Choose best candidate
                best_edges = min(candidates, key=lambda e: fitness(nodes, e, penalty_factor))
                new_grid[i][j] = best_edges

        grid = new_grid

    # Final best solution after all iterations
    best_edges = None
    best_fit = math.inf
    for i in range(G):
        for j in range(G):
            f = fitness(nodes, grid[i][j], penalty_factor)
            if f < best_fit:
                best_fit = f
                best_edges = grid[i][j]

    print("\n===== Final Best Solution =====")
    print("Edges:", best_edges)
    print("Optimized Cost:", best_fit)


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    # Example network with 6 nodes and edges with costs
    nodes = [1, 2, 3, 4, 5, 6]
    edges = [
        (1, 2, 4), (1, 3, 2), (2, 3, 1),
        (2, 4, 7), (3, 5, 3), (4, 5, 2),
        (4, 6, 5), (5, 6, 8)
    ]

    parallel_cellular_network_design(nodes, edges, G=3, T=3, penalty_factor=500)
