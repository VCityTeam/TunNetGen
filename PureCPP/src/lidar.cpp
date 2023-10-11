#include <iostream>

#include "lidar.h"


void lidar::record(const gbl::vec3f& pos, const sdfable& sc, std::ostream& os)
{
  using std::numbers::pi;
  float dphi = 2*pi/(Nphi-1);
  float dtheta = pi/(Ntheta-1);

  float phi = -pi/2.f;
  for(int i=0; i<Nphi; ++i){
    float theta = -pi;
    for(int j=0;j<Ntheta;++j){
      gbl::vec3f dir(sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta));
      gbl::vec3f intersection;
      if(raymarch(pos, dir, sc, intersection))
        os << intersection << std::endl;

      theta+=dtheta;
    }
    phi+=dphi;
  }
}

bool lidar::raymarch(const gbl::vec3f& pos, const gbl::vec3f& dir, 
  const sdfable& sc, gbl::vec3f& intersection)
{
  float depth = 0.0f;
  // warning : these parameter comes from nowhere
  for (int i = 0; i < 2000; ++i) {
    float dist = sc.sdf(pos + depth * dir);
    // warning : these parameter comes from nowhere
    if (dist < 0.01) {
      intersection = pos + depth*dir;
      return true;
    }
    depth += dist;

    // warning : these parameter comes from nowhere
    if (depth >= 2000.0) {
      return false;
    }
  }
  return false;
}