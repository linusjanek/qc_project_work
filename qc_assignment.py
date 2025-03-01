import math
import numpy as np
import random
import itertools

def cost_function_norm(start_azel_deg, end_azel_deg):
    return np.arccos(np.sin(start_azel_deg[1] * np.pi / 180) * np.sin(end_azel_deg[1] * np.pi / 180) + np.cos(start_azel_deg[1] * np.pi / 180) * np.cos(end_azel_deg[1] * np.pi / 180) * np.cos((end_azel_deg[0] - start_azel_deg[0]) * np.pi / 180)) / np.pi

def random_azel_dict(start_point, n):
    azel = {i+1:[random.randint(0, 360), random.randint(0, 360)] for i in range(n)}
    azel[0] = start_point
    return azel

def cost_dict(azel):
    cost = {}
    keys = list(azel.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            key_pair = (keys[i], keys[j])
            cost[key_pair] = cost_function_norm(azel[keys[i]], azel[keys[j]])
    return cost

# https://medium.com/@davidlfliang/intro-python-algorithms-traveling-salesman-problem-ffa61f0bd47b
def route_cost(route, costs):
    total_cost = 0
    n = len(route)
    for i in range(n-1):
        current_azel = route[i]
        next_azel = route[i + 1] # % n  # Wrap around to the start of the route -> do we want to return to the start point?
        if (current_azel, next_azel) in costs:
            total_cost += costs[(current_azel, next_azel)]
            # print(costs[(current_azel, next_azel)])
        else:
            total_cost += costs[(next_azel, current_azel)]
            # print(costs[(next_azel, current_azel)])
    return total_cost

# https://medium.com/@davidlfliang/intro-python-algorithms-traveling-salesman-problem-ffa61f0bd47b
def brute_force(azels, costs):
    # Generate all permutations of the cities
    all_permutations = itertools.permutations(azels)

    # Initialize variables to track the minimum cost and corresponding route
    min_cost = float('inf')
    optimal_route = None

    # Iterate over all permutations and calculate costs
    for perm in all_permutations:
        cost = route_cost(perm, costs)
        if cost < min_cost:
            min_cost = cost
            optimal_route = perm

    return optimal_route, min_cost

point_list = [
    [[0, 0], [0, 0]], 
    [[0, 0], [0, 90]], 
    [[0, 0], [90, 0]], 
    [[0, 0], [90, 90]], 
    [[0, 0], [180, 0]], 
    [[0, 0], [180, 90]], 
    [[0, 0], [270, 0]], 
    [[0, 0], [270, 90]], 
    [[0, 0], [360, 0]]
    ]

for p in point_list:
    print(f"{cost_function_norm(p[0], p[1])} == {cost_function_norm(p[1], p[0])}")

azel_start = np.array([0, 0])
azels = random_azel_dict(azel_start, 9)
costs = cost_dict(azels)
route = range(10)
print(route_cost(route, costs))
print(brute_force(azels, costs))