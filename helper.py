import numpy as np
import random

# return the rotation angle
def cost_function(start_azel_deg, end_azel_deg) -> float:
    # convert to radians
    start_azel = [deg * np.pi / 180 for deg in start_azel_deg]
    end_azel = [deg * np.pi / 180 for deg in end_azel_deg]
    return 0.1*np.arccos(np.sin(start_azel[1]) * np.sin(end_azel[1]) + np.cos(start_azel[1]) * np.cos(end_azel[1]) * np.cos(end_azel[0] - start_azel[0]))/np.pi

def vector_from_azel(azel: list[int]) -> list[int]:
    # convert to radians
    azel = [deg * np.pi / 180 for deg in azel]
    return [np.sin(azel[0]) * np.cos(azel[1]), np.cos(azel[0]) * np.cos(azel[1]), np.sin(azel[1])]

def rnd_points(n: int) -> list[list[int]]:
    return [[random.randint(0, 360), random.randint(-90, 90)] for i in range(n)]

def route_cost(route: list[list[int]]) -> float:
    total_cost = 0
    n = len(route)
    for i in range(n):
        current_azel = route[i]
        next_azel = route[(i + 1) % n] # Wrap around to the start of the route
        total_cost += cost_function(current_azel, next_azel)
    return total_cost

def route_cost_not_wrapped(route: list[list[int]]) -> float:
    total_cost = 0
    n = len(route)
    for i in range(n-1):
        current_azel = route[i]
        next_azel = route[(i + 1) % n] # Wrap around to the start of the route
        total_cost += cost_function(current_azel, next_azel)
    return total_cost

def generate_subgroup_indices(targets: int, subgroup_size: int) -> list[int]:
    subgroup_indices = []
    subgroup_rest = targets % subgroup_size
    subgroup_count = targets // subgroup_size
    for i in range(subgroup_count):
        subgroup_indices.append(subgroup_size)
    if subgroup_rest > 0:
        subgroup_indices.append(subgroup_rest)
    return subgroup_indices