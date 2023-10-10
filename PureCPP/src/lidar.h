#include "scene.h"

struct lidar
{
  int Nphi = 80, Ntheta = 80;

  void record(const gbl::vec3f& pos, const sdfable& sc, std::ostream& os);
  bool raymarch(const gbl::vec3f& pos, const gbl::vec3f& dir, 
    const sdfable& sc, gbl::vec3f& intersection);

};
