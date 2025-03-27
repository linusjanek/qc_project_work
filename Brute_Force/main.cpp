#include <iostream>
#include <numbers>
#include <vector>
#include <algorithm>
#include <random>
#include <math.h>
#include "Azel.h"
#include "Route.h"
#include "Timer.h"

Route brute_force(std::vector<Azel> points)
{
	Route minimal(points);
	do {
		Route next(points);
		if (next.route_cost() < minimal.route_cost()) minimal = next;
	} while (std::next_permutation(points.begin(), points.end()));
	return minimal;
}

int main()
{
	std::random_device rd;  // Will be used to obtain a seed for the random number engine
	std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
	std::uniform_real_distribution<> azimuths(0, 360);
	std::uniform_real_distribution<> elevations(-90, 90);

	const size_t attempts = 10;
	const size_t targets = 11;

	std::cout << "Calculating " << (size_t)(tgamma(targets + 1) / 2.0) << " permutations for each attempt (" << targets << " targets)." << std::endl;
	std::cout << "  Nr  | Time taken [s] |   Cost   | Optimal Route" << std::endl;

	for (size_t j = 0; j < attempts; j++)
	{
		std::vector<Azel> points;
		for (size_t i = 0; i < targets; i++)
		{
			points.emplace_back((int)azimuths(gen), (int)elevations(gen));
		}
		Timer timer;
		timer.start();
		auto optimal = brute_force(points);
		timer.stop();
		std::cout << std::setw(5) << j+1 << " | " << std::setw(14) << timer << " | " << std::fixed << std::setprecision(6) << optimal.route_cost() << " | " << optimal.print() << std::endl;
	}
	return 0;
}