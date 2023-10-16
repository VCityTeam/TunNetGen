#include <cmath>
#include <iostream>
#include <fstream>
#include <numbers>
#include <vector>
#include <limits>
#include <random>

#include "vec.h"
#include "lidar.h"

int main()
{

  // Create the cave network
  gbl::vec3 p00{-10.0, 0.0, 0.0};
  gbl::vec3 p01{10.0, 0.0, 0.0};
  std::shared_ptr<sdfable> main = std::make_shared<cylinder>(p00, p01, 1.0);
  main = std::make_shared<opInv>(main);

  // add the laterals 
  for(int i = -8; i<=8; i+=4)
  {
    gbl::vec3 p10{float(i), -5.0, 0.0};
    gbl::vec3 p11{float(i), 5.0, 0.0};
    auto c0 = std::make_shared<cylinder>(p10, p11, 1.0);
    main = std::make_shared<opSub>(main, c0);
  }

  // displacement function to have non homogeneous wall 
  auto f = [](const gbl::vec3& p)
  {    
    // Based on www.shadertoy.com/view/4dS3Wd
    // By Morgan McGuire @morgan3d, http://graphicscodex.com
    // Reuse permitted under the BSD license.
    // known from this amazing website
    // https://thebookofshaders.com/13/
    // By @patriciogv - 2015 http://patriciogonzalezvivo.com

    auto fract = [](auto p) {return p-floor(p);};
    auto mix = [](auto x, auto y, auto a) {return x*(1.0f-a)+y*a;};
    auto hash = [&](auto p)
    { p = fract(p * 0.011); p *= p + 7.5; p *= p + p; return fract(p); };
    auto noise = [&](const gbl::vec3& x) {
      using vec3 = gbl::vec3;
      using gbl::dot;
      using gbl::floor;
      using gbl::fract;
      
    const vec3 step(110.0, 241.0, 171.0);
    const vec3 i = floor(x);
    const vec3 f = fract(x);
    auto n = dot(i, step);

    const vec3 u = f * f * (vec3(3.0,3.0,3.0) - 2.0 * f);
    return mix(mix(mix( hash(n + dot(step, vec3(0.0, 0.0, 0.0))), hash(n + dot(step, vec3(1.0, 0.0, 0.0))), u.x()),
                   mix( hash(n + dot(step, vec3(0.0, 1.0, 0.0))), hash(n + dot(step, vec3(1.0, 1.0, 0.0))), u.x()), u.y()),
               mix(mix( hash(n + dot(step, vec3(0.0, 0.0, 1.0))), hash(n + dot(step, vec3(1.0, 0.0, 1.0))), u.x()),
                   mix( hash(n + dot(step, vec3(0.0, 1.0, 1.0))), hash(n + dot(step, vec3(1.0, 1.0, 1.0))), u.x()), u.y()), u.z());
    };
    auto fbm = [&](gbl::vec3 x) {
      using gbl::vec3;
      float v = 0.0;
      float a = 0.5;
      vec3 shift = vec3(100.0);
      for (int i = 0; i < 5; ++i) {
        v += a * noise(x);
        x = x * 2.0 + shift;
        a *= 0.5;
      }
      return v;
    };
    return fbm(p);
  };

  // add noise 
  main = std::make_shared<opDisplace>(main, f);

  // translate to be in Lyon and scale by 10
  const gbl::vec3 lyon{1842822.798333, 5176402.986592, 0.0};
  // const gbl::vec3 lyon{0.0, 0.0, 0.0}; 
  main = std::make_shared<opScale>(main, 10.0);
  main = std::make_shared<opTranslate>(main, lyon);
  
  // create the lidar sensor and the destination file
  std::ofstream ofs("pc.xyz");
  lidar mlidar;
  mlidar.Nphi = 500;
  mlidar.Ntheta = 500;

  // different poses because the cave network is big 
  mlidar.record(gbl::vec3{0.0, 0.0, 0.0}  * 10.0 + lyon, *main, ofs);
  mlidar.record(gbl::vec3{-5.0, 0.0, 0.0} * 10.0 + lyon, *main, ofs);
  mlidar.record(gbl::vec3{-9.0, 0.0, 0.0} * 10.0 + lyon, *main, ofs);
  mlidar.record(gbl::vec3{5.0, 0.0, 0.0}  * 10.0 + lyon, *main, ofs);
  mlidar.record(gbl::vec3{8.5, 0.0, 0.0}  * 10.0 + lyon, *main, ofs);
  mlidar.record(gbl::vec3{8.0, 1.0, 0.0}  * 10.0 + lyon, *main, ofs);

  return 0;
}
