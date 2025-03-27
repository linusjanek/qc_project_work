#pragma once
#include <chrono>

class Timer
{
    // make things readable
    using clk = std::chrono::steady_clock;

    clk::time_point b; // begin
    clk::time_point e; // end

public:
    void clear() { b = e = clk::now(); }
    void start() { b = clk::now(); }
    void stop() { e = clk::now(); }

    friend std::ostream& operator<<(std::ostream& o, const Timer& timer)
    {
        return o << timer.secs();
    }

    // return time difference in seconds
    double secs() const
    {
        if (e <= b)
            return 0.0;
        auto d = std::chrono::duration_cast<std::chrono::microseconds>(e - b);
        return d.count() / 1000000.0;
    }
};