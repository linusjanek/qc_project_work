#include <iostream>
#include <numbers>
#include <vector>
#include <algorithm>
#include <random>
#include <math.h>
#include <fstream>
#include <filesystem>
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
Route brute_force_advanced_planning(std::vector<Azel> points, std::vector<int> subgroup_indices){
	std::vector<int> numbers(points.size());
	for (size_t i = 0; i < points.size(); i++)
	{
		numbers[i] = i;
	}
	Route minimal(points);
	int subgroup_maxsize = 0;
	int prevsubgroup_maxsize = 0;
	do {
		// Check if the current permutation of numbers is valid for the subgroup indices
		bool valid = true;
		for (size_t i = 0; i < subgroup_indices.size(); i++)
		{
			subgroup_maxsize += subgroup_indices[i];
			for (size_t j = prevsubgroup_maxsize; j < subgroup_maxsize; j++)
			{
				if (numbers[j] > subgroup_maxsize){
					valid = false;
					break;
				}
			}
			if(valid == false) break;
			prevsubgroup_maxsize = subgroup_maxsize;
		}

		if(valid){
			Route next(points);
			if (next.route_cost() < minimal.route_cost()) minimal = next;
		}
	} while (std::next_permutation(points.begin(), points.end())
		&& std::next_permutation(numbers.begin(), numbers.end()));
	return minimal;

}

int main()
{
	std::random_device rd;  // Will be used to obtain a seed for the random number engine
	std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
	std::uniform_real_distribution<> azimuths(0, 360);
	std::uniform_real_distribution<> elevations(-90, 90);

	const size_t attempts = 10;
	const size_t max_targets = 16;
	const size_t max_subgroup_size = 4;

	for (size_t targets = 8; targets < max_targets + 1; targets++){
		for (size_t subgroup_size = 2;subgroup_size <= max_subgroup_size; subgroup_size++){
			
			const std::string fileName = "out/output" + std::to_string(targets) + "_" + std::to_string(subgroup_size) + ".json";

			std::cout << "Calculating " << (size_t)(tgamma(targets + 1) / 2.0) << " permutations for each attempt (" << targets << " targets, subgroup size: " << subgroup_size << ")." << std::endl;
			std::cout << "  Nr  | Time taken [s] |   Cost   | Optimal Route" << std::endl;

			std::stringstream json;
			json << "[\n";
			for (size_t j = 0; j < attempts; j++)
			{
				std::vector<Azel> points;
				for (size_t i = 0; i < targets; i++)
				{
					points.emplace_back((int)azimuths(gen), (int)elevations(gen));
				}
				size_t subgroup_rest = targets % subgroup_size;

				std::vector<int> subgroup_indices;
				for (size_t i = 0; i < int(targets/subgroup_size); i++)
				{
					subgroup_indices.push_back(subgroup_size);
				}
				if (subgroup_rest > 0)
				{
					subgroup_indices.push_back(subgroup_rest);
				}
				Timer timer;
				timer.start();
				auto optimal = brute_force_advanced_planning(points, subgroup_indices);
				timer.stop();
				std::cout << std::setw(5) << j + 1 << " | " << std::setw(14) << timer << " | " << std::fixed << std::setprecision(6) << optimal.route_cost() << " | " << optimal.print() << std::endl;
				json << optimal.printJSON();
			}
			json.seekp(-2, std::ios_base::end);
			json << "\n]";
			std::ofstream file(fileName);
			std::string json_str = json.str();
			file << json_str;
		}
	{
		const std::string fileName = "out/output" + std::to_string(targets) + ".json";

		std::cout << "Calculating " << (size_t)(tgamma(targets + 1) / 2.0) << " permutations for each attempt (" << targets << " targets)." << std::endl;
		std::cout << "  Nr  | Time taken [s] |   Cost   | Optimal Route" << std::endl;

		std::stringstream json;
		json << "[\n";
		for (size_t j = 0; j < attempts; j++)
		{
			std::vector<Azel> points;
			for (size_t i = 0; i < targets; i++)
			{
				points.emplace_back((int)azimuths(gen), (int)elevations(gen));
			}
			Timer timer;
			timer.start();
			auto optimal = brute_force_advanced_planning(points, );
			timer.stop();
			std::cout << std::setw(5) << j + 1 << " | " << std::setw(14) << timer << " | " << std::fixed << std::setprecision(6) << optimal.route_cost() << " | " << optimal.print() << std::endl;
			json << optimal.printJSON();
		}
		json.seekp(-2, std::ios_base::end);
		json << "\n]";
		std::ofstream file(fileName);
		std::string json_str = json.str();
		file << json_str;
	}
}
return 0;
}