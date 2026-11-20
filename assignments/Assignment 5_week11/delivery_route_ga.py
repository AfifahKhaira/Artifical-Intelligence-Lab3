import random

# Distance matrix (km) for locations A, B, C, D, E, F, G
LOCATIONS = ["A", "B", "C", "D", "E", "F", "G"]
IDX = {loc: i for i, loc in enumerate(LOCATIONS)}
DELIVERY_STOPS = ["B", "C", "D", "E", "F", "G"]

DISTANCE_MATRIX = [
    [0, 4, 8, 6, 7, 9, 5],  # A
    [4, 0, 5, 7, 3, 8, 6],  # B
    [8, 5, 0, 4, 6, 3, 7],  # C
    [6, 7, 4, 0, 5, 6, 8],  # D
    [7, 3, 6, 5, 0, 4, 6],  # E
    [9, 8, 3, 6, 4, 0, 5],  # F
    [5, 6, 7, 8, 6, 5, 0],  # G
]


def calculate_total_distance(route_stops):
    """Calculate total round-trip distance starting and ending at depot A."""
    full_route = ["A"] + route_stops + ["A"]
    total_km = 0
    for i in range(len(full_route) - 1):
        u = IDX[full_route[i]]
        v = IDX[full_route[i + 1]]
        total_km += DISTANCE_MATRIX[u][v]
    return total_km


def create_random_route(rng):
    """Create a valid chromosome (random permutation of B-G)."""
    route = DELIVERY_STOPS[:]
    rng.shuffle(route)
    return route


def tournament_selection(population, distances, rng, k=3):
    """Select the shortest route among k randomly sampled candidates."""
    contestants = rng.sample(list(zip(population, distances)), k)
    contestants.sort(key=lambda item: item[1])
    return contestants[0][0][:]


def order_crossover(parent1, parent2, rng):
    """Route-preserving Order Crossover (OX) with no duplicate or missing stops."""
    n = len(parent1)
    start, end = sorted(rng.sample(range(n), 2))
    child = [None] * n
    child[start : end + 1] = parent1[start : end + 1]

    remaining = [gene for gene in parent2 if gene not in child]
    idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = remaining[idx]
            idx += 1
    return child


def swap_mutation(route, rng, mutation_rate=0.25):
    """Swap two delivery stops with probability mutation_rate."""
    mutated = route[:]
    if rng.random() < mutation_rate:
        i, j = rng.sample(range(len(mutated)), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated


def run_genetic_algorithm(
    seed=42,
    population_size=80,
    generations=100,
    elite_size=2,
    mutation_rate=0.25,
):
    """Run GA for delivery route optimisation and return best route & distance."""
    rng = random.Random(seed)
    population = [create_random_route(rng) for _ in range(population_size)]

    for _ in range(generations):
        distances = [calculate_total_distance(ind) for ind in population]
        ranked = sorted(zip(population, distances), key=lambda item: item[1])

        # Elitism: keep best routes unchanged
        next_population = [ind[:] for ind, _ in ranked[:elite_size]]

        # Generate remaining offspring via selection, crossover, and mutation
        while len(next_population) < population_size:
            parent1 = tournament_selection(population, distances, rng, k=3)
            parent2 = tournament_selection(population, distances, rng, k=3)
            child = order_crossover(parent1, parent2, rng)
            child = swap_mutation(child, rng, mutation_rate=mutation_rate)
            next_population.append(child)

        population = next_population

    final_distances = [calculate_total_distance(ind) for ind in population]
    best_stops, best_distance = min(
        zip(population, final_distances), key=lambda item: item[1]
    )
    best_route = ["A"] + best_stops + ["A"]
    return best_route, best_distance


def main():
    best_route, best_distance = run_genetic_algorithm(
        seed=42,
        population_size=80,
        generations=100,
        elite_size=2,
        mutation_rate=0.25,
    )
    print("Best delivery route:", " -> ".join(best_route))
    print(f"Total distance: {best_distance} km")


if __name__ == "__main__":
    main()