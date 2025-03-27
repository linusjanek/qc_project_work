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
	std::cout << "Calculating " << (int)(tgamma(points.size() + 1) / 2.0) << " permutations." << std::endl;
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
	std::uniform_real_distribution<> elevations(0, 180);
	std::vector<Azel> points;
	for (size_t i = 0; i < 11; i++)
	{
		points.emplace_back((int)azimuths(gen), (int)elevations(gen));
	}
	Timer timer;
	timer.start();
	auto optimal = brute_force(points);
	timer.stop();
	std::cout << "Optimal Route: " << optimal.print() << "\nCost: " << optimal.route_cost() << "\nTime taken: " << timer << "s" << std::endl;
	return 0;
}