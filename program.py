import random
import math


# Визначення функції Сфери
def sphere_function(x):
    return sum(xi**2 for xi in x)


# Генерація випадкового рішення в межах bounds
def generate_random_solution(bounds):
    return [random.uniform(b[0], b[1]) for b in bounds]


# Обмеження рішення в межах bounds
def clamp_solution(solution, bounds):
    return [
        max(min(solution[i], bounds[i][1]), bounds[i][0]) for i in range(len(bounds))
    ]


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6, step=0.1):
    current_solution = generate_random_solution(bounds)
    current_value = func(current_solution)

    for _ in range(iterations):
        neighbor = [
            current_solution[i] + random.uniform(-step, step)
            for i in range(len(bounds))
        ]
        neighbor = clamp_solution(neighbor, bounds)
        neighbor_value = func(neighbor)

        if neighbor_value < current_value:
            current_solution, current_value = neighbor, neighbor_value

        if abs(neighbor_value - current_value) < epsilon:
            break

    return current_solution, current_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6, step=0.1):
    best_solution = generate_random_solution(bounds)
    best_value = func(best_solution)

    for _ in range(iterations):
        candidate = [
            best_solution[i] + random.uniform(-step, step) for i in range(len(bounds))
        ]
        candidate = clamp_solution(candidate, bounds)
        candidate_value = func(candidate)

        if candidate_value < best_value:
            best_solution, best_value = candidate, candidate_value

        if abs(candidate_value - best_value) < epsilon:
            break

    return best_solution, best_value


# Simulated Annealing
def simulated_annealing(
    func,
    bounds,
    iterations=1000,
    temp=1000,
    cooling_rate=0.95,
    epsilon=1e-6,
    initial_step=1,
):
    current_solution = generate_random_solution(bounds)
    current_value = func(current_solution)
    best_solution, best_value = current_solution, current_value

    for _ in range(iterations):
        # Динамічний крок залежно від температури
        step = initial_step * (temp / 1000)

        neighbor = [
            current_solution[i] + random.uniform(-step, step)
            for i in range(len(bounds))
        ]
        neighbor = clamp_solution(neighbor, bounds)
        neighbor_value = func(neighbor)

        if neighbor_value < current_value or random.random() < math.exp(
            -(neighbor_value - current_value) / temp
        ):
            current_solution, current_value = neighbor, neighbor_value

        if current_value < best_value:
            best_solution, best_value = current_solution, current_value

        temp *= cooling_rate

        if temp < epsilon:
            break

    return best_solution, best_value


if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]

    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", sa_value)
