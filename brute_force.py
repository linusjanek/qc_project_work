from helper import route_cost
import itertools

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