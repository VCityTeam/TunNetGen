#include <cmath>
#include "utils.h"

float clamp(float x, float min, float max)
{
  return std::min(std::max(x, min), max);
}
