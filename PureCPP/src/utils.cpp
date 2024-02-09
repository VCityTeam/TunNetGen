#include <cmath>
#include "utils.h"
#include <algorithm> // for min and max

float clamp(float x, float min, float max)
{
  return std::min(std::max(x, min), max);
}
