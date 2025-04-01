from helper import route_cost
import itertools
import numpy as np
# https://medium.com/@davidlfliang/intro-python-algorithms-traveling-salesman-problem-ffa61f0bd47b
def brute_force(azels):
    # Generate all permutations of the cities
    all_permutations = itertools.permutations(azels)

    # Initialize variables to track the minimum cost and corresponding route
    min_cost = float('inf')
    optimal_route = None

    # Iterate over all permutations and calculate costs
    for perm in all_permutations:
        cost = route_cost(perm)
        if cost < min_cost:
            min_cost = cost
            optimal_route = perm

    return optimal_route, min_cost

def brute_force_advanced_planning(azels, subgroup_indices):
    # Generate all permutations of the subgroups an the costs inside the subgroups
    cost_perms = np.zeros((np.factorial(subgroup_indices[0]), len(subgroup_indices)))
    added_soubgroup_count = 0
    i = 0
    for subgroup_index in subgroup_indices:
        subgroup = azels[added_soubgroup_count :  added_soubgroup_count+subgroup_index]
        subgroup_perms = itertools.permutations(subgroup)
        j = 0
        for perm in subgroup_perms:
            cost = route_cost_not_wrapped(perm)
            cost_perms[i][j] = cost
            j += 1
        added_soubgroup_count += subgroup_index
        i += 1
    
    # Generate all permutations of the costs
    
