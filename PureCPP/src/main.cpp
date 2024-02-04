#include <cmath>
#include <iostream>
#include <fstream>
#include <numbers>
#include <vector>
#include <limits>
#include <random>
#include <filesystem>

#include "CLI11.hpp"

#include "vec.h"
#include "lidar.h"

int main(int argc, char* argv[])
{

  // Parse the command line argument
  CLI::App app{"Creation of cave network as if a lidar was used."};
  // argv = app.ensure_utf8(argv);

  std::string out = "out.xyz";
  app.add_option("-o, --out", out, "Output filename as an .xyz");
  int n_sample = 500;
  app.add_option("-N, --num_sample", n_sample, "Numbers of samples for the lidar in phi and in theta, point cloud size is then NxN");
  bool splitted = false;
  app.add_flag("-S, --splitted", splitted, "Split the resulting point cloud by lidar if enabled");

  CLI11_PARSE(app, argc, argv);

  // Create the cave network
  gbl::vec3 p00{-10.0, 0.0, 0.0};
  gbl::vec3 p01{10.0, 0.0, 0.0};
  std::shared_ptr<sdfable> main = std::make_shared<cylinder>(p00, p01, 1.0);
  main = std::make_shared<opInv>(main);

  // Add the laterals
  for(int i = -8; i<=8; i+=4)
  {
    gbl::vec3 p10{float(i), -5.0, 0.0};
    gbl::vec3 p11{float(i), 5.0, 0.0};
    auto c0 = std::make_shared<cylinder>(p10, p11, 1.0);
    main = std::make_shared<opSub>(main, c0);
  }

  // Displacement function to have non homogeneous wall
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

  // Add noise
  main = std::make_shared<opDisplace>(main, f);

  // Translate to be in Lyon and scale by 10
  const gbl::vec3 lyon{1842822.798333, 5176402.986592, 0.0};
  main = std::make_shared<opScale>(main, 10.0);
  main = std::make_shared<opTranslate>(main, lyon);

  // Create all the poses of the lidars
  std::vector<gbl::vec3> poses = {
    gbl::vec3{0.0, 0.0, 0.0} ,
    gbl::vec3{-5.0, 0.0, 0.0},
    gbl::vec3{-9.0, 0.0, 0.0},
    gbl::vec3{5.0, 0.0, 0.0} ,
    gbl::vec3{8.5, 0.0, 0.0} ,
    gbl::vec3{8.0, 1.0, 0.0} };
  for(auto& p: poses)
    p = p*10.0+lyon;

  // Create the lidar sensor
  lidar mlidar;
  mlidar.Nphi = n_sample;
  mlidar.Ntheta = n_sample;

  // Run the acquisition
  std::ofstream ofs(out);
  if(splitted)
    for(const auto& p:poses)
      ofs << std::setprecision (15) << p << '\n';
  std::filesystem::path outpath(out);
  for(unsigned i=0;i<poses.size();++i){
    if(splitted){
      out = outpath.stem().string()
        + "-" + std::to_string(i)
        + outpath.extension().string();
      ofs = std::ofstream(out);
    }
    mlidar.record(poses[i], *main, ofs);
  }

  return 0;
}
