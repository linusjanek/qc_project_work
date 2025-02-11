import math
import numpy as np
import quaternion as qt
import random
import itertools

def cost_function(start_azel_deg, end_azel_deg):
    # 1. Calculate quaternion from start azel
    start_quaternion = qt.from_spherical_coords(np.deg2rad(start_azel_deg[0]), np.deg2rad(start_azel_deg[1]))
    # 2. Calculate quaternion from end azel
    end_quaternion = qt.from_spherical_coords(np.deg2rad(end_azel_deg[0]), np.deg2rad(end_azel_deg[1]))
    # 3. Calculate relative quaternion
    rel_quaternion = end_quaternion / start_quaternion
    # 4. Calculate cost function considering shortest path
    euler = qt.as_euler_angles(rel_quaternion)
    euler = np.mod(euler + np.pi, 2 * np.pi) - np.pi  # Normalize to [-pi, pi]
    cost = np.linalg.norm(euler)
    return cost

def cost_function_norm(start_azel_deg, end_azel_deg):
    cost = cost_function(start_azel_deg, end_azel_deg)
    cost_normalized = cost / cost_function([0, 0], [180, 180])
    return cost_normalized

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

print(cost_function([0, 0], [180, 180]))

azel_start = np.array([0, 0])
azels = random_azel_dict(azel_start, 9)
costs = cost_dict(azels)
route = range(10)
print(route_cost(route, costs))
print(brute_force(azels, costs))