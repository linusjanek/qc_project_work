#pragma once
#include <numbers>
#include <sstream>

struct Azel {
	Azel(int az_deg, int el_deg)
		:
		az_rad((double)az_deg* std::numbers::pi / 180.0),
		el_rad((double)el_deg* std::numbers::pi / 180.0),
		az_deg(az_deg),
		el_deg(el_deg)
	{}
	bool operator<(const Azel& other)
	{
		if (az_deg == other.az_deg) return el_deg < other.el_deg;
		return az_deg < other.az_deg;
	}
	std::string print() const
	{
		std::stringstream out;
		out << "[" << std::to_string(az_deg) << "," << std::to_string(el_deg) << "]";
		return out.str();
	}
	double az_rad;
	double el_rad;
	int az_deg;
	int el_deg;
};