#pragma once
#include <vector>
#include <numbers>
#include <cmath>
#include <sstream>
#include "Timer.h"
#include "Azel.h"

class Route {
public:
	Route(const std::vector<Azel> points)
		:
		points(points)
	{
		for (size_t i = 0; i < points.size() - 1; i++)
		{
			cost += edge_cost(points.at(i), points.at(i + 1));
		}
		cost += edge_cost(points.back(), points.front());
	}
	static double edge_cost(Azel start, Azel end)
	{
		return 0.1 * std::acos(std::sin(start.el_rad) * std::sin(end.el_rad) + std::cos(start.el_rad) * std::cos(end.el_rad) * std::cos(end.az_rad - start.az_rad)) / std::numbers::pi;
	}
	double route_cost() const
	{
		return cost;
	}
	std::string print() const
	{
		std::stringstream out;
		for (const auto& p : points)
		{
			out << p.print() << " ";
		}
		return out.str();
	}
	std::string printJSON(const Timer& timer) const
	{
		std::stringstream out;
		out << "\t{\n\t\t\"points\": [\n";
		for (const auto& p : points)
		{
			out << "\t\t\t[\n\t\t\t\t" << p.az_deg << ",\n\t\t\t\t" << p.el_deg << "\n\t\t\t],\n";
		}
		out.seekp(-2, std::ios_base::end);
		out << "\n\t\t],\n\t\t\"cost\": " << cost << ",\n\t\t\"time\": " << timer << "\n\t},\n";
		return out.str();
	}
private:
	std::vector<Azel> points;
	double cost = 0;
};
