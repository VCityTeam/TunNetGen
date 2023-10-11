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
  gbl::vec3f p00{-10.f, 0.f, 0.f};
  gbl::vec3f p01{10.f, 0.f, 0.f};
  std::shared_ptr<sdfable> main = std::make_shared<cylinder>(p00, p01, 1.f);
  main = std::make_shared<opInv>(main);

  // displacement function to have non homogeneous wall 
  auto f = [](gbl::vec3f p)
  {    
    // Based on www.shadertoy.com/view/4dS3Wd
    // By Morgan McGuire @morgan3d, http://graphicscodex.com
    // Reuse permitted under the BSD license.
    // known from this amazing website
    // https://thebookofshaders.com/13/
    // By @patriciogv - 2015 http://patriciogonzalezvivo.com

    auto fract = [](float p) {return p-floor(p);};
    auto mix = [](auto x, auto y, float a) {return x*(1.0f-a)+y*a;};
    auto hash = [&](float p)
    { p = fract(p * 0.011); p *= p + 7.5; p *= p + p; return fract(p); };
    auto noise = [&](const gbl::vec3f& x) {
      using vec3 = gbl::vec3f;
      using gbl::dot;
      using gbl::floor;
      using gbl::fract;
      
    const vec3 step(110, 241, 171);
    const vec3 i = floor(x);
    const vec3 f = fract(x);
    float n = dot(i, step);

    const vec3 u = f * f * (vec3(3.0f,3.0f,3.0f) - 2.0 * f);
    return mix(mix(mix( hash(n + dot(step, vec3(0, 0, 0))), hash(n + dot(step, vec3(1, 0, 0))), u.x()),
                   mix( hash(n + dot(step, vec3(0, 1, 0))), hash(n + dot(step, vec3(1, 1, 0))), u.x()), u.y()),
               mix(mix( hash(n + dot(step, vec3(0, 0, 1))), hash(n + dot(step, vec3(1, 0, 1))), u.x()),
                   mix( hash(n + dot(step, vec3(0, 1, 1))), hash(n + dot(step, vec3(1, 1, 1))), u.x()), u.y()), u.z());
    };
    auto fbm = [&](gbl::vec3f x) {
      using vec3 = gbl::vec3f;
      float v = 0.0;
      float a = 0.5;
      vec3 shift = vec3(100);
      for (int i = 0; i < 5; ++i) {
        v += a * noise(x);
        x = x * 2.0 + shift;
        a *= 0.5;
      }
      return v;
    };
    return fbm(p);
  };

  main = std::make_shared<opDisplace>(main, f);

  // add the laterals 
  for(int i = -8; i<=8; i+=4)
  {
    gbl::vec3f p10{float(i), -5.f, 0.f};
    gbl::vec3f p11{float(i), 5.f, 0.f};
    auto c0 = std::make_shared<opDisplace>(std::make_shared<cylinder>(p10, p11, 1.5f), f);
    main = std::make_shared<opSub>(main, c0);
  }

  // create the lidar sensor and the destination file
  std::ofstream ofs("pc.xyz");
  lidar mlidar;
  mlidar.Nphi = 500;
  mlidar.Ntheta = 500;

  // different poses because the cave network is big 
  mlidar.record(gbl::vec3f{0.f, 0.f, 0.f}, *main, ofs);
  mlidar.record(gbl::vec3f{-5.f, 0.f, 0.f}, *main, ofs);
  mlidar.record(gbl::vec3f{-9.f, 0.f, 0.f}, *main, ofs);
  mlidar.record(gbl::vec3f{5.f, 0.f, 0.f}, *main, ofs);
  mlidar.record(gbl::vec3f{8.5f, 0.f, 0.f}, *main, ofs);
  mlidar.record(gbl::vec3f{8.f, 1.f, 0.f}, *main, ofs);

  return 0;
}
