#include "scene.h"

struct lidar
{
  int Nphi = 80, Ntheta = 80;

  void record(const gbl::vec3& pos, const sdfable& sc, std::ostream& os);
  bool raymarch(const gbl::vec3& pos, const gbl::vec3& dir, 
    const sdfable& sc, gbl::vec3& intersection);

};
